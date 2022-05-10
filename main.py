'''
Here happens all the magic
'''

import pandas as pd
import scripts.auxillary as aux
import scripts.iodata as iod
import typer

#def choose_random(meals, rank=False, times=False, last_made=False, TA=None, k=1):
#def main(name: str = "", lastname: str = "", formal: bool = False):
def main(data: str, rank: bool = False, TA: bool = False):
    """
    < Here will go some text >

    data ::: str, csv file with the meal data
    """
    meals_db = pd.read_csv(data, index_col=0)
    aux.choose_random(meals_db, rank, TA )

if __name__ == "__main__":
    typer.run(main)
