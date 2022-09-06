'''
Here happens all the magic
'''

import pandas as pd
#import scripts.auxillary as aux
#import scripts.iodata as iod
from pathlib import Path

# default absolute pathway
MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent / MEAL_LIST
soup_list = ''
main_courses = ''
side_dishes = ''
salads = ''
desserts = ''

st.selectbox("Number of diners",tuple(range(1,11)))

