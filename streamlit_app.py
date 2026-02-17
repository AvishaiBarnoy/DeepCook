import streamlit as st
import pandas as pd
from pathlib import Path

import scripts.auxillary as aux
import scripts.iodata as iod
from image_loader import render_image, get_image_from_pexel, download_image
from classes.classes import KosherType, DietType

st.set_page_config(page_title="DeepCook", page_icon="🍳", layout="centered")

# Language Toggle
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'

col_title, col_lang = st.columns([0.8, 0.2])
with col_lang:
    if st.button("🌐 " + ("Hebrew" if st.session_state.lang == 'EN' else "English")):
        st.session_state.lang = 'HE' if st.session_state.lang == 'EN' else 'EN'
        st.rerun()

# Translations
TRANS = {
    'title': {'EN': '🍳 DeepCook: Your Smart Meal Guide', 'HE': '🍳 דיפ-קוק: מדריך הארוחות החכם שלך'},
    'intro': {
        'EN': "Welcome to DeepCook! We help you decide what to eat based on your preferences, dietary laws, and what you haven't made lately.",
        'HE': "ברוכים הבאים לדיפ-קוק! אנחנו נעזור לכם להחליט מה לאכול על סמך ההעדפות שלכם, הכשרות, ומה שלא הכנתם לאחרונה."
    },
    'button': {'EN': '🎲 Get a Random Meal!', 'HE': '🎲 קבל הצעה לארוחה!'},
    'filters': {'EN': '⚙️ Filter Options', 'HE': '⚙️ אפשרויות סינון'},
    'last_made': {'EN': 'Exclude meals made in the past N days', 'HE': 'אל תציע ארוחות שהוכנו ב-N הימים האחרונים'},
    'kosher': {'EN': 'Kosher Type', 'HE': 'כשרות'},
    'diet': {'EN': 'Diet Type', 'HE': 'סוג דיאטה'},
    'ease': {'EN': 'Max Preparation Difficulty', 'HE': 'קושי הכנה מקסימלי'},
    'smarter': {'EN': 'Smarter Weighting', 'HE': 'שקלול חכם (גוון)'},
    'suggestion_prefix': {'EN': 'Your random meal is: ', 'HE': 'ההצעה שלך היא: '},
    'no_meal': {'EN': '⚠️ No meals match your filter criteria.', 'HE': '⚠️ אין ארוחות שמתאימות לסינון הנבחר.'},
    'recipe': {'EN': 'Recipe suggestion: ', 'HE': 'הצעת מתכון: '},
    'no_recipe': {'EN': 'No recipe suggestion exists.', 'HE': 'אין הצעת מתכון במאגר.'},
    'people_count': {'EN': 'People that pressed the button: ', 'HE': 'אנשים שלחצו על הכפתור: '},
    'crowd': {'EN': 'Cooking for a crowd? (High scaling)', 'HE': 'מבשלים להרבה אנשים? (יכולת הגדלה)'},
    'surprise_toggle': {'EN': 'Surprise Me! (New/Rare meals)', 'HE': 'הפתעות! (דברים חדשים/נדירים)'}
}

l = st.session_state.lang

st.title(TRANS['title'][l])
st.write(TRANS['intro'][l])

# Filter Options
with st.expander(TRANS['filters'][l]):
    last_made_days = st.slider(
        TRANS['last_made'][l],
        min_value=0,
        max_value=7,
        value=0
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        kosher_type = st.selectbox(
            TRANS['kosher'][l],
            options=["nonkosher", "parve", "milchik", "fleisch"],
            index=0
        )
        
        ease_value = st.slider(
            TRANS['ease'][l],
            min_value=1,
            max_value=10,
            value=10
        )
    
    with col2:
        diet_type = st.selectbox(
            TRANS['diet'][l],
            options=["any", "vegan", "vegetarian", "glutenfree", "keto"],
            index=0
        )
        
        smarter_weighting = st.checkbox(
            TRANS['smarter'][l],
            value=False
        )
        
        scaling_only = st.checkbox(
            TRANS['crowd'][l],
            value=False
        )
        
        surprise_me = st.checkbox(
            TRANS['surprise_toggle'][l],
            value=False
        )

MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent / MEAL_LIST
meals_db = pd.read_csv(absolute_path, index_col=0)
COUNTER_PATH = "data/counter.txt"
counter_file = Path(__file__).parent / COUNTER_PATH

# initiate counter
with open(counter_file, "r") as f:
    counter_data = f.readline()
    counter = 0 if counter_data == "" else int(counter_data)

if st.button(TRANS['button'][l], use_container_width=True, type="primary"):
    counter += 1
    
    # Use centralized filtering
    _, chosen_one, chosen_idx = aux.choose_random(
        meals_db, 
        rank=False, 
        last_made=last_made_days, 
        TA=None,
        kosher=KosherType[kosher_type],
        diet=DietType[diet_type],
        ease_cutoff=ease_value,
        times=smarter_weighting,
        scaling_only=scaling_only,
        surprise_me=surprise_me
    )
    
    if chosen_one is None:
        st.warning(TRANS['no_meal'][l])
    else:
        meal_row = meals_db.loc[chosen_idx]
        display_name = meal_row['Name_HE'] if l == 'HE' and isinstance(meal_row.get('Name_HE'), str) else chosen_one
        
        st.header(TRANS['suggestion_prefix'][l] + f"**{display_name}**")

        # Visuals
        try:
            image_save_as = 'last_meal_img.jpg'
            image_data = get_image_from_pexel(chosen_one)
            
            if image_data.get('url'):
                image = download_image(image_data['url'], save_as=image_save_as)
                st.image(image_save_as, use_container_width=True)
                st.caption(f'Photographer: {image_data["photographer"]}')
            else:
                st.info(f"📷 No image found for '{chosen_one}'")
        except Exception as e:
            st.error(f"📷 Image error: {str(e)}")
            st.info("Please check your PEXEL_API_KEY in .streamlit/secrets.toml")
        
        # Recipe
        recipe_url = aux.get_recipe_link(meal_row)
        if recipe_url:
            st.info(f"🔗 {TRANS['recipe'][l]} [Click here]({recipe_url})")
        else:
            st.caption(TRANS['no_recipe'][l])

        with open(counter_file, "w") as f:
            f.truncate()
            f.write(f"{counter}")

st.divider()
st.write(f"{TRANS['people_count'][l]} {counter}")
st.caption("DeepCook v1.2.0 - Internationalized Edition")
