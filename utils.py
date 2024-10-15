import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter

def initialize_session_state():
    if 'historical_df' not in st.session_state:
        st.session_state.historical_df = None
    if 'forecast_df' not in st.session_state:
        st.session_state.forecast_df = None
    if 'selected_materials' not in st.session_state:
        st.session_state.selected_materials = []
    if 'selected_branches' not in st.session_state:
        st.session_state.selected_branches = []
    if 'selected_forecast_materials' not in st.session_state:
        st.session_state.selected_forecast_materials = []
    if 'selected_forecast_branches' not in st.session_state:
        st.session_state.selected_forecast_branches = []
    if 'safety_stock_percent' not in st.session_state:
        st.session_state.safety_stock_percent = 20
    if 'start_date' not in st.session_state:
        st.session_state.start_date = None
    if 'end_date' not in st.session_state:
        st.session_state.end_date = None

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def to_csv(df):
    return df.to_csv(index=False, encoding='utf-16').encode('utf-16')

def load_data(file_uploader, key):
    uploaded_file = file_uploader(f"Выберите Excel файл с {key} данными", type=["xlsx"], key=f"{key}_uploader")
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state[f"{key}_df"] = df
            st.success(f"{key.capitalize()} данные успешно загружены!")
            return df
        except Exception as e:
            st.error(f"Ошибка при загрузке {key} данных: {str(e)}")
    return None

def select_columns(df, key):
    st.subheader(f"Выберите столбцы для {key} данных")
    columns = df.columns.tolist()
    
    date_column = st.selectbox(f"Выберите столбец с датой для {key} данных", columns, key=f"{key}_date_column")
    material_column = st.selectbox(f"Выберите столбец с материалом для {key} данных", columns, key=f"{key}_material_column")
    branch_column = st.selectbox(f"Выберите столбец с филиалом для {key} данных", columns, key=f"{key}_branch_column")
    
    if key == "historical":
        start_quantity_column = st.selectbox("Выберите ст��лбец с начальным количеством", columns, key="start_quantity_column")
        end_quantity_column = st.selectbox("Выберите столбец с конечным количеством", columns, key="end_quantity_column")
        return date_column, material_column, branch_column, start_quantity_column, end_quantity_column
    else:
        quantity_column = st.selectbox("Выберите столбец с прогнозируемым количеством", columns, key="forecast_quantity_column")
        return date_column, material_column, branch_column, quantity_column

def filter_data(df, date_column, material_column, branch_column, key):
    st.subheader(f"Фильтрация {key} данных")
    
    # Фильтрация по материалам
    all_materials = df[material_column].unique().tolist()
    selected_materials = st.multiselect(f"Выберите материалы для анализа {key} данных", all_materials, key=f"{key}_materials")
    
    # Фильтрация о филиалам
    all_branches = df[branch_column].unique().tolist()
    selected_branches = st.multiselect(f"Выберите филиалы для анализа {key} данных", all_branches, key=f"{key}_branches")
    
    # Фильтрация по датам
    min_date = df[date_column].min().date()
    max_date = df[date_column].max().date()
    start_date = st.date_input(f"Выберите начальную дату для {key} данных", min_date, key=f"{key}_start_date")
    end_date = st.date_input(f"Выберите конечную дату для {key} данных", max_date, key=f"{key}_end_date")
    
    # Применение фильтров
    filtered_df = df.copy()
    if selected_materials:
        filtered_df = filtered_df[filtered_df[material_column].isin(selected_materials)]
    if selected_branches:
        filtered_df = filtered_df[filtered_df[branch_column].isin(selected_branches)]
    filtered_df = filtered_df[
        (pd.to_datetime(filtered_df[date_column]).dt.date >= start_date) & 
        (pd.to_datetime(filtered_df[date_column]).dt.date <= end_date)
    ]
    
    return filtered_df

def set_safety_stock():
    st.session_state.safety_stock_percent = st.slider("Выберите процент страхового запаса", 0, 100, st.session_state.safety_stock_percent, 5)
    return st.session_state.safety_stock_percent / 100
