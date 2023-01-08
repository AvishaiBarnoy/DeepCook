'''
random meal choice function and its tiny helpers
this is called auxiallary as it is supposed to support the main main.py file
'''
from enum import Enum
import pandas as pd
from pathlib import Path


# TODO:
# Think how each function talks with another
# what is the relationships between the objects passed around

try:
    import scripts.iodata as iod
    #from classes.classes import KosherType
except:
    import iodata as iod
    #import classes.classes
    #from ../classes/classes.py import KosherType
    #class_path = Path(__file__).parent / "../classes/"
    #print(class_path)
    #import class_path.classes

def choose_random(meals, rank: bool = False, times: bool = False, last_made: bool = False, TA=False, k=1):
    '''
    meals ::: pandas DataFrame, meals data
    TA    ::: bool, should choose random from take-away options
    
    makes a random choice of a meal from a meal DB

    IMPORTANT: this returns too many arguments, either needs to be truncated or used by other functions 
    
    TODO:
        1. get rid of all the print(). make a parameter called "out_msg" and throw everything inside for return
    '''
    use_rank = None
           
    # filter meals prepared in the past 4 days
    # NOT IMPLEMENTED YET #

    # use a weighted choice, by rank
    if rank == True:
        use_rank = choice["Rank"]
    
    # filter for take-away, TA is boolean:
    meals = meals[meals["TA"] == TA]

    ################################
    # REFACTORED TO LOCAL FUNCTION #
    #       filter_long            #
    ################################
    #if check_time == True:
    #    is_late = is_too_late_to_cook()
    #    translate_time = {"short":0, "medium":1, "long": 2}
    #    if is_late == True:
    #        meals.replace({"Prep_Time":translate_time,"Cook_Time":translate_time},inplace=True)
    #        meals = meals_copy[meals_copy["Prep_Time"] < 2]
    #        meals = meals_copy[meals_copy["Cook_Time"] < 2]

    choice = meals.sample(n=k, weights=use_rank)
    
    choice_name = choice["Name"].iloc[0]

    return choice

def filter_long(meals):
    """
    converts Prep_Time and Cook_Time to numerical value and filters out
    all meals that take too long to prepare
    """

    translate_time = {"short":0, "medium":1, "long": 2}
    meals.replace({"Prep_Time":translate_time,"Cook_Time":translate_time},inplace=True)
    meals["Total_Time"] = meals["Prep_Time"] + meals["Cook_Time"]
    meals = meals[meals["Total_Time"] < 3]

    choice = choose_random(meals)
    return choice

def make_this_meal(meals, choice):
    '''
    ################################
    # DOES NOT WORK WITH STREAMLIT #
    ################################

    Asks user if he will make the meal, if yes meal is logged.
    doesn't return anythin, just changes the state of the meals DB
    '''
    make_it = input("Are you going to make this meal? (y/n)")
    while True:
        if make_it.lower() == "y":
            meals.loc[choice,"times_made"] += 1
            meals.loc[choice,"Timestamp"] = pd.Timestamp.now().date()
            print("meal logged.")
            return True
        elif make_it.lower() == "n":
            print("meal not logged.")
            return False
        else:
            print("Please enter a valid answer.")
            make_it = input("Are you going to make this meal? (y/n)")

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

def filter_kosher(meal_list, kosher):# KosherType):
    '''
    Takes loaded meal_list DF and returns the filtered meals according to specified kosher

    meal_list   ::: pandas DataFrame with meals
    kosher      ::: kosher type [parve|milchik|fleisch]
    '''
    return meal_list

if __name__ == "__main__":
    FILENAME = "../data/meal_list.csv"
    PATH = Path(__file__).parent / FILENAME
    data = pd.read_csv(PATH, index_col=0)
    #print(data)
    suggestion = choose_random(data,rank=False,times=False,last_made=False,TA=False,k=1)
    print(suggestion)
    #print(filter_long(data))
    #reboot_time_timestamps(data)

