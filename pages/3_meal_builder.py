import streamlit as st
import pandas as pd
from pathlib import Path
import scripts.auxillary as aux
from classes.classes import KosherType, DietType

st.set_page_config(page_title="DeepCook Meal Builder", page_icon="🏗️")

# Language State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
l = st.session_state.lang

TRANS = {
    'title': {'EN': "🏗️ Meal Builder", 'HE': "🏗️ בונה הארוחות"},
    'intro': {'EN': "Generate a complete meal by combining a main course, a side dish, and a salad.", 'HE': "צרו ארוחה שלמה על ידי שילוב של מנה עיקרית, תוספת וסלט."},
    'filters': {'EN': "⚙️ Filter Options", 'HE': "⚙️ אפשרויות סינון"},
    'kosher': {'EN': "Kosher Type", 'HE': "כשרות"},
    'diet': {'EN': "Diet Type", 'HE': "סוג דיאטה"},
    'button': {'EN': "Build a Meal!", 'HE': "בנו ארוחה!"},
    'main': {'EN': "🥩 Main", 'HE': "🥩 עיקרית"},
    'side': {'EN': "🍚 Side", 'HE': "🍚 תוספת"},
    'salad': {'EN': "🥗 Salad", 'HE': "🥗 סלט"},
    'no_main': {'EN': "No main courses found", 'HE': "לא נמצאו מנות עיקריות"},
    'no_side': {'EN': "No side dishes found", 'HE': "לא נמצאו תוספות"},
    'no_salad': {'EN': "No salads found", 'HE': "לא נמצאו סלטים"},
    'result_prefix': {'EN': "**Your Meal:** ", 'HE': "**הארוחה שלכם:** "},
    'with': {'EN': " with ", 'HE': " עם "},
    'and': {'EN': " and ", 'HE': " וגם "},
    'tip': {'EN': "💡 You can add more items to the subunit files in the `data/` directory to improve suggestions.", 'HE': "💡 ניתן להוסיף פריטים נוספים לקבצי היחידות בספריית `data/` כדי לשפר את ההצעות."}
}

st.title(TRANS['title'][l])
st.write(TRANS['intro'][l])

DATA_DIR = Path(__file__).parent.parent / "data"

def load_data(filename):
    path = DATA_DIR / filename
    if path.exists():
        return pd.read_csv(path, index_col=0)
    return pd.DataFrame()

main_df = load_data("maincourses.csv")
side_df = load_data("sidedishes.csv")
salad_df = load_data("salads.csv")

# Filter Options
with st.expander(TRANS['filters'][l]):
    kosher_type = st.selectbox(
        TRANS['kosher'][l],
        options=["nonkosher", "parve", "milchik", "fleisch"],
        index=0
    )
    
    diet_type = st.selectbox(
        TRANS['diet'][l],
        options=["any", "vegan", "vegetarian", "glutenfree", "keto"],
        index=0
    )

if st.button(TRANS['button'][l], type="primary"):
    cols = st.columns(3)
    
    # 1. Choose Main
    if not main_df.empty:
        _, main_name, main_idx = aux.choose_random(
            main_df, 
            kosher=KosherType[kosher_type], 
            diet=DietType[diet_type]
        )
        if main_name:
            row = main_df.loc[main_idx]
            main_name = row['Name_HE'] if l == 'HE' and isinstance(row.get('Name_HE'), str) else main_name
    else:
        main_name = TRANS['no_main'][l]
        
    # 2. Choose Side
    if not side_df.empty:
        _, side_name, side_idx = aux.choose_random(
            side_df, 
            kosher=KosherType[kosher_type], 
            diet=DietType[diet_type]
        )
        if side_name:
            row = side_df.loc[side_idx]
            side_name = row['Name_HE'] if l == 'HE' and isinstance(row.get('Name_HE'), str) else side_name
    else:
        side_name = TRANS['no_side'][l]
        
    # 3. Choose Salad
    if not salad_df.empty:
        _, salad_name, salad_idx = aux.choose_random(
            salad_df, 
            kosher=KosherType[kosher_type], 
            diet=DietType[diet_type]
        )
        if salad_name:
            row = salad_df.loc[salad_idx]
            salad_name = row['Name_HE'] if l == 'HE' and isinstance(row.get('Name_HE'), str) else salad_name
    else:
        salad_name = TRANS['no_salad'][l]
        
    with cols[0]:
        st.subheader(TRANS['main'][l])
        st.info(main_name)
    
    with cols[1]:
        st.subheader(TRANS['side'][l])
        st.info(side_name)
        
    with cols[2]:
        st.subheader(TRANS['salad'][l])
        st.info(salad_name)
    
    st.success(f"{TRANS['result_prefix'][l]} {main_name} {TRANS['with'][l]} {side_name} {TRANS['and'][l]} {salad_name}")

st.markdown("---")
st.info(TRANS['tip'][l])
