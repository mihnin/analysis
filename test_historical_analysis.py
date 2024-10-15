import unittest
import pandas as pd
from historical_analysis import analyze_historical_data

class TestHistoricalAnalysis(unittest.TestCase):

    def test_analyze_historical_data(self):
        df = pd.DataFrame({
            'date': pd.date_range(start='1/1/2023', periods=3),
            'branch': ['A', 'A', 'B'],
            'material': ['X', 'X', 'Y'],
            'start_quantity': [10, 20, 30],
            'end_quantity': [5, 15, 25],
            'end_cost': [100, 200, 300]
        })
        results_df, explanation = analyze_historical_data(df, 'date', 'branch', 'material', 'start_quantity', 'end_quantity', 'end_cost', 5.0)
        self.assertIsInstance(results_df, pd.DataFrame)
        self.assertIsInstance(explanation, str)

if __name__ == '__main__':
    unittest.main()
