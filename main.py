'''
Here happens all the magic
'''

import pandas as pd
import scripts.auxillary as aux
import scripts.iodata as iod
import typer
from pathlib import Path
from classes.classes import KosherType, DietType

# default absolute pathway
MEAL_LIST = "data/meal_list.csv"
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
    last_made: int = typer.Option(
        0, help="exclude meals made in the past N days (0 = no filtering, recommended: 3-5)"),
    inp: bool = typer.Option(
        False, help="Add a new meal to the meal DB, by questions to the audience"),
    kosher: KosherType = typer.Option(KosherType.nonkosher, case_sensitive=False, help="Filter by kosher type: parve, milchik, fleisch, nonkosher"),
    diet: DietType = typer.Option(DietType.any, case_sensitive=False, help="Filter by diet: any, vegan, vegetarian, glutenfree, keto"),
    ease: int = typer.Option(None, help="Filter by preparation ease (1-10, lower is easier)"),
    times: bool = typer.Option(False, "--smarter-weighting", help="Penalize meals prepared frequently"),
    mock: bool = typer.Option(False, help="Mock try for testing and developing, will not prompt for saving.")
):
    
    # load data
    meals_db = pd.read_csv(absolute_path, index_col=0)

    #meals_db = aux.filter_kosher(meals_db, kosher)
    #filterd_meals = aux.filter_kosher(meals_db, kosher)

    # adding new meal to db or randomly suggesting one
    if inp:
        new_meal = iod.meal_questions(meals_db)
        if new_meal is not None:
            meals_db = iod.add_meal(meals_db, new_meal)
    else:
        # Apply filters via choose_random
        _, chosen_one, chosen_idx = aux.choose_random(
            meals_db, 
            rank=rank, 
            last_made=last_made, 
            TA=TA, 
            kosher=kosher, 
            diet=diet,
            ease_cutoff=ease,
            times=times
        )
        
        if chosen_one is not None and mock == False:
            iod.write_to_log(chosen_one)
            aux.make_this_meal(meals_db, chosen_idx)
        elif chosen_one is None:
            print("No meal found with current filters.")

    # save changes
    if mock == False:
        iod.save_data(meals_db, absolute_path)

if __name__ == "__main__":
    typer.run(main)
