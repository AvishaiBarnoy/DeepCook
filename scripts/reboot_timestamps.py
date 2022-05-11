'''
This script just reboots all timestamps and meal log data, good to run this when first configurating the program to your needs.
'''
import pandas as pd
import scripts.auxillary as aux
import scripts.iodata as iod
import typer

def main(data: str):
    """
    resets all date data in the data file
    """
    meals_db = pd.read_csv(f"./data/{data}", index_col=0)
    aux.reboot_time_timestamps(meals_db)

if __name__ == "__main__":
    typer.run(main)
