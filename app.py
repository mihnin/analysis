import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import visualization as vis
#import inventory_analysis as ia
import io
from io import BytesIO
import xlsxwriter  # Добавьте эту строку
import historical_analysis as ha
import forecast_analysis as fa
import utils
from logging_config import setup_logger, log_user_action, create_private_download_button

# Инициализация логирования
logger = setup_logger()
st.session_state['logger'] = logger

st.set_page_config(page_title="Анализ и прогнозирование управления запасами", layout="wide")

# Функция для конвертации DataFrame в Excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Записываем заголовки
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value)

    # Записываем данные
    for row_num, row in enumerate(df.values):
        for col_num, value in enumerate(row):
            worksheet.write(row_num + 1, col_num, value.encode('utf-8').decode('utf-8') if isinstance(value, str) else value)

    workbook.close()
    processed_data = output.getvalue()
    return processed_data

def main():
    st.title("Анализ и прогнозирование управления запасами")

    # Инициализация session_state
    if 'historical_df' not in st.session_state:
        st.session_state.historical_df = None
    if 'forecast_df' not in st.session_state:
        st.session_state.forecast_df = None

    # Загрузка исторических данных
    st.header("Загрузка исторических данных")
    historical_file = st.file_uploader("Выберите Excel файл с историческими данными", type=["xlsx"], key="historical_uploader")

    if historical_file is not None and st.session_state.get("historical_df") is None:
        st.session_state.historical_df = pd.read_excel(historical_file)
        log_user_action(
            action="Загрузка исторических данных",
            message=f"Загружен файл {historical_file.name}. Количество строк: {st.session_state.historical_df.shape[0]}."
        )
    
    if historical_file is not None:
        st.session_state.historical_df = pd.read_excel(historical_file)
        st.success("Файл с историческими данными успешно загружен!")
        
    if st.session_state.historical_df is not None:
        st.write("Первые несколько строк загруженных исторических данных:")
        st.write(st.session_state.historical_df.head())

        # Выбор обязательных полей для исторических данных
        date_column = st.selectbox("Выберие поле с датой", st.session_state.historical_df.columns)
        branch_column = st.selectbox("Выберите поле с номером филиала", st.session_state.historical_df.columns)
        material_column = st.selectbox("Выберите поле с наименованием материала", st.session_state.historical_df.columns)
        start_quantity_column = st.selectbox("Выберите поле с количеством остатков на начало", st.session_state.historical_df.columns)
        end_quantity_column = st.selectbox("Выберите поле с количеством остатков на конец", st.session_state.historical_df.columns)
        end_cost_column = st.selectbox("Выберите поле со стоимостью остатков на конец", st.session_state.historical_df.columns)

        # Опциональное поле для фактического списания/расхода
        consumption_column = None
        consumption_convention = 'AUTO'
        if st.checkbox("Есть колонка с фактическим списанием/расходом (рекомендуется для точных расчетов)"):
            consumption_column = st.selectbox("Выберите поле с фактическим списанием", st.session_state.historical_df.columns)

            # Выбор конвенции знака списания
            with st.expander("⚙️ Настройки знака списания (для продвинутых пользователей)"):
                st.write("""
                **В разных системах учета списание может быть представлено по-разному:**
                - **AUTO (рекомендуется)**: Система автоматически определит конвенцию по балансу данных
                - **POSITIVE**: Списание = положительное число (расход товара)
                - **NEGATIVE**: Списание = отрицательное число (уменьшение запаса)
                - **ABS**: Просто взять модуль всех значений (безопасный вариант)
                """)
                consumption_convention = st.radio(
                    "Как представлено списание в ваших данных?",
                    ['AUTO', 'POSITIVE', 'NEGATIVE', 'ABS'],
                    index=0,
                    help="AUTO - система сама определит правильный формат"
                )

        # Выбор конкретных значений признаков для исторических данных
        selected_materials = st.multiselect("Выберите материалы для анализа", st.session_state.historical_df[material_column].unique())
        selected_branches = st.multiselect("Выберите филиалы для анализа", st.session_state.historical_df[branch_column].unique())

        # Фильтация исторических данных по выбранным значениям
        if selected_materials:
            st.session_state.historical_df = st.session_state.historical_df[st.session_state.historical_df[material_column].isin(selected_materials)]
        if selected_branches:
            st.session_state.historical_df = st.session_state.historical_df[st.session_state.historical_df[branch_column].isin(selected_branches)]

        # Выбор периода анализа
        min_date = pd.to_datetime(st.session_state.historical_df[date_column]).min().date()
        max_date = pd.to_datetime(st.session_state.historical_df[date_column]).max().date()
        start_date = st.date_input("Выберите начальную дату анализа", min_date)
        end_date = st.date_input("Выберите конечную дату анализа", max_date)

        # Преобразование start_date и end_date в datetime
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)

        # Фильтрация данных по выбранному периоду
        st.session_state.historical_df = st.session_state.historical_df[(pd.to_datetime(st.session_state.historical_df[date_column]) >= start_datetime) & 
                                          (pd.to_datetime(st.session_state.historical_df[date_column]) <= end_datetime)]

        # Анализ исторических данных
        interest_rate = st.number_input("Введите процентную ставку для расчета упущенной выгоды", min_value=0.0, max_value=100.0, value=5.0, step=0.1)

        # НОВЫЙ ПАРАМЕТР: Lead Time (время выполнения заказа)
        lead_time_days = st.number_input(
            "Время выполнения заказа (Lead Time) в днях",
            min_value=1,
            max_value=365,
            value=30,
            step=1,
            help="Среднее время от размещения заказа до получения товара. Используется для расчета точки заказа (ROP)."
        )

        if st.button("Провести анализ исторических данных"):
            try:
                results_df, explanation = ha.analyze_historical_data(
                    st.session_state.historical_df,
                    date_column,
                    branch_column,
                    material_column,
                    start_quantity_column,
                    end_quantity_column,
                    end_cost_column,
                    interest_rate,
                    consumption_column,  # ИСПРАВЛЕНИЕ ОШИБКИ #1: передаем колонку списания
                    lead_time_days,  # НОВЫЙ ПАРАМЕТР: Lead Time
                    consumption_convention  # НОВЫЙ ПАРАМЕТР: Конвенция знака списания
                )
                st.subheader("Анализ исторических данных")
                st.dataframe(results_df)
                
                # Кнопка скачивания перед пояснением расчетов
                if not results_df.empty:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv_file = utils.to_csv(results_df)
                        st.download_button(
                            label="Скачать таблицу как CSV файл",
                            data=csv_file,
                            file_name="historical_analysis.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        excel_file = utils.to_excel(results_df)
                        st.download_button(
                            label="Скачать таблицу как Excel файл",
                            data=excel_file,
                            file_name="historical_analysis.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                
                st.subheader("Пояснение расчеов")
                st.write(explanation)
                
                log_user_action(
                    action="Анализ исторических данных",
                    message=f"Нажата кнопка 'Провести анализ исторических данных'. Анализ исторических данных успешно выполнен. Использован файл {historical_file.name}. Количество строк: {st.session_state.historical_df.shape[0]}."
                )
            except Exception as e:
                st.error(f"Произошла ошибка при анализе исторических данных: {str(e)}")
                log_user_action(
                    action="Анализ исторических данных",
                    message=f"Произошла ошибка при анализе исторических данных: {str(e)}"
                )

    # Добавим ввод страхового запаса
    safety_stock_percent = st.slider("Выберите процент страхового запаса", 0, 100, 20, 5)
    safety_stock_percent /= 100  # Преобразуем процент в десятичную дробь

    # Загрузка прогнозируемых данных
    st.header("Загрузка прогнозируемых данных")
    forecast_file = st.file_uploader("Выберите Excel фай с прогнозируемыми данными", type=["xlsx"], key="forecast_uploader")

    if forecast_file is not None and st.session_state.get("forecast_df") is None:
        st.session_state.forecast_df = pd.read_excel(forecast_file)
        log_user_action(
            action="Загрузка прогнозируемых данных",
            message=f"Загружен файл {forecast_file.name}. Количество строк: {st.session_state.forecast_df.shape[0]}."
        )
        
    if forecast_file is not None:
        st.session_state.forecast_df = pd.read_excel(forecast_file)
        st.success("Файл с прогнозируемыми данными успешно загружен!")

    if st.session_state.forecast_df is not None:
        st.write("Первые несколько строк загруженных прогнозных данных:")
        st.write(st.session_state.forecast_df.head())

        # Выбор обязательных полей для прогнозируемых данных
        forecast_date_column = st.selectbox("Выберите поле с датой прогноза", st.session_state.forecast_df.columns)
        forecast_branch_column = st.selectbox("Выберите поле с номером филиала (прогноз)", st.session_state.forecast_df.columns)
        forecast_material_column = st.selectbox("Выберите поле с наименованием материала (прогноз)", st.session_state.forecast_df.columns)
        forecast_quantity_column = st.selectbox("Выберите поле с запланированной потребностью", st.session_state.forecast_df.columns)

        # Выбор конкретных значений признаков для прогноза
        selected_forecast_materials = st.multiselect("Выберите материалы для прогноза", st.session_state.forecast_df[forecast_material_column].unique())
        selected_forecast_branches = st.multiselect("Выберите филиалы для прогноза", st.session_state.forecast_df[forecast_branch_column].unique())

        # Фильтрация прогнозных данных по выбранным значениям
        if selected_forecast_materials:
            st.session_state.forecast_df = st.session_state.forecast_df[st.session_state.forecast_df[forecast_material_column].isin(selected_forecast_materials)].reset_index(drop=True)
        if selected_forecast_branches:
            st.session_state.forecast_df = st.session_state.forecast_df[st.session_state.forecast_df[forecast_branch_column].isin(selected_forecast_branches)].reset_index(drop=True)

        # нализ прогнозируемых данных
        if st.button("Провести анализ прогнозируемых данных"):
            try:
                if st.session_state.historical_df is None:
                    st.error("Пожалуйста, загрузите и проанализируйте исторические данные перед анализом прогноза.")
                else:
                    # Прогноз остатков на основе исторических данных
                    st.session_state.forecast_df['Прогноз остатка на начало'] = fa.forecast_start_balance(st.session_state.historical_df, st.session_state.forecast_df, 
                                                                                          date_column, material_column, branch_column, end_quantity_column,
                                                                                          forecast_date_column, forecast_material_column, forecast_branch_column)
                    
                    # Расчет прогнозируемого остатка на конец
                    st.session_state.forecast_df['Прогноз остатка на конец'] = st.session_state.forecast_df['Прогноз остатка на начало'] - st.session_state.forecast_df[forecast_quantity_column]
                    
                    # Рекомендации по закупкам с учетом введенного страхового запаса
                    recommendations_df = fa.calculate_purchase_recommendations(
                        st.session_state.forecast_df, 'Прогноз остатка на конец', forecast_quantity_column, safety_stock_percent
                    )
                    st.session_state.forecast_df = pd.concat([st.session_state.forecast_df, recommendations_df], axis=1)
                    
                    analysis_df, explanation = fa.analyze_forecast_data(
                        st.session_state.forecast_df,
                        forecast_date_column,
                        forecast_material_column,
                        forecast_branch_column,
                        forecast_quantity_column,
                        'Прогноз остатка на начало',
                        'Прогноз остатка на конец',
                        'Рекомендация по закупке',
                        'Будущий спрос',
                        'Страховой запас'
                    )
                    st.subheader("Прогноз остатков и рекомендации по закупкам:")
                    st.dataframe(analysis_df)
                    st.subheader("Пояснение расчетов")
                    st.write(explanation)
                    
                    # Кнопка для скачивания
                    excel_file = utils.to_excel(analysis_df)
                    st.download_button(
                        label="Скачать таблицу как Excel файл",
                        data=excel_file,
                        file_name="forecast_and_recommendations.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                    # Визуализация прогноза
                    forecast_fig = vis.plot_forecast_analysis(analysis_df, forecast_date_column, 
                                                              forecast_material_column, 
                                                              'Прогноз остатка на конец', 'Рекомендация по закупке')
                    st.plotly_chart(forecast_fig)
                    
                    log_user_action(
                        action="Анализ прогнозируемых данных",
                        message=f"Нажата кнопка 'Провести анализ прогнозируемых данных'. Анализ прогнозируемых данных успешно выполнен. Использован файл {forecast_file.name}. Количество строк: {st.session_state.forecast_df.shape[0]}."
                    )
            except Exception as e:
                st.error(f"Произошла ошибка ри анализе прогнозируемых данных: {str(e)}")
                log_user_action(
                    action="Анализ прогнозируемых данных",
                    message=f"Произошла ошибка ри анализе прогнозируемых данных: {str(e)}"
                )
                
    # Кнопка для скачивания лог-файла
    create_private_download_button()

if __name__ == "__main__":
    main()