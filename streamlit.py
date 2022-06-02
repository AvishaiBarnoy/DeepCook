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

if st.button('Random meal idea!'):
    _, chosen_one, chosen_idx = aux.choose_random(meals_db, rank=False, TA=None)
    st.write('Your random meal is: ', chosen_one)


