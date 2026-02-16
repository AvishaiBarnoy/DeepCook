'''
main random meal choice function and its tiny helpers
this is called auxiallary as it is supposed to support the main main.py file
'''
from enum import Enum
import pandas as pd
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
    DEPRACTED
    still here to make sure nothing depends on this, this will be removed later
    '''
    parve= "parve"
    fleisch = "fleisch"
    milchik = "milchik"

def choose_random(meals, rank: bool = False, times: bool = False, last_made: int = 0, TA=None, k=1):
    '''
    makes a random choice of a meal from a meal DB
    
    Parameters:
        meals: DataFrame with meal data
        rank: bool, use weighted choice by rank
        times: bool, (not implemented)
        last_made: int, exclude meals made in the past N days. 0 = no filtering
        TA: bool or None, filter take-away options
        k: int, number of choices to return
    
    Returns:
        tuple: (meals, chosen_name, chosen_idx)
    '''
    use_rank = None
    
    meals_copy = meals.copy()
    
    # filter meals prepared in the past N days
    if last_made > 0:
        today = pd.Timestamp.now().date()
        # Convert Timestamp column to datetime, handling NaN/NaT values
        meals_copy['Timestamp'] = pd.to_datetime(meals_copy['Timestamp'], errors='coerce')
        
        # Filter out meals made within the last_made days
        # Keep meals where: timestamp is NaT (never made) OR timestamp is older than last_made days
        cutoff_date = today - pd.Timedelta(days=last_made)
        meals_copy = meals_copy[
            (meals_copy['Timestamp'].isna()) | 
            (meals_copy['Timestamp'].dt.date < cutoff_date)
        ]
        
        if len(meals_copy) == 0:
            print(f"Warning: All meals were made in the past {last_made} days. Ignoring filter.")
            meals_copy = meals.copy()

    # use a weighted choice, by rank
    if rank == True:
        use_rank = choice["Rank"]
    
    # include or choose only take-away, default is to random from everythin
    if TA == False:
        meals_copy = meals_copy[meals_copy["TA"] == 0]
    elif TA == True:
        meals_copy = meals_copy[meals_copy["TA"] == 1]
    
    is_late = is_too_late_to_cook()
    translate_time = {"short":0, "medium":1, "long": 2}
    if is_late == True:
        meals_copy.replace({"Prep_Time":translate_time,"Cook_Time":translate_time},inplace=True)
        meals_copy = meals_copy[meals_copy["Prep_Time"] < 2]
        meals_copy = meals_copy[meals_copy["Cook_Time"] < 2]

    choice = meals_copy.sample(n=k, weights=use_rank)

    print(choice["Name"].iloc[0])
    
    suggestion = meals.iloc[choice.index[0]].iloc[11]
    if isinstance(suggestion,str):
        print(f'Recipe suggestion: {suggestion}')
    elif isinstance(suggestion,float):
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
    # Check for kosher column (support both 'KosherType' and 'Kosher')
    col_name = None
    if 'KosherType' in meal_list.columns:
        col_name = 'KosherType'
    elif 'Kosher' in meal_list.columns:
        col_name = 'Kosher'
    
    if col_name is None:
        print("Warning: Kosher column not found in meal database. Skipping kosher filter.")
        return meal_list

    if kosher == KosherType.nonkosher:
        # Nonkosher can eat anything
        return meal_list
    elif kosher == KosherType.parve:
        # Parve can eat parve and nonkosher
        return meal_list[meal_list[col_name].isin(['parve', 'nonkosher'])]
    elif kosher == KosherType.milchik:
        # Milchik can eat milchik, parve, and nonkosher (no fleisch)
        return meal_list[meal_list[col_name].isin(['milchik', 'parve', 'nonkosher'])]
    elif kosher == KosherType.fleisch:
        # Fleisch can eat fleisch, parve, and nonkosher (no milchik)
        return meal_list[meal_list[col_name].isin(['fleisch', 'parve', 'nonkosher'])]
    
    return meal_list


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

