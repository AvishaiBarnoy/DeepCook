import streamlit as st
import pandas as pd
from pathlib import Path
import scripts.auxillary as aux
from classes.classes import KosherType, DietType

st.set_page_config(page_title="DeepCook Kids", page_icon="👶")

# Language State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
l = st.session_state.lang

TRANS = {
    'title': {'EN': "👶 Kids' Corner", 'HE': "👶 פינת הילדים"},
    'intro': {'EN': "Finding something the kids will actually eat!", 'HE': "מוצאים משהו שהילדים באמת יאכלו!"},
    'filters': {'EN': "⚙️ Kids' Filter Options", 'HE': "⚙️ אפשרויות סינון לילדים"},
    'kosher': {'EN': "Kosher Type", 'HE': "כשרות"},
    'diet': {'EN': "Diet Type", 'HE': "סוג דיאטה"},
    'ease': {'EN': "Max Difficulty for Parent", 'HE': "קושי הכנה מקסימלי להורה"},
    'button': {'EN': "Get Kids' Meal!", 'HE': "קבל ארוחה לילדים!"},
    'success': {'EN': "How about: ", 'HE': "מה דעתכם על: "},
    'warning': {'EN': "No kid-friendly meals found with those filters. Try relaxing them!", 'HE': "לא נמצאו ארוחות מתאימות לילדים בסינון הזה. נסו להקל על הסינון!"},
    'db_error': {'EN': "Meal database not found!", 'HE': "מאגר הארוחות לא נמצא!"}
}

st.title(TRANS['title'][l])
st.write(TRANS['intro'][l])

MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent.parent / MEAL_LIST

if absolute_path.exists():
    meals_db = pd.read_csv(absolute_path, index_col=0)
    
    with st.expander(TRANS['filters'][l]):
        kosher_type = st.selectbox(TRANS['kosher'][l], ["nonkosher", "parve", "milchik", "fleisch"], index=0)
        diet_type = st.selectbox(TRANS['diet'][l], ["any", "vegan", "vegetarian", "glutenfree", "keto"], index=0)
        max_ease = st.slider(TRANS['ease'][l], 1, 10, 5)

    if st.button(TRANS['button'][l], type="primary"):
        _, chosen_one, chosen_idx = aux.choose_random(
            meals_db,
            kosher=KosherType[kosher_type],
            diet=DietType[diet_type],
            ease_cutoff=max_ease,
            kids=True
        )
        
        if chosen_one:
            meal_row = meals_db.loc[chosen_idx]
            display_name = meal_row['Name_HE'] if l == 'HE' and isinstance(meal_row.get('Name_HE'), str) else chosen_one
            
            st.success(f"{TRANS['success'][l]} **{display_name}**?")
            
            if l == 'EN' and 'Name_HE' in meal_row and isinstance(meal_row['Name_HE'], str):
                st.subheader(f"🇮🇱 {meal_row['Name_HE']}")
                
            st.balloons()
        else:
            st.warning(TRANS['warning'][l])
else:
    st.error(TRANS['db_error'][l])
