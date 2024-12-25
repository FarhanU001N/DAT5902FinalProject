import unittest
import pandas as pd
import numpy as np
from io import StringIO

# Import the function to be tested
from datafunctions import read_format_join

class TestReadFormatJoin(unittest.TestCase):
    def setUp(self):
        # Mock CSV data for testing
        self.csv1 = StringIO("""
        entity,day,vaccines
        Region A,2024-01-01,1000
        Region B,2024-01-02,1500
        Region C,2024-01-03,2000
        """)
        
        self.csv2 = StringIO("""
        entity,day,cases
        Region A,2024-01-01,50
        Region B,2024-01-02,60
        Region C,2024-01-03,70
        """)

    def test_read_format_join(self):
        # Read and merge using the function
        result = read_format_join(self.csv1, self.csv2)
        
        # Expected DataFrame
        expected_data = {
            'entity': ['Region A', 'Region B', 'Region C'],
            'day': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'vaccines': [1000, 1500, 2000],
            'cases': [50, 60, 70]
        }
        expected_df = pd.DataFrame(expected_data)
        
        # Assert the DataFrame is as expected
        self.assertEqual(result, expected_df)

if __name__ == '__main__':
    unittest.main()
