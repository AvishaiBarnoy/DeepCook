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
            kids=False # Filter for non-kids specific meals if possible
        )
        
        if chosen_one:
            meal_row = meals_db.loc[chosen_idx]
            display_name = meal_row['Name_HE'] if l == 'HE' and isinstance(meal_row.get('Name_HE'), str) else chosen_one
            
            st.success(f"{TRANS['success_prefix'][l]} **{display_name}**")
            
            if l == 'EN' and 'Name_HE' in meal_row and isinstance(meal_row['Name_HE'], str):
                st.subheader(f"🇮🇱 {meal_row['Name_HE']}")
                
            if 'recipe_suggestion' in meal_row and isinstance(meal_row['recipe_suggestion'], str):
                st.info(f"🔗 [{TRANS['view_recipe'][l]}]({meal_row['recipe_suggestion']})")
        else:
            st.warning(TRANS['warning'][l])
else:
    st.error(TRANS['db_error'][l])
