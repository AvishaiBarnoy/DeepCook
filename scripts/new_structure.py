"""
1. choose_random
2. filter_long
3. make_this_meal 
4. reboot_time_stamp - obsolete, should work with logs
5. filter_kosher - 
6. read_file
"""

import pandas as pd
from pathlib import Path

def read_meal_file(filename):
    filepath = "../data/" + filename
    path_to_meal = Path(__file__).parent / filepath
    meal_data = pd.read_csv(path_to_meal, index_col=0)
    return meal_data

test_filename = "meal_list.csv"
test_read = pd.read_csv(Path(__file__).parent / f"../data/{test_filename}", index_col=0)
assert pd.testing.assert_frame_equal(read_meal_file(test_filename),test_read) == None

# maybe combine these into one
def filter_prep_time():
    pass

def filter_cook_time():
    pass

def cook_the_dish():
    pass

def filter_kosher(meal_data,kosher):
    """filter by kosher type, not if meal is kosher"""
    filterd_for_kosher = meal_data[meal_data["KosherType"] == kosher]
    return filtered_for_kosher

def filter_diet():
    """celiac, non-dairy, vegeterian, vegan, etc."""
    pass

def filter_complexity():
    """filter how complex is the meal"""
    pass

def is_recipe():
    """only show meals that have a recipe suggestion"""
    pass

def filter_too_soon():
    """filter if meal was prepared recently"""
    pass

def log_meal():
    """
    if yes -> cooked_log
    if no -> not_cooked_log
    """
    pass

def choose_random():
    """implement here ranking flag"""
    pass

def test_run(filename):
    data = read_meal_file(filename)
    pass

if __name__ == "__main__":
    meal_filename = "meal_list.csv"
    run = test_run(meal_filename)
