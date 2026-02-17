'''
main random meal choice function and its tiny helpers
this is called auxiallary as it is supposed to support the main main.py file
'''
from enum import Enum
import pandas as pd
import numpy as np
from pathlib import Path

try:
    import scripts.iodata as iod
    from classes.classes import KosherType, DietType
except:
    import iodata as iod
    import classes.classes
    #from ../classes/classes.py import KosherType
    #class_path = Path(__file__).parent / "../classes/"
    #print(class_path)
    #import class_path.classes

class Kosher(str, Enum):
    '''
    DEPRECATED
    still here to make sure nothing depends on this, this will be removed later
    '''
    parve = "parve"
    fleisch = "fleisch"
    milchik = "milchik"

def choose_random(
    meals, 
    rank: bool = False, 
    times: bool = False, 
    last_made: int = 0, 
    TA=None, 
    k=1, 
    kosher: KosherType = KosherType.nonkosher, 
    diet: DietType = DietType.any,
    ease_cutoff: int | None = None,
    kids: bool | None = None,
    scaling_only: bool = False,
    surprise_me: bool = False
):
    '''
    makes a random choice of a meal from a meal DB
    
    Parameters:
        meals: DataFrame with meal data
        rank: bool, use weighted choice by rank
        times: bool, if True, adjust weights based on times_made and timestamp (penalty for recent/frequent)
        last_made: int, exclude meals made in the past N days. 0 = no filtering
        TA: bool or None, filter take-away options
        k: int, number of choices to return
        kosher: KosherType enum, filter by kosher requirements
        diet: DietType enum, filter by dietary preferences
        ease_cutoff: int, if set, only show meals with Prep_Ease <= ease_cutoff
        kids: bool or None, filter for kids-friendly meals
        scaling_only: bool, only show meals that scale well
        surprise_me: bool, prioritize meals never made or low-frequency
    
    Returns:
        tuple: (meals, chosen_name, chosen_idx)
    '''
    use_rank = None
    
    # 1. Apply Kosher filter
    meals_copy = filter_kosher(meals, kosher)
    
    # 2. Apply Diet filter
    meals_copy = filter_diet(meals_copy, diet)
    
    # 3. Filter by Ease
    if ease_cutoff is not None and 'Prep_Ease' in meals_copy.columns:
        # Assuming Prep_Ease 1 is easiest, 10 is hardest
        meals_copy = meals_copy[meals_copy['Prep_Ease'].astype(float) <= float(ease_cutoff)]
        if len(meals_copy) == 0:
            print(f"Warning: No meals found with ease <= {ease_cutoff}. Ignoring ease filter.")
            meals_copy = filter_diet(filter_kosher(meals, kosher), diet)

    # 4. Filter by Kids
    if kids is not None and 'Kids' in meals_copy.columns:
        val = 1 if kids else 0
        meals_copy = meals_copy[meals_copy['Kids'].astype(float) == float(val)]
        if len(meals_copy) == 0:
            print(f"Warning: No meals found for kids={kids}. Ignoring kids filter.")
            meals_copy = filter_diet(filter_kosher(meals, kosher), diet)
            if ease_cutoff is not None and 'Prep_Ease' in meals_copy.columns:
                meals_copy = meals_copy[meals_copy['Prep_Ease'].astype(float) <= float(ease_cutoff)]

    # 4.5 Filter by Scaling (Cooking for a crowd)
    if scaling_only and 'Scaling' in meals_copy.columns:
        # Assuming 1 is good for scaling, 0 is not. If empty, assume it doesn't scale well unless marked.
        meals_copy = meals_copy[meals_copy['Scaling'].astype(float) == 1.0]
        if len(meals_copy) == 0:
            print("Warning: No high-scaling meals found. Ignoring scaling filter.")
            # Fallback (don't reset everything, just this filter)
            meals_copy = filter_diet(filter_kosher(meals, kosher), diet)
            if kids is not None and 'Kids' in meals_copy.columns:
                 meals_copy = meals_copy[meals_copy['Kids'].astype(float) == float(1 if kids else 0)]

    # 4. Filter meals prepared in the past N days
    if last_made > 0:
        today = pd.Timestamp.now().normalize()
        meals_copy['Timestamp'] = pd.to_datetime(meals_copy['Timestamp'], errors='coerce')
        cutoff_date = today - pd.Timedelta(days=last_made)
        meals_copy = meals_copy[
            (meals_copy['Timestamp'].isna()) | 
            (meals_copy['Timestamp'] < cutoff_date)
        ]
        
        if len(meals_copy) == 0:
            print(f"Warning: All meals matching other filters were made in the past {last_made} days. Ignoring age filter.")
            # Fallback to state before age filter
            state_before = filter_diet(filter_kosher(meals, kosher), diet)
            if ease_cutoff is not None and 'Prep_Ease' in state_before.columns:
                state_before = state_before[state_before['Prep_Ease'].astype(float) <= float(ease_cutoff)]
            meals_copy = state_before

    # 5. Filter Take-Away
    if TA == False:
        meals_copy = meals_copy[meals_copy["TA"] == 0]
    elif TA == True:
        meals_copy = meals_copy[meals_copy["TA"] == 1]
    
    # Check if we have any meals left after filtering
    if len(meals_copy) == 0:
        print("Warning: No meals found after applying filters.")
        return meals, None, None

    # 6. Check for late-night cooking
    is_late = is_too_late_to_cook()
    translate_time = {"short":0, "medium":1, "long": 2}
    if is_late == True:
        if 'Prep_Time' in meals_copy.columns and 'Cook_Time' in meals_copy.columns:
            meals_subset = meals_copy.copy()
            meals_subset.replace({"Prep_Time":translate_time,"Cook_Time":translate_time},inplace=True)
            meals_subset = meals_subset[meals_subset["Prep_Time"] < 2]
            meals_subset = meals_subset[meals_subset["Cook_Time"] < 2]
            if len(meals_subset) > 0:
                meals_copy = meals_subset
            else:
                print("Warning: It's late but only 'long' prep meals remain. Suggesting a meal anyway.")

    # 7. Calculate weights
    weights = pd.Series(1.0, index=meals_copy.index)
    
    if rank == True and "Rank" in meals_copy.columns:
        weights = meals_copy["Rank"].astype(float).fillna(5.0)
    
    if times == True and "times_made" in meals_copy.columns:
        # Frequency penalty
        times_made = meals_copy["times_made"].fillna(0).astype(float)
        weights = weights / (1.0 + 0.5 * times_made)
        
        # Time decay penalty (if timestamp available)
        if "Timestamp" in meals_copy.columns:
            ts = pd.to_datetime(meals_copy['Timestamp'], errors='coerce')
            days_since = (pd.Timestamp.now() - ts).dt.days.fillna(365)
            # Decaying factor: lower weight for more recent
            decay = 1.0 - np.exp(-days_since / 14.0)
            weights = weights * (decay + 0.05)

    if surprise_me:
        # Prioritize 0 times_made or very low frequency
        if "times_made" in meals_copy.columns:
            times_made = meals_copy["times_made"].fillna(0).astype(float)
            # Inverse of frequency gives high weight to 0 or 1
            surprise_weights = 1.0 / (1.0 + times_made)
            weights = weights * (surprise_weights * 10.0) 
    
    # Normalize weights to avoid issues
    if weights.sum() == 0:
        weights = None
    
    choice = meals_copy.sample(n=k, weights=weights)

    print(choice["Name"].iloc[0])
    
    # Try to find recipe suggestion URL (column 11 is recipe_suggestion in standard schema)
    if len(meals_copy.columns) > 11:
        suggestion = meals.iloc[choice.index[0]].iloc[11]
        if isinstance(suggestion, str) and suggestion.startswith("http"):
            print(f'Recipe suggestion: {suggestion}')
        else:
            print("No recipe suggestion exists in the database.")
    
    return meals, choice["Name"].iloc[0], choice.index[0]

def make_this_meal(meals, choice):
    '''
    Asks user if he will make the meal, if yes meal is logged.
    doesn't return anythin, just changes the state of the meals DB
    '''
    make_it = input("Are you going to make this meal? (y/n)")
    while True:
        if make_it.lower() == "y":
            meals.loc[choice,"times_made"] += 1
            meals.loc[choice,"Timestamp"] =pd.to_datetime(pd.Timestamp.now().date())
            print("meal logged.")
            return True
        elif make_it.lower() == "n":
            print("meal not logged.")
            return False
        else:
            print("Please enter a valid answer.")
            make_it = input("Are you going to make this meal? (y/n)")

def is_too_late_to_cook(cutoff: int = 20):
    '''
    Checks actual time and returns if choose_random should skip ideas with long preparation time.
        After 20:00 only short and medium durations will be considered.
        Between midnight and 5:00 AM, also returns True (too late to cook).
    
    Returns:
        bool: True if too late to cook (filter out long meals), False otherwise
    '''
    hour = pd.Timestamp.now().hour
    
    # Check early morning hours first (midnight to 5 AM)
    if hour < 5:
        return True  # Don't cook in the middle of the night
    
    # Then check if after cutoff time
    if hour < cutoff:
        return False  # Before cutoff, not too late
    else:
        return True  # After cutoff, too late

def reboot_time_timestamps(data="meal_list.csv",logfile="meal.log"):
    '''
    Resets all times made to 0 and removes all time stamps.
    This is currently designed only testing and developing.
    '''
    while True:
        just_checking = input("Are you sure you want to reset *ALL* timestamps and all times_made? (y/n)")
        if just_checking.lower() == "n":
            print("data was not reset")
            return 0
        elif just_checking.lower() == "y":
            data["Timestamp"] = "NaN"
            data["times_made"] = 0
            iod.save_data(data)
            with open(logfile, "w") as f: pass # empties the meal.log file
            print("Data was reset and saved")
            return 0

def filter_kosher(meal_list, kosher: KosherType):
    '''
    Filters meals according to kosher requirements.
    Standardized to use 'KosherType' column.
    
    Kosher rules:
    - parve: can eat parve and nonkosher meals
    - milchik: can eat milchik, parve, and nonkosher meals
    - fleisch: can eat fleisch, parve, and nonkosher meals  
    - nonkosher: can eat anything
    
    Parameters:
        meal_list: pandas DataFrame with meals
        kosher: KosherType enum [parve|milchik|fleisch|nonkosher]
    
    Returns:
        pandas DataFrame with filtered meals
    '''
    if 'KosherType' not in meal_list.columns:
        print("Warning: 'KosherType' column not found in database. Skipping kosher filter.")
        return meal_list

    if kosher == KosherType.nonkosher:
        return meal_list
    elif kosher == KosherType.parve:
        return meal_list[meal_list['KosherType'].isin(['parve', 'nonkosher'])]
    elif kosher == KosherType.milchik:
        return meal_list[meal_list['KosherType'].isin(['milchik', 'parve', 'nonkosher'])]
    elif kosher == KosherType.fleisch:
        return meal_list[meal_list['KosherType'].isin(['fleisch', 'parve', 'nonkosher'])]
    
    return meal_list

def choose_batch(meals, k=7, **kwargs):
    '''
    Selects a batch of k unique meals using provided filters.
    A wrapper around choose_random logic for multiple selections.
    '''
    results = []
    temp_db = meals.copy()
    
    for _ in range(k):
        # We call choose_random with k=1 each time to handle weights correctly for individual pics
        # but we need to remove the chosen one from temp_db to ensure uniqueness
        _, name, idx = choose_random(temp_db, k=1, **kwargs)
        
        if name is None:
            # If we run out of meals matching criteria
            results.append((None, None))
            continue
            
        results.append((name, idx))
        temp_db = temp_db.drop(index=idx)
        
def get_meal_for_day(db, kosher: KosherType, diet: DietType, prev_main=None, leftover_mode=False):
    '''
    Suggests a meal for a specific day, considering leftover logic.
    '''
    # 1. Leftover logic: If leftover mode is on and previous main scales well, reuse it
    if leftover_mode and prev_main is not None:
        # Check if Scaling is 1.0 (float or int)
        scaling_val = prev_main.get('Scaling', 0)
        try:
             if float(scaling_val) == 1.0:
                 return prev_main
        except (ValueError, TypeError):
             pass
            
    # 2. Otherwise pick a random one
    # last_made=3 to ensure some variety from recent history if available
    _, name, idx = choose_random(db, kosher=kosher, diet=diet, last_made=3, times=True)
    
    if name:
        return db.loc[idx].to_dict()
    return None


def get_recipe_link(meal_row, preferred_site=None):
    '''
    Returns a recipe link for a meal.
    If 'recipe_suggestion' is a valid URL, it's used.
    Otherwise, generates a search link for popular Israeli recipe sites.
    
    Parameters:
        meal_row: dict or Series, the meal data
        preferred_site: str, optional ('krutit', 'kitchencoach', 'nikib', 'mako')
    '''
    # 1. Use existing suggestion if valid
    suggestion = meal_row.get('recipe_suggestion')
    if isinstance(suggestion, str) and suggestion.startswith("http"):
        return suggestion
        
    # 2. Generate Search Link
    # Prefer Hebrew name for searching Israeli sites
    name_he = meal_row.get('Name_HE')
    name_en = meal_row.get('Name')
    query = name_he if isinstance(name_he, str) and name_he != "" else name_en
    
    if not query:
        return None
        
    # Search Templates
    templates = {
        'krutit': f"https://www.krutit.co.il/?s={query}",
        'kitchencoach': f"https://www.kitchencoach.co.il/?s={query}",
        'nikib': f"https://nikib.co.il/?s={query}",
        'mako': f"https://www.mako.co.il/search-results?q={query}",
        'google': f"https://www.google.com/search?q={query}+מתכון"
    }
    
    if preferred_site in templates:
        return templates[preferred_site]
        
    # Default to Google Search (Hebrew) or Krutit
    return templates['krutit']

def filter_diet(meal_list, diet: DietType):
    '''
    Filters meals according to dietary preferences.
    
    Diet filtering rules:
    - any: no filtering
    - vegan: only vegan meals
    - vegetarian: vegan + vegetarian meals
    - glutenfree: meals marked as gluten-free
    - keto: meals marked as keto-friendly
    
    Parameters:
        meal_list: pandas DataFrame with meals
        diet: DietType enum [any|vegan|vegetarian|glutenfree|keto]
    
    Returns:
        pandas DataFrame with filtered meals
    
    Note: Requires 'Diet' column in the DataFrame. If column doesn't exist,
          returns original list with a warning.
    '''
    # Check if Diet column exists
    if 'Diet' not in meal_list.columns:
        print("Warning: 'Diet' column not found in meal database. Skipping diet filter.")
        return meal_list
    
    if diet == DietType.any:
        return meal_list
    elif diet == DietType.vegan:
        return meal_list[meal_list['Diet'].str.contains('vegan', case=False, na=False)]
    elif diet == DietType.vegetarian:
        # Vegetarian includes vegan
        return meal_list[meal_list['Diet'].str.contains('vegan|vegetarian', case=False, na=False)]
    elif diet == DietType.glutenfree:
        return meal_list[meal_list['Diet'].str.contains('glutenfree', case=False, na=False)]
    elif diet == DietType.keto:
        return meal_list[meal_list['Diet'].str.contains('keto', case=False, na=False)]
    
    return meal_list


if __name__ == "__main__":
    FILENAME = "../data/meal_list.csv"
    PATH = Path(__file__).parent / FILENAME
    data = pd.read_csv(PATH, index_col=0)
    #reboot_time_timestamps(data)

