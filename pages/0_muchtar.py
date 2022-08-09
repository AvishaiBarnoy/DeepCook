import streamlit as st
import pandas as pd
from pathlib import Path

muchtar_file = "../data/muchtar_list.csv"
muchtar_path = Path(__file__).parent / muchtar_file
muchtar_db = pd.read_csv(muchtar_path)

muchtar_meal = muchtar_db.sample()

meal_name = muchtar_meal.iloc[0].iloc[0]
price = muchtar_meal.iloc[0].iloc[1]

if st.button('מנה מהדר מוכתר'):
    st.write(f"""
        {meal_name} בעלות זניחה של {price}""")
