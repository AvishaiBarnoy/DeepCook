'''
Here I will have the main logic
'''

import pandas as pd
import auxillary as aux
import io_data as iod
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
    #print(data)
    #random_choice = aux.choose_random(data)
    #print(type(random_choice))

    
    typer.run(main)
    # uncomment to reset timestamps and times_made
    #aux.reboot_time_timestamps(data)
