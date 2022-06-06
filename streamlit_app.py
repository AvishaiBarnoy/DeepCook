import streamlit as st
import pandas as pd
from pathlib import Path

import scripts.auxillary as aux
import scripts.iodata as iod

# Simple App

st.title('DeepCook Web App')

st.write('Just press the button and DeepCook will give you a meal suggestion!')

MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent / MEAL_LIST
meals_db = pd.read_csv(absolute_path, index_col=0)
COUNTER_PATH = "data/counter.txt"
counter_file = Path(__file__).parent / COUNTER_PATH

# initiate counter
with open(counter_file, "r") as f:
    counter = f.readline()
    counter = 0 if counter == "" else int(counter)

if st.button('Random meal idea!'):
    counter += 1
    _, chosen_one, chosen_idx = aux.choose_random(meals_db, rank=False, TA=None)
    st.write('Your random meal is: ', chosen_one)
    
    # print recipe suggestion if one exists
    suggestion = meals_db.iloc[chosen_idx].iloc[11]
    if isinstance(suggestion, str):
        st.write(f'Recipe suggestion: {suggestion}')
    elif isinstance(suggestion, float):
        st.write("No recipe suggestion exists in the database.")

    with open(counter_file, "w") as f:
        f.truncate()
        f.write(f"{counter}")

st.write(f"People that pressed on the button: {counter}")

