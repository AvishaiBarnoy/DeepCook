'''
This script just reboots all timestamps and meal log data, good to run this when first configurating the program to your needs.
'''
import pandas as pd
import typer
import os
from pathlib import Path
try:
    import scripts.auxillary as aux
    import scripts.iodata as iod
except:
    import auxillary as aux
    import iodata as iod

def main(data: str = "../data/meal_list.csv", log: str = "../data/meal.log"):
    """
    resets all date data in the data file
    """

    DATANAME = data
    LOGNAME  = log
    PATH = os.path.dirname(__file__)

    datapath = Path(__file__).parent / data
    logpath  = Path(__file__).parent / log
    
    meals_db = pd.read_csv(datapath, index_col=0)
    aux.reboot_time_timestamps(data=meals_db, logfile=log)

if __name__ == "__main__":
    pass
    typer.run(main)
