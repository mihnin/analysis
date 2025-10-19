"""Analysis modules for inventory management"""
from .historical_analysis import analyze_historical_data
from .historical_analysis import get_explanation as get_historical_explanation
from .forecast_analysis import analyze_forecast_data, forecast_start_balance, calculate_purchase_recommendations, auto_forecast_demand
from .forecast_analysis import get_explanation as get_forecast_explanation
from .forecasting_models import forecast_demand, auto_select_best_model

__all__ = [
    'analyze_historical_data',
    'get_historical_explanation',
    'analyze_forecast_data',
    'get_forecast_explanation',
    'forecast_start_balance',
    'calculate_purchase_recommendations',
    'auto_forecast_demand',
    'forecast_demand',
    'auto_select_best_model',
]
