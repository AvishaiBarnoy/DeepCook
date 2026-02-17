import streamlit as st
import pandas as pd
from pathlib import Path
import scripts.auxillary as aux
from classes.classes import KosherType, DietType

st.set_page_config(page_title="DeepCook Grownups", page_icon="🍷")

# Language State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
l = st.session_state.lang

TRANS = {
    'title': {'EN': "🍷 Grownups' Gourmet", 'HE': "🍷 גורמה למבוגרים"},
    'intro': {'EN': "Sophisticated meal suggestions for the adults.", 'HE': "הצעות לארוחות מתוחכמות למבוגרים."},
    'filters': {'EN': "⚙️ Advanced Filters", 'HE': "⚙️ מסננים מתקדמים"},
    'kosher': {'EN': "Kosher Type", 'HE': "כשרות"},
    'diet': {'EN': "Diet Type", 'HE': "סוג דיאטה"},
    'rank': {'EN': "Minimum Rank", 'HE': "דירוג מינימלי"},
    'smarter': {'EN': "Smarter Weighting", 'HE': "שקלול חכם"},
    'button': {'EN': "Surprise Me!", 'HE': "הפתע אותי!"},
    'success_prefix': {'EN': "Tonight's recommendation: ", 'HE': "ההמלצה להערב: "},
    'view_recipe': {'EN': "View Recipe", 'HE': "צפה במתכון"},
    'warning': {'EN': "No sophisticated meals found with those filters. Try relaxing them!", 'HE': "לא נמצאו ארוחות מתוחכמות בסינון הזה. נסו להקל על הסינון!"},
    'db_error': {'EN': "Meal database not found!", 'HE': "מאגר הארוחות לא נמצא!"}
}

st.title(TRANS['title'][l])

# Sophisticated Theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #F8F9FA;
    }
    .main {
        background: linear-gradient(180deg, #F8F9FA 0%, #E9ECEF 100%);
    }
    h1 {
        color: #1A1A1A !important;
        font-family: 'DM Serif Display', serif;
        font-weight: 400;
        letter-spacing: -0.5px;
    }
    .stButton>button {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .gourmet-card {
        background-color: white;
        padding: 2.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #1A1A1A;
        margin: 2rem 0;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=DM+Serid+Display&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.write(TRANS['intro'][l])

MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent.parent / MEAL_LIST

if absolute_path.exists():
    meals_db = pd.read_csv(absolute_path, index_col=0)
    
    with st.expander(TRANS['filters'][l]):
        kosher_type = st.selectbox(TRANS['kosher'][l], ["nonkosher", "parve", "milchik", "fleisch"], index=0)
        diet_type = st.selectbox(TRANS['diet'][l], ["any", "vegan", "vegetarian", "glutenfree", "keto"], index=0)
        min_rank = st.slider(TRANS['rank'][l], 1, 10, 7)
        smarter = st.checkbox(TRANS['smarter'][l], value=True)

    if st.button(TRANS['button'][l], type="primary"):
        # For grownups, maybe we exclude kid-only meals or just show everything
        _, chosen_one, chosen_idx = aux.choose_random(
            meals_db,
            kosher=KosherType[kosher_type],
            diet=DietType[diet_type],
            rank=True,
            times=smarter,
            kids=False, # Filter for non-kids specific meals
            surprise_me=True
        )
        
        if chosen_one:
            meal_row = meals_db.loc[chosen_idx]
            display_name = meal_row['Name_HE'] if l == 'HE' and isinstance(meal_row.get('Name_HE'), str) else chosen_one
            
            st.markdown(f"""
            <div class="gourmet-card">
                <p style="text-transform: uppercase; letter-spacing: 2px; color: #868E96; font-size: 0.8rem; margin-bottom: 0.5rem;">{TRANS['success_prefix'][l]}</p>
                <h2 style="margin-top: 0; color: #1A1A1A; font-family: serif;">{display_name}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if l == 'EN' and 'Name_HE' in meal_row and isinstance(meal_row['Name_HE'], str) and meal_row['Name_HE'] != "":
                 st.markdown(f"<p style='font-style: italic; color: #495057;'>🇮🇱 {meal_row['Name_HE']}</p>", unsafe_allow_html=True)
                
            # Recipe Link for Grownups
            recipe_url = aux.get_recipe_link(meal_row, preferred_site='kitchencoach')
            if recipe_url:
                st.info(f"🔗 [{TRANS['view_recipe'][l]}]({recipe_url})")
        else:
            st.warning(TRANS['warning'][l])
else:
    st.error(TRANS['db_error'][l])
