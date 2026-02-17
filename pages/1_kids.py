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

# Playful Theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #FFF5F5;
    }
    .main {
        background: linear-gradient(135deg, #FFF5F5 0%, #FFF0F6 100%);
    }
    h1 {
        color: #FF6B6B !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px #FFE3E3;
    }
    .stButton>button {
        background-color: #4DABF7 !important;
        color: white !important;
        border-radius: 20px !important;
        border: 2px solid #339AF0 !important;
        font-weight: bold !important;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05) rotate(-1deg);
        background-color: #339AF0 !important;
    }
    .kids-card {
        background-color: white;
        padding: 20px;
        border-radius: 25px;
        border: 4px dashed #FFD43B;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

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
            kids=True,
            times=True,
            surprise_me=True
        )
        
        if chosen_one:
            meal_row = meals_db.loc[chosen_idx]
            display_name = meal_row['Name_HE'] if l == 'HE' and isinstance(meal_row.get('Name_HE'), str) else chosen_one
            
            st.markdown(f"""
            <div class="kids-card">
                <h2 style="margin:0;">Yay!</h2>
                <p style="font-size: 1.5rem; color: #4DABF7;">{TRANS['success'][l]}</p>
                <p style="font-size: 2.5rem; font-weight: bold; color: #FF6B6B;">{display_name}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if l == 'EN' and 'Name_HE' in meal_row and isinstance(meal_row['Name_HE'], str) and meal_row['Name_HE'] != "":
                st.markdown(f"<p style='text-align:center; font-size:1.5rem; color:#868E96;'>🇮🇱 {meal_row['Name_HE']}</p>", unsafe_allow_html=True)
                
            # Recipe Link for Kids
            recipe_url = aux.get_recipe_link(meal_row, preferred_site='nikib') # NikiB is very kid-friendly
            if recipe_url:
                st.markdown(f"<div style='text-align:center;'><a href='{recipe_url}' target='_blank'>👩‍🍳 View Recipe for Parents</a></div>", unsafe_allow_html=True)
                
            st.balloons()
        else:
            st.warning(TRANS['warning'][l])
else:
    st.error(TRANS['db_error'][l])
