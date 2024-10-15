import unittest
import pandas as pd
from forecast_analysis import analyze_forecast_data, forecast_start_balance, calculate_purchase_recommendations

class TestForecastAnalysis(unittest.TestCase):

    def test_analyze_forecast_data(self):
        df = pd.DataFrame({
            'date': pd.date_range(start='1/1/2023', periods=3),
            'material': ['A', 'A', 'B'],
            'branch': ['X', 'X', 'Y'],
            'demand': [10, 20, 30],
            'start_balance': [5, 15, 25],
            'end_balance': [0, 10, 20],
            'recommendation': [5, 10, 15],
            'future_demand': [15, 25, 35],
            'safety_stock': [2, 3, 4]
        })
        analysis_df, explanation = analyze_forecast_data(df, 'date', 'material', 'branch', 'demand', 'start_balance', 'end_balance', 'recommendation', 'future_demand', 'safety_stock')
        self.assertIsInstance(analysis_df, pd.DataFrame)
        self.assertIsInstance(explanation, str)

    def test_forecast_start_balance(self):
        historical_df = pd.DataFrame({
            'date': pd.date_range(start='1/1/2023', periods=3),
            'branch': ['A', 'A', 'B'],
            'material': ['X', 'X', 'Y'],
            'end_quantity': [10, 20, 30]
        })
        forecast_df = pd.DataFrame({
            'date': pd.date_range(start='1/1/2023', periods=3),
            'branch': ['A', 'A', 'B'],
            'material': ['X', 'X', 'Y']
        })
        start_balances = forecast_start_balance(historical_df, forecast_df, 'date', 'material', 'branch', 'end_quantity', 'date', 'material', 'branch')
        self.assertEqual(start_balances.tolist(), [20, 20, 30])

    def test_calculate_purchase_recommendations(self):
        df = pd.DataFrame({
            'end_quantity': [10, 20, 30],
            'forecast_quantity': [5, 15, 25]
        })
        recommendations_df = calculate_purchase_recommendations(df, 'end_quantity', 'forecast_quantity', 0.2)
        self.assertEqual(recommendations_df['Рекомендация по закупке'].tolist(), [0, 0, 0])

if __name__ == '__main__':
    unittest.main()
