import unittest
import pandas as pd
import numpy as np
from app import to_excel, main

class TestApp(unittest.TestCase):

    def test_to_excel(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        excel_data = to_excel(df)
        self.assertIsInstance(excel_data, bytes)

    def test_main(self):
        # This is a placeholder test. You can add more specific tests if needed.
        self.assertIsNone(main())

if __name__ == '__main__':
    unittest.main()
