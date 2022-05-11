'''
Here happens all the magic
'''

import pandas as pd
import scripts.auxillary as aux
import scripts.iodata as iod
import typer


# default 
MEAL_LIST = "./data/meal_list.csv"

#def choose_random(meals, rank=False, times=False, last_made=False, TA=None, k=1):
#def main(name: str = "", lastname: str = "", formal: bool = False):
def main(data: str = MEAL_LIST, rank: bool = False, TA: bool = None):
    """
    data ::: str, csv file with the meal data - default meal_list.csv in the data folder.
    rank ::: uses weights from the rank feature for random meal.
    TA   ::: True-chooses only from takeaway, False-choose from everythin except TA, no flag
                choose from everything including TA.
    """
    meals_db = pd.read_csv(data, index_col=0)
     
    meals_db, chosen_one = aux.choose_random(meals_db, rank, TA)

    # save changes
    iod.save_data(meals_db, MEAL_LIST)
    iod.write_to_log(chosen_one)

if __name__ == "__main__":
    typer.run(main)
