import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_inventory_trend(df, date_column, start_quantity_column, end_quantity_column):
    df['average_quantity'] = (df[start_quantity_column] + df[end_quantity_column]) / 2
    fig = px.line(df, x=date_column, y='average_quantity', title='Тренд запасов')
    return fig

def plot_seasonality(df, date_column, quantity_column):
    df['month'] = pd.to_datetime(df[date_column]).dt.month
    monthly_avg = df.groupby('month')[quantity_column].mean().reset_index()
    fig = px.bar(monthly_avg, x='month', y=quantity_column, title='Сезонность запасов')
    return fig

def plot_forecast_analysis(df, date_column, material_column, end_quantity_column, purchase_recommendation_column):
    fig = go.Figure()
    for material in df[material_column].unique():
        material_df = df[df[material_column] == material]
        fig.add_trace(go.Scatter(x=material_df[date_column], y=material_df[end_quantity_column],
                                 mode='lines+markers', name=f'{material} - Остаток'))
        fig.add_trace(go.Bar(x=material_df[date_column], y=material_df[purchase_recommendation_column],
                             name=f'{material} - Рекомендация по закупке'))
    fig.update_layout(title='Прогноз остатков и рекомендации по закупкам', xaxis_title='Дата', yaxis_title='Количество')
    return fig