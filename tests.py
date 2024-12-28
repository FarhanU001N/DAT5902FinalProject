import unittest
import pandas as pd
import numpy as np
from io import StringIO

# Import the function to be tested
from datafunctions import format_join

class TestReadFormatJoin(unittest.TestCase):
    def setUp(self):
        # Mock CSV data for testing
        self.csv1 = pd.DataFrame({
        "Entity": ["Region A", "Region B", "Region C"],
        "Day": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "vaccines": [1000, 1500, 2000]
        })
        
        self.csv2 = pd.DataFrame({
        "Entity": ["Region A", "Region B", "Region C"],
        "Day": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "cases": [50, 60, 70]
        })

    def test_format_join(self):
        # Read and merge using the function
        result = format_join(self.csv1, self.csv2)
        
        # Expected DataFrame
        expected_data = {
            'Entity': ['Region A', 'Region B', 'Region C'],
            'Day': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'vaccines': [1000, 1500, 2000],
            'cases': [50, 60, 70]
        }
        expected_df = pd.DataFrame(expected_data)
        
        # Assert the DataFrame is as expected
        self.assertEqual(result.equals(expected_df),True)

if __name__ == '__main__':
    unittest.main()
