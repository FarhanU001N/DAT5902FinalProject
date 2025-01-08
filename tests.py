import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch
import os
import glob
# Import the function to be tested
from datafunction import format_join
from models import trend_analysis,lag_analysis_region,lagged_effect_analysis
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
        folder_path = 'visualisations'
        if os.path.exists(folder_path):
            files = glob.glob(f"{folder_path}/*")
            for file in files:
                os.remove(file)
        else:
            os.makedirs(folder_path)
    
    def test_trend_analysis(self):
        """Test trend_analysis with valid input data."""
        # Call the function
        trend_analysis(self.data)
        selected_regions = ['Africa', 'Asia', 'North America', 'South America', 'Europe']
        for region in selected_regions:
            file_path = f"visualisations/{region}_trend_analysis.png"
            self.assertTrue(os.path.exists(file_path))

    def test_trend_analysis_empty(self):
        """Test trend_analysis with an empty DataFrame."""
        empty_data = pd.DataFrame(columns=['Day', 'Region', 'Cases', 'Vaccines'])
        trend_analysis(empty_data)
        # Ensure no files are created
        files = os.listdir("visualisations")
        self.assertEqual(len(files), 0)

    def test_trend_analysis_missing_columns(self):
        """Test trend_analysis with missing columns."""
        incomplete_data = pd.DataFrame({
            'Day': pd.date_range(start='2021-01-01', periods=10),
            'Region': ['Africa'] * 10,
            'Cases': [100] * 10
        })
        
        with self.assertRaises(KeyError):
            trend_analysis(incomplete_data)  # Should raise KeyError due to missing 'Vaccines' column
class TestLagAnalysisRegion(unittest.TestCase):
    def setUp(self):
        os.makedirs("visualisations", exist_ok=True)
        """Set up sample data for testing."""
        self.data = pd.DataFrame({
            'Day': pd.date_range(start='2021-01-01', periods=60),
            'Region': ['Africa'] * 30 + ['Asia'] * 30,
            'Vaccines': list(range(1, 31)) * 2,
            'Cases': list(range(1, 31)) * 2
        })

    def test_lag_analysis_region_default(self):
        """Test lag_analysis_region with default parameters."""
        lag_analysis_region(self.data)
        file_path = "visualisations/lag_analysis.png"
        self.assertTrue(os.path.exists(file_path))

    def test_lag_analysis_region_custom_regions(self):
        """Test lag_analysis_region with custom selected regions."""
        selected_regions = ['Africa']
        result = lag_analysis_region(self.data, selected_regions=selected_regions)
        self.assertIn('Africa', result)
        self.assertNotIn('Asia', result)

    def test_lag_analysis_region_empty_data(self):
        """Test lag_analysis_region with an empty DataFrame."""
        empty_data = pd.DataFrame(columns=['Day', 'Region', 'Vaccines', 'Cases'])
        result = lag_analysis_region(empty_data)
        self.assertEqual(result, {})  # Should return an empty dictionary

    def test_lag_analysis_region_partial_overlap(self):
        """Test lag_analysis_region when lag exceeds available data."""
        # Modify data to create a shorter time series
        data_short = self.data[self.data['Region'] == 'Africa'].iloc[:10]  # Only 10 days
        result = lag_analysis_region(data_short, selected_regions=['Africa'], max_lag_months=5)
        
        self.assertEqual(len(result['Africa']), 6)  # Lags 0 through 5
        self.assertTrue(np.isnan(result['Africa'][-1]))  # The last lag should be NaN due to insufficient data

    def test_lag_analysis_region_missing_columns(self):
        """Test lag_analysis_region with missing columns."""
        incomplete_data = pd.DataFrame({
            'Day': pd.date_range(start='2021-01-01', periods=10),
            'Region': ['Africa'] * 10,
            'Vaccines': list(range(1, 11))
        })
        
        with self.assertRaises(KeyError):
            lag_analysis_region(incomplete_data)  # Should raise KeyError due to missing 'Cases'
class TestLaggedEffectAnalysis(unittest.TestCase):
    def setUp(self):
        os.makedirs("visualisations", exist_ok=True)
    
    def test_valid_data(self):
        # Create a sample DataFrame
        data = pd.DataFrame({
            'Day': pd.date_range(start='2021-01-01', periods=60),
            'Region': ['Africa'] * 30 + ['Asia'] * 30,
            'Vaccines': list(range(1, 31)) * 2,
            'Cases': list(range(1, 31)) * 2
        })
        result = lagged_effect_analysis(data, lag_weeks=1)
        file_path = "visualisations/lag_effect_analysis.png"
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(result)
    
    
    def test_empty_data_after_filtering(self):
        data = pd.DataFrame({
            'Region': ['Unknown', 'Unknown'],
            'Day': ['2025-01-01', '2025-01-02'],
            'Cases': [100, 200],
            'Vaccines': [10, 20]
        })

        # Call the function with test data
        result = lagged_effect_analysis(data, lag_weeks=1)

        # Assert the function returned None
        self.assertIsNone(result)

    def test_no_lag_cases(self):
        # Create data with insufficient lagged rows
        data = pd.DataFrame({
            'Region': ['Africa', 'Africa'],
            'Day': ['2025-01-01', '2025-01-02'],
            'Cases': [100, 200],
            'Vaccines': [10, 20]
        })

        # Call the function with a large lag_weeks value
        result = lagged_effect_analysis(data, lag_weeks=1000)
        
        # Expect the function to return None
        self.assertIsNone(result)
if __name__ == '__main__':
    unittest.main()
