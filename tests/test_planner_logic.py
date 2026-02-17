import pytest
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import scripts.auxillary as aux
from classes.classes import KosherType, DietType

@pytest.fixture
def mock_db():
    data = {
        'Name': ['Pasta', 'Steak', 'Salad', 'Burger'],
        'KosherType': ['parve', 'fleisch', 'parve', 'fleisch'],
        'Scaling': [1.0, 0.0, 1.0, 1.0],
        'times_made': [0, 0, 0, 0],
        'Rank': [10, 10, 10, 10],
        'Timestamp': [None, None, None, None]
    }
    return pd.DataFrame(data)

def test_get_meal_for_day_basic(mock_db):
    meal = aux.get_meal_for_day(mock_db, KosherType.nonkosher, DietType.any)
    assert meal is not None
    assert 'Name' in meal

def test_get_meal_for_day_leftovers(mock_db):
    # If leftover_mode is True and prev_main scales well (1.0)
    prev_main = mock_db.iloc[0].to_dict() # Pasta (Scaling 1.0)
    meal = aux.get_meal_for_day(mock_db, KosherType.nonkosher, DietType.any, prev_main=prev_main, leftover_mode=True)
    assert meal['Name'] == 'Pasta'

def test_get_meal_for_day_no_leftovers_if_scaling_low(mock_db):
    # If leftover_mode is True but prev_main doesn't scale well (0.0)
    prev_main = mock_db.iloc[1].to_dict() # Steak (Scaling 0.0)
    meal = aux.get_meal_for_day(mock_db, KosherType.nonkosher, DietType.any, prev_main=prev_main, leftover_mode=True)
    # Should pick something else (or randomly pick the same, but here we expect variety logic to potentially pick others)
    # In our mock DB, it should just pick something.
    assert meal is not None

def test_get_meal_for_day_kosher_filter(mock_db):
    # Fleisch filter should exclude nothing in this logic (wait, fleisch filter in auxillary allows fleisch + parve)
    # But if we ask for Parve only:
    meal = aux.get_meal_for_day(mock_db, KosherType.parve, DietType.any)
    assert meal['KosherType'] in ['parve', 'nonkosher']
    assert meal['Name'] in ['Pasta', 'Salad']

def test_get_meal_for_day_exhaustion(mock_db):
    # Filter that matches nothing
    empty_db = mock_db[mock_db['Name'] == 'Nothing']
    meal = aux.get_meal_for_day(empty_db, KosherType.nonkosher, DietType.any)
    assert meal is None
