"""Analysis modules for inventory management"""
from .historical_analysis import analyze_historical_data
from .forecast_analysis import analyze_forecast_data, forecast_start_balance, calculate_purchase_recommendations, auto_forecast_demand
from .forecasting_models import forecast_demand, auto_select_best_model

__all__ = [
    'analyze_historical_data',
    'analyze_forecast_data',
    'forecast_start_balance',
    'calculate_purchase_recommendations',
    'auto_forecast_demand',
    'forecast_demand',
    'auto_select_best_model',
]
