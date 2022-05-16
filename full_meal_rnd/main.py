'''
Here happens all the magic
'''

import pandas as pd
#import scripts.auxillary as aux
#import scripts.iodata as iod
import typer
import os
from pathlib import Path

# default absolute pathway
MEAL_LIST = "data/meal_list.csv"
#absolute_path = os.path.join(os.path.dirname(__file__), f"../data/{MEAL_LIST}")
absolute_path = Path(__file__).parent / MEAL_LIST
soup_list = ''
main_courses = ''
side_dishes = ''
salads = ''
desserts = ''

def main(soups: str = soup_list, main: str = main_courses, side: str = side_dishes, salad: str = salads,
        dessert: str = desserts):
    print("Not implemented yet")

if __name__ == "__main__":
    typer.run(main)
