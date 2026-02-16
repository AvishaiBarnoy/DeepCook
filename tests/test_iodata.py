"""
Tests for scripts.iodata module, covering data I/O operations.
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.iodata import add_meal, save_data, write_to_log


class TestAddMeal:
    """Tests for the add_meal function."""
    
    @pytest.fixture
    def sample_meals_db(self):
        """Create a sample meal database."""
        data = {
            'Name': ['Pasta', 'Pizza'],
            'Rank': [8, 9],
            'TA': [0, 0],
            'Timestamp': [pd.NaT, pd.NaT],
            'times_made': [0, 1]
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def new_meal(self):
        """Create a new meal to add."""
        data = {
            'Name': ['Salad'],
            'Rank': [7],
            'TA': [0],
            'Timestamp': [pd.NaT],
            'times_made': [0]
        }
        return pd.DataFrame(data)
    
    def test_add_single_meal(self, sample_meals_db, new_meal):
        """Test adding a single meal to the database."""
        result = add_meal(sample_meals_db, new_meal)
        
        assert len(result) == 3
        assert 'Salad' in result['Name'].values
        assert result.iloc[2]['Name'] == 'Salad'
    
    def test_add_meal_preserves_existing(self, sample_meals_db, new_meal):
        """Test that existing meals are preserved when adding new one."""
        result = add_meal(sample_meals_db, new_meal)
        
        assert 'Pasta' in result['Name'].values
        assert 'Pizza' in result['Name'].values
    
    def test_add_multiple_meals(self, sample_meals_db):
        """Test adding multiple meals at once."""
        new_meals = pd.DataFrame({
            'Name': ['Soup', 'Burger'],
            'Rank': [6, 10],
            'TA': [0, 1],
            'Timestamp': [pd.NaT, pd.NaT],
            'times_made': [0, 0]
        })
        
        result = add_meal(sample_meals_db, new_meals)
        
        assert len(result) == 4
        assert 'Soup' in result['Name'].values
        assert 'Burger' in result['Name'].values


class TestSaveData:
    """Tests for the save_data function."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for saving."""
        return pd.DataFrame({
            'Name': ['Pasta', 'Pizza', 'Pasta'],  # Intentional duplicate
            'Rank': [8, 9, 8],
            'TA': [0, 0, 0]
        })
    
    def test_save_data_creates_file(self, sample_data):
        """Test that save_data creates a CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tf:
            temp_path = tf.name
        
        try:
            result = save_data(sample_data, temp_path)
            
            assert result == 0
            assert os.path.exists(temp_path)
            
            # Read back and verify
            loaded = pd.read_csv(temp_path, index_col=0)
            assert len(loaded) >= 2  # Should have at least 2 rows
            assert 'Name' in loaded.columns
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_save_data_overwrites_existing(self, sample_data):
        """Test that save_data overwrites existing files."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tf:
            temp_path = tf.name
            tf.write("old,data\n1,2\n")
        
        try:
            save_data(sample_data, temp_path)
            
            # Read back and verify it's the new data
            loaded = pd.read_csv(temp_path, index_col=0)
            assert 'Name' in loaded.columns
            assert 'old' not in loaded.columns
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestWriteToLog:
    """Tests for the write_to_log function."""
    
    def test_write_to_log_creates_entry(self):
        """Test that write_to_log creates a log entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create data directory
            data_dir = Path(tmpdir) / 'data'
            data_dir.mkdir()
            log_file = data_dir / 'test_meal.log'
            
            # Change to temp directory
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                
                write_to_log('Pasta', logfile='test_meal.log')
                
                assert log_file.exists()
                
                # Read and verify
                with open(log_file, 'r') as f:
                    content = f.read()
                    assert 'Pasta' in content
                    assert ',' in content  # Should have timestamp separator
            finally:
                os.chdir(original_cwd)
    
    def test_write_to_log_appends(self):
        """Test that write_to_log appends to existing log."""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / 'data'
            data_dir.mkdir()
            log_file = data_dir / 'test_meal.log'
            
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                
                # Write first entry
                write_to_log('Pasta', logfile='test_meal.log')
                # Write second entry
                write_to_log('Pizza', logfile='test_meal.log')
                
                # Read and verify both entries exist
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    assert len(lines) == 2
                    assert 'Pasta' in lines[0]
                    assert 'Pizza' in lines[1]
            finally:
                os.chdir(original_cwd)
    
    def test_write_to_log_format(self):
        """Test that log entries have correct format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / 'data'
            data_dir.mkdir()
            log_file = data_dir / 'test_meal.log'
            
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                
                write_to_log('Burger', logfile='test_meal.log')
                
                with open(log_file, 'r') as f:
                    line = f.readline()
                    parts = line.strip().split(',')
                    
                    assert len(parts) == 2
                    assert parts[0] == 'Burger'
                    # parts[1] should be a timestamp, just check it exists
                    assert len(parts[1]) > 0
            finally:
                os.chdir(original_cwd)


class TestEdgeCasesIO:
    """Tests for edge cases in I/O operations."""
    
    def test_add_meal_empty_database(self):
        """Test adding meal to empty database."""
        empty_db = pd.DataFrame(columns=['Name', 'Rank', 'TA', 'Timestamp', 'times_made'])
        new_meal = pd.DataFrame({
            'Name': ['Pasta'],
            'Rank': [8],
            'TA': [0],
            'Timestamp': [pd.NaT],
            'times_made': [0]
        })
        
        result = add_meal(empty_db, new_meal)
        
        assert len(result) == 1
        assert result.iloc[0]['Name'] == 'Pasta'
    
    def test_save_data_empty_dataframe(self):
        """Test saving an empty dataframe."""
        empty_df = pd.DataFrame()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tf:
            temp_path = tf.name
        
        try:
            result = save_data(empty_df, temp_path)
            assert result == 0
            assert os.path.exists(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
