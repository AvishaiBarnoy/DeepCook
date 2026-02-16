import streamlit as st
import pandas as pd
from pathlib import Path

import scripts.auxillary as aux
import scripts.iodata as iod
from image_loader import render_image, get_image_from_pexel, download_image
from classes.classes import KosherType, DietType

# Simple App

st.title('DeepCook Web App')

st.write('Just press the button and DeepCook will give you a meal suggestion!')

# Filter Options
with st.expander("⚙️ Filter Options"):
    col1, col2 = st.columns(2)
    
    with col1:
        kosher_type = st.selectbox(
            "Kosher Type",
            options=["nonkosher", "parve", "milchik", "fleisch"],
            index=0,
            help="Filter by kosher dietary laws"
        )
    
    with col2:
        diet_type = st.selectbox(
            "Diet Type",
            options=["any", "vegan", "vegetarian", "glutenfree", "keto"],
            index=0,
            help="Filter by dietary preference"
        )

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
    
    # Apply filters sequentially
    filtered_meals = aux.filter_kosher(meals_db, KosherType[kosher_type])
    filtered_meals = aux.filter_diet(filtered_meals, DietType[diet_type])
    
    # Check if any meals match the filters
    if len(filtered_meals) == 0:
        st.warning("⚠️ No meals match your filter criteria. Try relaxing your filters.")
    else:
        _, chosen_one, chosen_idx = aux.choose_random(filtered_meals, rank=False, TA=None)
        st.write('Your random meal is: ', chosen_one)

        image_save_as = 'last_meal_img.jpg'
        image_data = get_image_from_pexel(chosen_one)
        image = download_image(image_data['url'], save_as=image_save_as)
        render_image(image_save_as)
        st.write(f'Photographer: {image_data["photographer"]}.\n')
        # print recipe suggestion if one exists
        suggestion = filtered_meals.iloc[chosen_idx].iloc[11]
        if isinstance(suggestion, str):
            st.write(f'Recipe suggestion: {suggestion}')
        elif isinstance(suggestion, float):
            st.write("No recipe suggestion exists in the database.")

        with open(counter_file, "w") as f:
            f.truncate()
            f.write(f"{counter}")

st.write(f"People that pressed on the button: {counter}")

#st.sidebar.success("success sidebar")
#st.sidebar.selectbox("Navigation Pane")
