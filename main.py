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

<<<<<<< HEAD
def main(data: str = MEAL_LIST, rank: bool = False, TA: bool = None, inp: bool = False, mock: bool = False, kosher: str = "fleisch"):
    """
    data ::: str, csv file with the meal data - default meal_list.csv in the data folder.
=======
>>>>>>> f311e5d871ff080c3907212d8c693da46d5c60d9

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
    kosher: aux.Kosher = typer.Option(aux.Kosher.fleisch, case_sensitive=False)
):
    #typer.echo(f"Choosing meal from {kosher.value}")
<<<<<<< HEAD
    print(f"mock value is {mock}") 
    meals_db = pd.read_csv(absolute_path, index_col=0)
    
    # meals_db = aux.filter_kosher(meals_db, kosher) -> PROBLEM: will overwrite DB with only kosher meals
=======

    meals_db = pd.read_csv(absolute_path, index_col=0)

    meals_db = aux.filter_kosher(meals_db, kosher)
>>>>>>> f311e5d871ff080c3907212d8c693da46d5c60d9
    if inp:
        new_meal = iod.meal_questions(meals_db)
        meals_db = iod.add_meal(meals_db, new_meal)
    else:
        meals_db, chosen_one = aux.choose_random(meals_db, rank, TA)
<<<<<<< HEAD
        if mock == True:
            pass
        elif mock == False:
            iod.write_to_log(chosen_one)
     
=======
        iod.write_to_log(chosen_one)

>>>>>>> f311e5d871ff080c3907212d8c693da46d5c60d9
    # save changes
    if mock == True:
        pass
    elif mock == False:
        iod.save_data(meals_db, absolute_path)


if __name__ == "__main__":
    typer.run(main)
