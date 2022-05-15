'''
Here happens all the magic
'''

import pandas as pd
import scripts.auxillary as aux
import scripts.iodata as iod
import typer
import os
from pathlib import Path

# default absolute pathway
MEAL_LIST = "data/meal_list.csv"
#absolute_path = os.path.join(os.path.dirname(__file__), f"../data/{MEAL_LIST}")
absolute_path = Path(__file__).parent / MEAL_LIST

def main(data: str = MEAL_LIST, rank: bool = False, TA: bool = None, inp: bool = False):
    """
    data ::: str, csv file with the meal data - default meal_list.csv in the data folder.

    rank ::: uses weights from the rank feature for random meal.

    TA   ::: True-chooses only from takeaway, False-choose from everythin except TA, no-flag - choose from everything including TA.

    inp  ::: Add a new meal to the meal DB, by questions to the audience. 
    """
    meals_db = pd.read_csv(absolute_path, index_col=0)
    
    if inp:
        new_meal = iod.meal_questions(meals_db)
        meals_db = iod.add_meal(meals_db, new_meal) 
    
    else:
        meals_db, chosen_one = aux.choose_random(meals_db, rank, TA)
        iod.write_to_log(chosen_one)
    
    # save changes
    iod.save_data(meals_db, absolute_path)

if __name__ == "__main__":
    typer.run(main)
