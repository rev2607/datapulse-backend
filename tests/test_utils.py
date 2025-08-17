import pytest
import pandas as pd
import numpy as np
from app.utils import analyze_csv, detect_outliers_iqr, detect_outliers_iforest, calculate_psi, drift_check

class TestUtils:
    """Test class for utility functions"""
    
    def test_analyze_csv_basic(self):
        """Test basic CSV analysis functionality"""
        # Create test DataFrame
        df = pd.DataFrame({
            'name': ['John', 'Jane', 'Bob'],
            'age': [25, 30, 35],
            'salary': [50000, 60000, 70000]
        })
        
        results = analyze_csv(df)
        
        assert 'schema' in results
        assert 'summary' in results
        assert 'missing' in results
        assert 'health_score' in results
        assert 'outliers_iqr' in results
        assert 'outliers_iforest' in results
        assert 'drift' in results
        assert results['schema']['name'] == 'object'
        assert results['schema']['age'] == 'int64'
        assert results['schema']['salary'] == 'int64'
        assert results['missing']['name'] == 0
        assert results['missing']['age'] == 0
        assert results['missing']['salary'] == 0
        assert results['health_score'] == 100.0
        
    def test_analyze_csv_with_missing_values(self):
        """Test CSV analysis with missing values"""
        df = pd.DataFrame({
            'name': ['John', 'Jane', None],
            'age': [25, None, 35],
            'salary': [50000, 60000, None]
        })
        
        results = analyze_csv(df)
        
        assert results['missing']['name'] == 1
        assert results['missing']['age'] == 1
        assert results['missing']['salary'] == 1
        # With 3 missing values out of 9 total cells, health score should be 66.67
        assert results['health_score'] == 66.67
        
    def test_detect_outliers_iqr(self):
        """Test IQR outlier detection"""
        df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45, 100],  # 100 is an outlier
            'salary': [50000, 60000, 70000, 80000, 90000, 200000]  # 200000 is an outlier
        })
        
        outliers = detect_outliers_iqr(df)
        
        assert 'age' in outliers
        assert 'salary' in outliers
        assert outliers['age'] >= 1  # Should detect at least one outlier
        assert outliers['salary'] >= 1  # Should detect at least one outlier
        
    def test_detect_outliers_iforest(self):
        """Test Isolation Forest outlier detection"""
        df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45, 100],
            'salary': [50000, 60000, 70000, 80000, 90000, 200000]
        })
        
        outliers = detect_outliers_iforest(df)
        
        assert 'outlier_count' in outliers
        assert outliers['outlier_count'] >= 0
        
    def test_calculate_psi(self):
        """Test PSI calculation"""
        expected = pd.Series([1, 2, 3, 4, 5] * 20)  # 100 values
        actual = pd.Series([1, 2, 3, 4, 5] * 20)    # Same distribution
        
        psi = calculate_psi(expected, actual)
        
        assert isinstance(psi, (int, float))
        assert psi >= 0  # PSI should be non-negative
        
    def test_drift_check(self):
        """Test drift checking between two DataFrames"""
        old_df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45] * 20,
            'salary': [50000, 60000, 70000, 80000, 90000] * 20
        })
        
        new_df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45] * 20,  # Same distribution
            'salary': [50000, 60000, 70000, 80000, 90000] * 20
        })
        
        drift = drift_check(old_df, new_df)
        
        assert 'age' in drift
        assert 'salary' in drift
        assert isinstance(drift['age'], (int, float))
        assert isinstance(drift['salary'], (int, float))
        
    def test_analyze_csv_with_previous_data(self):
        """Test CSV analysis with previous data for drift detection"""
        current_df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000]
        })
        
        previous_df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000]
        })
        
        results = analyze_csv(current_df, previous_df)
        
        assert 'drift' in results
        assert results['drift'] is not None
        assert 'age' in results['drift']
        assert 'salary' in results['drift']
        
    def test_analyze_csv_empty_dataframe(self):
        """Test CSV analysis with empty DataFrame"""
        df = pd.DataFrame()
        
        results = analyze_csv(df)
        
        assert results['schema'] == {}
        assert results['summary'] == {}
        assert results['missing'] == {}
        assert results['health_score'] == 100.0
        assert results['outliers_iqr'] == {}
        assert results['outliers_iforest'] == {}
        assert results['drift'] is None
        
    def test_analyze_csv_no_numerical_columns(self):
        """Test CSV analysis with only categorical columns"""
        df = pd.DataFrame({
            'name': ['John', 'Jane', 'Bob'],
            'city': ['NYC', 'LA', 'Chicago']
        })
        
        results = analyze_csv(df)
        
        assert results['outliers_iqr'] == {}
        assert results['outliers_iforest'] == {}
        
if __name__ == "__main__":
    pytest.main([__file__])
