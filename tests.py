import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch
# Import the function to be tested
from datafunctions import format_join
from models import trend_analysis
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
class TestTrendAnalysis(unittest.TestCase):
    def setUp(self):
        """Set up sample data for testing."""
        self.data = pd.DataFrame({
            'Day': pd.date_range(start='2021-01-01', periods=10),
            'Region': ['Africa', 'Asia', 'North America', 'South America', 'Europe',
                       'Oceania', 'Antarctica', 'Africa', 'Asia', 'Europe'],
            'Cases': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
            'Vaccines': [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
        })

    @patch("matplotlib.pyplot.show")
    def test_trend_analysis(self, mock_show):
        """Test trend_analysis with valid input data."""
        # Call the function
        trend_analysis(self.data)
        
        # Check that plt.show() was called 5 times (once for each region in selected_regions)
        self.assertEqual(mock_show.call_count, 5)

        # Validate filtering: Only selected_regions should remain
        selected_regions = ['Africa', 'Asia', 'North America', 'South America', 'Europe']
        filtered_data = self.data[self.data['Region'].isin(selected_regions)]
        self.assertEqual(len(filtered_data), 8)  # Count of rows matching selected regions

    def test_trend_analysis_empty(self):
        """Test trend_analysis with an empty DataFrame."""
        empty_data = pd.DataFrame(columns=['Day', 'Region', 'Cases', 'Vaccines'])
        
        # Check that it runs without error
        with patch("matplotlib.pyplot.show") as mock_show:
            trend_analysis(empty_data)
            mock_show.assert_not_called()  # No plots should be shown

    def test_trend_analysis_missing_columns(self):
        """Test trend_analysis with missing columns."""
        incomplete_data = pd.DataFrame({
            'Day': pd.date_range(start='2021-01-01', periods=10),
            'Region': ['Africa'] * 10,
            'Cases': [100] * 10
        })
        
        with self.assertRaises(KeyError):
            trend_analysis(incomplete_data)  # Should raise KeyError due to missing 'Vaccines' column

if __name__ == '__main__':
    unittest.main()
