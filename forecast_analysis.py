import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import plotly.express as px

def analyze_forecast_data(df, date_column, material_column, branch_column, demand_column,
                          start_balance_column, end_balance_column, recommendation_column,
                          future_demand_column, safety_stock_column):
    analysis_df = df.copy()
    numeric_columns = [demand_column, start_balance_column, end_balance_column,
                       recommendation_column, future_demand_column, safety_stock_column]
    analysis_df[numeric_columns] = analysis_df[numeric_columns].round(1)
    analysis_df = analysis_df.sort_values([date_column, material_column, branch_column])

    # ИСПРАВЛЕНИЕ ОШИБКИ #3: УДАЛЕНО применение Exponential Smoothing
    # Причина: Перезапись запланированной потребности некорректна и происходит
    # ПОСЛЕ всех расчетов, что делает предыдущие расчеты бессмысленными.
    # Если нужно сглаживание для визуализации, создайте отдельную колонку.

    explanation = get_explanation(analysis_df.iloc[0], date_column, material_column, branch_column,
                                  demand_column, start_balance_column, end_balance_column,
                                  recommendation_column, future_demand_column, safety_stock_column)

    return analysis_df, explanation

def get_explanation(row, date_column, material_column, branch_column, demand_column, 
                    start_balance_column, end_balance_column, recommendation_column, 
                    future_demand_column, safety_stock_column):
    explanation = f"""
    Пояснение расчетов на примере:
    
    Рассмотрим строку для {row[material_column]} в {row[branch_column]} на дату {row[date_column]}:

    1. **Запланированная потребность**: {row[demand_column]}
       - Это значение берется напрямую из загруженных исходных данных.
       - Что делать: Используйте это значение для планирования закупок на указанную дату, чтобы избежать нехватки материала.

    2. **Прогноз остатка на начало**: {row[start_balance_column]}
       - Рассчитывается на основе исторических данных, предыдущего прогноза или с использованием модели Exponential Smoothing.
       - Модель Exponential Smoothing помогает предсказать, сколько материала останется, учитывая прошлое использование и тренды.
       - Представляет ожидаемый остаток {row[material_column]} в {row[branch_column]} на начало дня {row[date_column]}.
       - Что делать: Сравните этот остаток с запланированной потребностью, чтобы понять, достаточно ли материала.

    3. **Прогноз остатка на конец**: {row[end_balance_column]}
       - Вычисляется как: Прогноз остатка на начало - Запланированная потребность
       - {row[start_balance_column]} - {row[demand_column]} = {row[end_balance_column]}
       - Это ожидаемый остаток {row[material_column]} в {row[branch_column]} в конце дня {row[date_column]} после удовлетворения запланированной потребности.
       - Что делать: Если прогноз остатка на конец слишком мал, подумайте о дополнительных закупках, чтобы избежать нехватки.

    4. **Рекомендация по закупке**: {row[recommendation_column]}
       - Рассчитывается на основе будущего спроса и текущих остатков с учетом страхового запаса.
       - Формула: max(0, Будущий спрос + Страховой запас - Прогноз остатка на конец)
       - max(0, {row[future_demand_column]} + {row[safety_stock_column]} - {row[end_balance_column]}) = {row[recommendation_column]}
       - Что делать: Если значение больше 0, необходимо заказать дополнительное количество материала, чтобы покрыть будущий спрос и избежать нехватки.

    5. **Будущий спрос**: {row[future_demand_column]}
       - Сумма запланированных потребностей за текущий и два следующих периода.
       - Представьте, что вы управляете складом строительных материалов. Будущий спрос — это то, сколько материала вам понадобится в ближайшее время.
       
       Как это работает:
       - Если сегодня понедельник, вы смотрите на потребность в материале на понедельник, вторник и среду.
       - Например, если в понедельник нужно 20 единиц материала, во вторник — 20, а в среду — 14, то будущий спрос составит: 20 + 20 + 14 = 54 единицы.
       
       Зачем это нужно:
       - Знание будущего спроса помогает заранее подготовиться и убедиться, что у вас будет достаточно материала.
       - Это позволяет избежать ситуаций, когда материал неожиданно заканчивается.
       - Помогает планировать закупки и поддерживать оптимальный уровень запасов.
       
       Что делать:
       - Используйте этот показатель для планирования закупок на ближайшее время.
       - Убедитесь, что у вас есть достаточно материала для покрытия будущего спроса.
       - Если текущих запасов недостаточно, рассмотрите возможность дополнительной закупки.
       - Регулярно сравнивайте фактический спрос с прогнозируемым, чтобы улучшать точность прогнозов.

    6. **Страховой запас**: {row[safety_stock_column]}
       - Рассчитывается как процент от запланированной потребности.
       - Помогает обеспечить наличие достаточного количества материала в случае непредвиденных обстоятельств.
       - Что делать: Держите достаточный страховой запас, чтобы избежать перебоев в поставках при внезапном увеличении спроса.

    Эти расчеты помогают оптимизировать управление запасами, обеспечивая достаточное количество материалов 
    для удовлетворения спроса и поддержания страхового запаса, одновременно минимизируя излишки. Это значит, что вы можете сократить излишние расходы и не допустить нехватки.
    """
    return explanation

def forecast_start_balance(historical_df, forecast_df, date_column, material_column, branch_column, end_quantity_column,
                           forecast_date_column, forecast_material_column, forecast_branch_column):
    last_historical_date = historical_df[date_column].max()
    last_balances = historical_df[historical_df[date_column] == last_historical_date][[branch_column, material_column, end_quantity_column]]
    
    forecast_start_balances = forecast_df.merge(last_balances, 
                                                left_on=[forecast_branch_column, forecast_material_column],
                                                right_on=[branch_column, material_column],
                                                how='left')[end_quantity_column]
    return forecast_start_balances

def calculate_forward_rolling_sum(series, window=3):
    """
    Вычисляет rolling sum ВПЕРЕД (текущий + следующие периоды)
    вместо стандартного rolling (текущий + предыдущие периоды)
    """
    result = []
    for i in range(len(series)):
        # Суммируем от текущего до текущего+window (не включая)
        window_sum = series.iloc[i:min(i+window, len(series))].sum()
        result.append(window_sum)
    return pd.Series(result, index=series.index)


def calculate_purchase_recommendations(df, end_quantity_column, forecast_quantity_column, safety_stock_percent):
    safety_stock = df[forecast_quantity_column] * safety_stock_percent

    # ИСПРАВЛЕНИЕ ОШИБКИ #2: Используем forward rolling sum (текущий + 2 следующих)
    # вместо backward rolling sum (текущий + 2 предыдущих)
    future_demand = calculate_forward_rolling_sum(df[forecast_quantity_column], window=3)

    recommendations = np.maximum(0, future_demand + safety_stock - df[end_quantity_column])

    return pd.DataFrame({
        'Рекомендация по закупке': recommendations,
        'Будущий спрос': future_demand,
        'Страховой запас': safety_stock
    })

def analyze_coverage(df, start_quantity_column, forecast_quantity_column):
    total_inventory = df[start_quantity_column].sum()
    total_demand = df[forecast_quantity_column].sum()
    coverage_ratio = total_inventory / total_demand
    
    if coverage_ratio >= 1:
        return f"Текущие запасы покрывают {coverage_ratio:.2f} от запланированной потребности."
    else:
        shortage = total_demand - total_inventory
        return f"Текущих запасов недостаточно. Нехватка составляет {shortage:.0f} единиц."

def plot_top_materials_by_cost(df, material_column, cost_column):
    top_materials = df.groupby(material_column)[cost_column].sum().nlargest(10).reset_index()
    fig = px.bar(top_materials, x=material_column, y=cost_column, title='Топ 10 материалов по стоимости')
    return fig

def analyze_materials(df, material_column, date_column, start_quantity_column, end_quantity_column):
    df['month'] = pd.to_datetime(df[date_column]).dt.month
    df['usage'] = df[start_quantity_column] - df[end_quantity_column]
    
    analysis = df.groupby(material_column).agg({
        'usage': ['mean', 'std'],
        start_quantity_column: 'mean',
        end_quantity_column: 'mean'
    }).reset_index()
    
    analysis.columns = [material_column, 'Среднее использование', 'Стандартное отклонение использования', 
                        'Средний остаток на начало', 'Средний остаток на конец']
    
    analysis['Коэффициент вариации'] = analysis['Стандартное отклонение использования'] / analysis['Среднее использование']
    analysis['Сезонность'] = analysis['Коэффициент вариации'] > 0.5
    
    def get_seasonality_info(material):
        material_data = df[df[material_column] == material]
        monthly_usage = material_data.groupby('month')['usage'].mean()
        high_season = monthly_usage.nlargest(3).index.tolist()
        low_season = monthly_usage.nsmallest(3).index.tolist()
        return f"Высокий сезон: {', '.join(map(str, high_season))}, Низкий сезон: {', '.join(map(str, low_season))}"
    
    analysis['Информация о сезонности'] = analysis.apply(lambda row: get_seasonality_info(row[material_column]) if row['Сезонность'] else "Не сезонный", axis=1)
    analysis['Оборачиваемость'] = analysis['Среднее использование'] / ((analysis['Средний остаток на начало'] + analysis['Средний остаток на конец']) / 2)
    
    analysis['Проблемы с запасом'] = analysis.apply(lambda row: 
        "Излишек" if row['Средний остаток на конец'] > 2 * row['Среднее использование'] 
        else ("Дефицит" if row['Средний остаток на конец'] < 0.5 * row['Среднее использование'] 
              else "Нормальный уровень"), axis=1)
    
    return analysis