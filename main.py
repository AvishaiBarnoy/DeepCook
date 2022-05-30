'''
Here happens all the magic
'''

import pandas as pd
import scripts.auxillary as aux
import scripts.iodata as iod
import typer
import os
from pathlib import Path
from classes.classes import KosherType

# default absolute pathway
MEAL_LIST = "data/meal_list.csv"
#absolute_path = os.path.join(os.path.dirname(__file__), f"../data/{MEAL_LIST}")
absolute_path = Path(__file__).parent / MEAL_LIST


def main(
    data: str = typer.Option(MEAL_LIST, help="csv file with the meal data"),
    rank: bool = typer.Option(
        False, help="uses weights from the rank feature for random meal"),
    TA: bool = typer.Option(
        None, "--ta/--no-ta",
        help='''True: chooses only from takeaway,
False: from everythin except TA,
no-flag: choose from everything including TA'''),
    inp: bool = typer.Option(
        False, help="Add a new meal to the meal DB, by questions to the audience"),
    kosher: KosherType = typer.Option(KosherType.fleisch, case_sensitive=False, help="NOT YET IMPLEMENTED."),
    #mock: bool = typer.Option("Mock try for testing and developing, will not prompt for saving.", case_sensitive=False)
    mock: bool = typer.Option(False, help="Mock try for testing and developing, will not prompt for saving.")
):
    
    # load data
    meals_db = pd.read_csv(absolute_path, index_col=0)

    #meals_db = aux.filter_kosher(meals_db, kosher)
    #filterd_meals = aux.filter_kosher(meals_db, kosher)

    # adding new meal to db or randomly suggesting one
    if inp:
        new_meal = iod.meal_questions(meals_db)
        meals_db = iod.add_meal(meals_db, new_meal)
    else:
        filterd_meals = aux.filter_kosher(meals_db, kosher)
        _, chosen_one, chosen_idx = aux.choose_random(meals_db, rank, TA)
        if mock == False:
            iod.write_to_log(chosen_one)
            aux.make_this_meal(meals_db,chosen_idx)

    # save changes
    if mock == False:
        iod.save_data(meals_db, absolute_path)

if __name__ == "__main__":
    typer.run(main)
