import unittest
import pandas as pd
from utils import to_excel, to_csv

class TestUtils(unittest.TestCase):

    def test_to_excel(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        excel_data = to_excel(df)
        self.assertIsInstance(excel_data, bytes)

    def test_to_csv(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        csv_data = to_csv(df)
        self.assertIsInstance(csv_data, bytes)

if __name__ == '__main__':
    unittest.main()
