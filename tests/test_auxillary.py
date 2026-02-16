"""
Tests for scripts.auxillary module, focusing on the core meal selection logic.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.auxillary import choose_random, is_too_late_to_cook, make_this_meal


class TestChooseRandom:
    """Tests for the choose_random function."""
    
    @pytest.fixture
    def sample_meals_db(self):
        """Create a sample meal database for testing."""
        data = {
            'Name': ['Pasta', 'Pizza', 'Salad', 'Soup', 'Burger'],
            'Name_he': ['פסטה', 'פיצה', 'סלט', 'מרק', 'המבורגר'],
            'Rank': [8, 9, 6, 7, 10],
            'Kosher': ['parve', 'milchik', 'parve', 'parve', 'fleisch'],
            'Prep_Time': ['short', 'long', 'short', 'medium', 'short'],
            'Cook_Time': ['medium', 'long', 'short', 'long', 'short'],
            'prep_ease': ['easy', 'medium', 'easy', 'easy', 'easy'],
            'scaling': [1.0, 1.0, 1.0, 1.0, 1.0],
            'TA': [0, 0, 0, 0, 1],
            'Timestamp': [
                pd.NaT,  # Never made
                (pd.Timestamp.now() - pd.Timedelta(days=2)).date(),  # 2 days ago
                (pd.Timestamp.now() - pd.Timedelta(days=5)).date(),  # 5 days ago
                pd.NaT,  # Never made
                (pd.Timestamp.now() - pd.Timedelta(days=1)).date(),  # 1 day ago
            ],
            'times_made': [0, 3, 2, 0, 5],
            'recipe_suggestion': [np.nan, 'http://example.com/pizza', np.nan, np.nan, np.nan]
        }
        return pd.DataFrame(data)
    
    def test_basic_random_selection(self, sample_meals_db):
        """Test basic random meal selection without filters."""
        meals, chosen_name, chosen_idx = choose_random(sample_meals_db, k=1)
        
        assert isinstance(chosen_name, str)
        assert chosen_name in sample_meals_db['Name'].values
        assert chosen_idx in sample_meals_db.index
    
    def test_last_made_filter_excludes_recent(self, sample_meals_db):
        """Test that last_made filter excludes recently made meals."""
        # Filter meals made in last 3 days (should exclude Pizza and Burger)
        meals, chosen_name, chosen_idx = choose_random(
            sample_meals_db, 
            last_made=3,
            k=1
        )
        
        # Should only choose from: Pasta (never), Salad (5 days ago), Soup (never)
        assert chosen_name in ['Pasta', 'Salad', 'Soup']
        assert chosen_name not in ['Pizza', 'Burger']
    
    def test_last_made_zero_no_filtering(self, sample_meals_db):
        """Test that last_made=0 doesn't filter any meals."""
        meals, chosen_name, chosen_idx = choose_random(
            sample_meals_db,
            last_made=0,
            k=1
        )
        
        # Could be any meal
        assert chosen_name in sample_meals_db['Name'].values
    
    def test_last_made_includes_never_made(self, sample_meals_db):
        """Test that meals with NaT timestamps are always included."""
        # Even with very strict filter, never-made meals should be available
        meals, chosen_name, chosen_idx = choose_random(
            sample_meals_db,
            last_made=1000,  # Very long period
            k=1
        )
        
        # Should choose from never-made meals: Pasta or Soup
        assert chosen_name in ['Pasta', 'Soup']
    
    def test_last_made_fallback_when_all_filtered(self):
        """Test fallback when all meals are filtered out."""
        # Create DB where all meals were made today
        today = pd.Timestamp.now().date()
        data = {
            'Name': ['Pasta', 'Pizza'],
            'Name_he': ['פסטה', 'פיצה'],
            'Rank': [8, 9],
            'Kosher': ['parve', 'milchik'],
            'Prep_Time': ['short', 'long'],
            'Cook_Time': ['medium', 'long'],
            'prep_ease': ['easy', 'medium'],
            'scaling': [1.0, 1.0],
            'TA': [0, 0],
            'Timestamp': [today, today],
            'times_made': [1, 1],
            'recipe_suggestion': [np.nan, np.nan]
        }
        meals_db = pd.DataFrame(data)
        
        # Try to filter with last_made=1 (should trigger fallback)
        meals, chosen_name, chosen_idx = choose_random(
            meals_db,
            last_made=1,
            k=1
        )
        
        # Should still return a meal (fallback behavior)
        assert chosen_name in ['Pasta', 'Pizza']
    
    def test_ta_filter_only_takeaway(self, sample_meals_db):
        """Test filtering to only show take-away meals."""
        meals, chosen_name, chosen_idx = choose_random(
            sample_meals_db,
            TA=True,
            k=1
        )
        
        # Should only choose Burger (TA=1)
        assert chosen_name == 'Burger'
    
    def test_ta_filter_exclude_takeaway(self, sample_meals_db):
        """Test filtering to exclude take-away meals."""
        meals, chosen_name, chosen_idx = choose_random(
            sample_meals_db,
            TA=False,
            k=1
        )
        
        # Should not choose Burger
        assert chosen_name != 'Burger'
        assert chosen_name in ['Pasta', 'Pizza', 'Salad', 'Soup']
    
    def test_combined_filters(self, sample_meals_db):
        """Test combining last_made and TA filters."""
        meals, chosen_name, chosen_idx = choose_random(
            sample_meals_db,
            last_made=3,
            TA=False,
            k=1
        )
        
        # Should exclude: Pizza (2 days ago), Burger (TA=1, 1 day ago)
        # Should choose from: Pasta (never, TA=0), Salad (5 days, TA=0), Soup (never, TA=0)
        assert chosen_name in ['Pasta', 'Salad', 'Soup']


class TestIsTooLateToCook:
    """Tests for the is_too_late_to_cook function."""
    
    def test_before_cutoff(self, monkeypatch):
        """Test that returns False before cutoff time."""
        # Mock time to 15:00 (3 PM)
        class MockDateTime:
            @staticmethod
            def now():
                class MockTimestamp:
                    hour = 15
                return MockTimestamp()
        
        monkeypatch.setattr(pd, 'Timestamp', MockDateTime)
        
        result = is_too_late_to_cook(cutoff=20)
        assert result is False
    
    def test_after_cutoff(self, monkeypatch):
        """Test that returns True after cutoff time."""
        # Mock time to 21:00 (9 PM)
        class MockDateTime:
            @staticmethod
            def now():
                class MockTimestamp:
                    hour = 21
                return MockTimestamp()
        
        monkeypatch.setattr(pd, 'Timestamp', MockDateTime)
        
        result = is_too_late_to_cook(cutoff=20)
        assert result is True
    
    def test_midnight_cooking(self, monkeypatch):
        """Test that cooking after midnight but before 5 AM returns True (too late)."""
        # Mock time to 02:00 (2 AM)
        class MockDateTime:
            @staticmethod
            def now():
                class MockTimestamp:
                    hour = 2
                return MockTimestamp()
        
        monkeypatch.setattr(pd, 'Timestamp', MockDateTime)
        
        # After bug fix: hour < 5 is checked first, so returns True (too late to cook)
        result = is_too_late_to_cook(cutoff=20)
        assert result is True


class TestMakeThisMeal:
    """Tests for the make_this_meal function."""
    
    @pytest.fixture
    def sample_meals_for_logging(self):
        """Create a sample meal database for logging tests."""
        data = {
            'Name': ['Pasta', 'Pizza'],
            'Rank': [8, 9],
            'Timestamp': [pd.NaT, pd.NaT],
            'times_made': [0, 0]
        }
        return pd.DataFrame(data)
    
    def test_make_meal_yes(self, sample_meals_for_logging, monkeypatch):
        """Test logging a meal when user says yes."""
        # Mock user input to return 'y'
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        
        initial_times = sample_meals_for_logging.loc[0, 'times_made']
        result = make_this_meal(sample_meals_for_logging, 0)
        
        assert result is True
        assert sample_meals_for_logging.loc[0, 'times_made'] == initial_times + 1
        assert sample_meals_for_logging.loc[0, 'Timestamp'] == pd.Timestamp.now().date()
    
    def test_make_meal_no(self, sample_meals_for_logging, monkeypatch):
        """Test not logging a meal when user says no."""
        # Mock user input to return 'n'
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        
        initial_times = sample_meals_for_logging.loc[0, 'times_made']
        result = make_this_meal(sample_meals_for_logging, 0)
        
        assert result is False
        assert sample_meals_for_logging.loc[0, 'times_made'] == initial_times
        assert pd.isna(sample_meals_for_logging.loc[0, 'Timestamp'])
    
    def test_make_meal_invalid_then_yes(self, sample_meals_for_logging, monkeypatch):
        """Test that invalid input prompts again."""
        inputs = iter(['maybe', 'sure', 'y'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        result = make_this_meal(sample_meals_for_logging, 0)
        
        assert result is True
        assert sample_meals_for_logging.loc[0, 'times_made'] == 1


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_empty_database(self):
        """Test handling of empty meal database."""
        empty_db = pd.DataFrame(columns=[
            'Name', 'Name_he', 'Rank', 'Kosher', 'Prep_Time', 'Cook_Time',
            'prep_ease', 'scaling', 'TA', 'Timestamp', 'times_made', 'recipe_suggestion'
        ])
        
        with pytest.raises(ValueError):
            choose_random(empty_db, k=1)
    
    def test_single_meal(self):
        """Test with database containing only one meal."""
        data = {
            'Name': ['Only Meal'],
            'Name_he': ['ארוחה יחידה'],
            'Rank': [10],
            'Kosher': ['parve'],
            'Prep_Time': ['short'],
            'Cook_Time': ['short'],
            'prep_ease': ['easy'],
            'scaling': [1.0],
            'TA': [0],
            'Timestamp': [pd.NaT],
            'times_made': [0],
            'recipe_suggestion': [np.nan]
        }
        meals_db = pd.DataFrame(data)
        
        meals, chosen_name, chosen_idx = choose_random(meals_db, k=1)
        
        assert chosen_name == 'Only Meal'
        assert chosen_idx == 0
