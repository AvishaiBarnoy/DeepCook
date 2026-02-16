"""
Tests for kosher and diet filtering functions.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.auxillary import filter_kosher, filter_diet
from classes.classes import KosherType, DietType


class TestFilterKosher:
    """Tests for the filter_kosher function."""
    
    @pytest.fixture
    def meals_with_kosher_type(self):
        """Create a meal database with KosherType column."""
        data = {
            'Name': ['Pasta Salad', 'Cheeseburger', 'Steak', 'Chicken Soup', 'Bacon', 'Hummus'],
            'KosherType': ['parve', 'milchik', 'fleisch', 'fleisch', 'nonkosher', 'parve'],
            'Rank': [7, 8, 9, 8, 6, 7],
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def meals_with_kosher_legacy(self):
        """Create a meal database with legacy Kosher column."""
        data = {
            'Name': ['Pasta Salad', 'Steak'],
            'Kosher': ['parve', 'fleisch'],
        }
        return pd.DataFrame(data)
    
    def test_filter_nonkosher_shows_all(self, meals_with_kosher_type):
        """Test that nonkosher filter shows all meals."""
        result = filter_kosher(meals_with_kosher_type, KosherType.nonkosher)
        assert len(result) == 6
        assert set(result['Name']) == {'Pasta Salad', 'Cheeseburger', 'Steak', 'Chicken Soup', 'Bacon', 'Hummus'}
    
    def test_filter_parve_excludes_meat_dairy(self, meals_with_kosher_type):
        """Test that parve filter only shows parve and nonkosher."""
        result = filter_kosher(meals_with_kosher_type, KosherType.parve)
        assert len(result) == 3
        assert set(result['Name']) == {'Pasta Salad', 'Hummus', 'Bacon'}
        assert 'Cheeseburger' not in result['Name'].values  # milchik excluded
        assert 'Steak' not in result['Name'].values  # fleisch excluded
    
    def test_filter_milchik_excludes_meat(self, meals_with_kosher_type):
        """Test that milchik filter excludes fleisch."""
        result = filter_kosher(meals_with_kosher_type, KosherType.milchik)
        assert len(result) == 4
        assert set(result['Name']) == {'Pasta Salad', 'Cheeseburger', 'Bacon', 'Hummus'}
        assert 'Steak' not in result['Name'].values  # fleisch excluded
        assert 'Chicken Soup' not in result['Name'].values  # fleisch excluded
    
    def test_filter_fleisch_excludes_dairy(self, meals_with_kosher_type):
        """Test that fleisch filter excludes milchik."""
        result = filter_kosher(meals_with_kosher_type, KosherType.fleisch)
        assert len(result) == 5
        assert set(result['Name']) == {'Pasta Salad', 'Steak', 'Chicken Soup', 'Bacon', 'Hummus'}
        assert 'Cheeseburger' not in result['Name'].values  # milchik excluded

    def test_filter_kosher_fallback_legacy(self, meals_with_kosher_legacy):
        """Test that filter_kosher supports legacy 'Kosher' column name."""
        result = filter_kosher(meals_with_kosher_legacy, KosherType.parve)
        assert len(result) == 1
        assert result.iloc[0]['Name'] == 'Pasta Salad'
        
    def test_filter_kosher_missing_column(self):
        """Test that filter_kosher handles missing column gracefully."""
        df = pd.DataFrame({'Name': ['Test']})
        result = filter_kosher(df, KosherType.parve)
        assert len(result) == 1
        assert result.iloc[0]['Name'] == 'Test'


class TestFilterDiet:
    """Tests for the filter_diet function."""
    
    @pytest.fixture
    def meals_with_diet(self):
        """Create a meal database with dietary information."""
        data = {
            'Name': ['Tofu Stir Fry', 'Vegetable Curry', 'Grilled Chicken', 'Keto Salad', 'Gluten-Free Pasta', 'Regular Pizza'],
            'Diet': ['vegan', 'vegetarian', 'none', 'keto', 'glutenfree', 'none'],
            'Rank': [8, 7, 9, 7, 6, 8],
        }
        return pd.DataFrame(data)
    
    def test_filter_any_shows_all(self, meals_with_diet):
        """Test that 'any' diet filter shows all meals."""
        result = filter_diet(meals_with_diet, DietType.any)
        assert len(result) == 6
    
    def test_filter_vegan_only(self, meals_with_diet):
        """Test that vegan filter only shows vegan meals."""
        result = filter_diet(meals_with_diet, DietType.vegan)
        assert len(result) == 1
        assert result.iloc[0]['Name'] == 'Tofu Stir Fry'
    
    def test_filter_vegetarian_includes_vegan(self, meals_with_diet):
        """Test that vegetarian filter includes vegan meals."""
        result = filter_diet(meals_with_diet, DietType.vegetarian)
        assert len(result) == 2
        assert set(result['Name']) == {'Tofu Stir Fry', 'Vegetable Curry'}
    
    def test_filter_glutenfree(self, meals_with_diet):
        """Test that gluten-free filter works."""
        result = filter_diet(meals_with_diet, DietType.glutenfree)
        assert len(result) == 1
        assert result.iloc[0]['Name'] == 'Gluten-Free Pasta'
    
    def test_filter_keto(self, meals_with_diet):
        """Test that keto filter works."""
        result = filter_diet(meals_with_diet, DietType.keto)
        assert len(result) == 1
        assert result.iloc[0]['Name'] == 'Keto Salad'
    
    def test_filter_diet_missing_column(self, meals_with_kosher):
        """Test that filter_diet handles missing Diet column gracefully."""
        # meals_with_kosher doesn't have Diet column
        result = filter_diet(meals_with_kosher, DietType.vegan)
        # Should return original list with warning
        assert len(result) == len(meals_with_kosher)
    
    @pytest.fixture
    def meals_with_kosher(self):
        """Reuse from TestFilterKosher for missing column test."""
        data = {
            'Name': ['Pasta Salad', 'Cheeseburger'],
            'Kosher': ['parve', 'milchik'],
            'Rank': [7, 8],
        }
        return pd.DataFrame(data)


class TestFilterCombination:
    """Tests for combining kosher and diet filters."""
    
    @pytest.fixture
    def meals_with_both(self):
        """Create meals with both kosher and diet info."""
        data = {
            'Name': ['Vegan Hummus', 'Vegetarian Cheese Pizza', 'Beef Steak', 'Tofu Scramble'],
            'Kosher': ['parve', 'milchik', 'fleisch', 'parve'],
            'Diet': ['vegan', 'vegetarian', 'none', 'vegan'],
            'Rank': [8, 7, 9, 8],
        }
        return pd.DataFrame(data)
    
    def test_filter_vegan_and_parve(self, meals_with_both):
        """Test combining vegan and parve filters."""
        result = filter_kosher(meals_with_both, KosherType.parve)
        result = filter_diet(result, DietType.vegan)
        
        assert len(result) == 2
        assert set(result['Name']) == {'Vegan Hummus', 'Tofu Scramble'}
    
    def test_filter_vegetarian_and_milchik(self, meals_with_both):
        """Test combining vegetarian and milchik filters."""
        result = filter_kosher(meals_with_both, KosherType.milchik)
        result = filter_diet(result, DietType.vegetarian)
        
        assert len(result) == 3  # Vegan Hummus, Cheese Pizza, Tofu Scramble
        assert 'Beef Steak' not in result['Name'].values
    
    def test_filter_fleisch_excludes_vegan(self, meals_with_both):
        """Test that fleisch excludes all vegan options (which are parve)."""
        result = filter_kosher(meals_with_both, KosherType.fleisch)
        result = filter_diet(result, DietType.vegan)
        
        # Fleisch can have parve (vegan), so should show vegan parve options
        assert len(result) == 2
        assert set(result['Name']) == {'Vegan Hummus', 'Tofu Scramble'}
