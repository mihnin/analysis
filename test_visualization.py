import unittest
import pandas as pd
from visualization import plot_inventory_trend, plot_seasonality, plot_forecast_analysis

class TestVisualization(unittest.TestCase):

    def test_plot_inventory_trend(self):
        df = pd.DataFrame({
            'date': pd.date_range(start='1/1/2023', periods=3),
            'start_quantity': [10, 20, 30],
            'end_quantity': [5, 15, 25]
        })
        fig = plot_inventory_trend(df, 'date', 'start_quantity', 'end_quantity')
        self.assertIsNotNone(fig)

    def test_plot_seasonality(self):
        df = pd.DataFrame({
            'date': pd.date_range(start='1/1/2023', periods=12),
            'quantity': range(12)
        })
        fig = plot_seasonality(df, 'date', 'quantity')
        self.assertIsNotNone(fig)

    def test_plot_forecast_analysis(self):
        df = pd.DataFrame({
            'date': pd.date_range(start='1/1/2023', periods=3),
            'material': ['A', 'A', 'B'],
            'end_quantity': [10, 20, 30],
            'purchase_recommendation': [5, 15, 25]
        })
        fig = plot_forecast_analysis(df, 'date', 'material', 'end_quantity', 'purchase_recommendation')
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()
