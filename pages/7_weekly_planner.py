import streamlit as st
import pandas as pd
from pathlib import Path
import scripts.auxillary as aux
from classes.classes import KosherType, DietType

st.set_page_config(page_title="DeepCook Weekly Planner", page_icon="🗓️", layout="wide")

# Language State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
l = st.session_state.lang

# Days of the week
DAYS = {
    'EN': ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    'HE': ["יום ראשון", "יום שני", "יום שלישי", "יום רביעי", "יום חמישי", "יום שישי", "שבת"]
}

TRANS = {
    'title': {'EN': "🗓️ Weekly Meal Planner", 'HE': "🗓️ מתכנן ארוחות שבועי"},
    'intro': {'EN': "Plan your entire week in one click. Lock your favorites and regenerate the rest!", 'HE': "תכננו את כל השבוע בלחיצה אחת. נעלו את האהובים עליכם וצרו מחדש את השאר!"},
    'filters': {'EN': "⚙️ Global Weekly Filters", 'HE': "⚙️ מסנני שבוע כלליים"},
    'kosher': {'EN': "Kosher Type", 'HE': "כשרות"},
    'diet': {'EN': "Diet Type", 'HE': "סוג דיאטה"},
    'leftovers': {'EN': "Leftover Friendly (Repeats large mains)", 'HE': "ידידותי לשאריות (חוזר על עיקריות גדולות)"},
    'gen_button': {'EN': "Generate Full Week", 'HE': "צור תוכנית שבועית"},
    'lock': {'EN': "Lock", 'HE': "נעל"},
    'reload': {'EN': "🔄 Reload Day", 'HE': "🔄 החלף יום"},
    'main': {'EN': "Main", 'HE': "עיקרית"},
    'side': {'EN': "Side", 'HE': "תוספת"},
    'salad': {'EN': "Salad", 'HE': "סלט"},
    'db_error': {'EN': "Meal database not found!", 'HE': "מאגר הארוחות לא נמצא!"},
    'summary': {'EN': "Weekly Summary", 'HE': "סיכום שבועי"},
    'export': {'EN': "💾 Download Meal Plan", 'HE': "💾 הורד תוכנית ארוחות"}
}

st.title(TRANS['title'][l])
st.write(TRANS['intro'][l])

DATA_DIR = Path(__file__).parent.parent / "data"
MEAL_DB_PATH = DATA_DIR / "meal_list.csv"

# Initialize Session State for the plan
if 'weekly_plan' not in st.session_state:
    st.session_state.weekly_plan = {day: None for day in DAYS['EN']}

if 'locked_days' not in st.session_state:
    st.session_state.locked_days = {day: False for day in DAYS['EN']}

# Meals DB Loading logic...

if MEAL_DB_PATH.exists():
    meals_db = pd.read_csv(MEAL_DB_PATH, index_col=0)
    
    with st.sidebar:
        st.header(TRANS['filters'][l])
        kosher_type = st.selectbox(TRANS['kosher'][l], ["nonkosher", "parve", "milchik", "fleisch"], index=0)
        diet_type = st.selectbox(TRANS['diet'][l], ["any", "vegan", "vegetarian", "glutenfree", "keto"], index=0)
        leftover_mode = st.toggle(TRANS['leftovers'][l], value=True)
        
        if st.button(TRANS['gen_button'][l], type="primary", use_container_width=True):
            prev_main = None
            new_plan = st.session_state.weekly_plan.copy()
            for day_en in DAYS['EN']:
                if not st.session_state.locked_days[day_en]:
                    meal = aux.get_meal_for_day(meals_db, KosherType[kosher_type], DietType[diet_type], prev_main, leftover_mode)
                    new_plan[day_en] = meal
                    prev_main = meal
                else:
                    prev_main = st.session_state.weekly_plan[day_en]
            st.session_state.weekly_plan = new_plan

    # Display the grid
    cols = st.columns(7) if l == 'EN' else st.columns(7)[::-1]
    
    for i, day_en in enumerate(DAYS['EN']):
        with cols[i]:
            day_display = DAYS[l][i]
            st.subheader(day_display)
            
            # Lock Toggle
            st.session_state.locked_days[day_en] = st.checkbox(f"{TRANS['lock'][l]} ##{day_en}", value=st.session_state.locked_days[day_en], key=f"lock_{day_en}", label_visibility="collapsed")
            st.caption(f"{TRANS['lock'][l]}" if not st.session_state.locked_days[day_en] else f"🔒 {TRANS['lock'][l]}")

            meal = st.session_state.weekly_plan[day_en]
            if meal:
                meal_name = meal['Name_HE'] if l == 'HE' and isinstance(meal.get('Name_HE'), str) and meal['Name_HE'] != '' else meal['Name']
                st.info(f"**{meal_name}**")
                
                # Show metadata
                tags = []
                if meal.get('KosherType'): tags.append(f"🏷️ {meal['KosherType']}")
                if meal.get('Prep_Ease'): tags.append(f"⏳ Ease: {int(meal['Prep_Ease'])}")
                if tags: st.caption(" | ".join(tags))
                
                if st.button(TRANS['reload'][l], key=f"reload_{day_en}", disabled=st.session_state.locked_days[day_en]):
                    st.session_state.weekly_plan[day_en] = aux.get_meal_for_day(meals_db, KosherType[kosher_type], DietType[diet_type])
                    st.rerun()
            else:
                st.write("---")
                
    st.divider()
    
    # Simple Export/Summary
    if any(st.session_state.weekly_plan.values()):
        with st.expander(TRANS['summary'][l]):
            summary_text = ""
            for i, day_en in enumerate(DAYS['EN']):
                meal = st.session_state.weekly_plan[day_en]
                if meal:
                    meal_name = meal['Name_HE'] if l == 'HE' and isinstance(meal.get('Name_HE'), str) and meal['Name_HE'] != '' else meal['Name']
                    summary_text += f"### {DAYS[l][i]}\n"
                    summary_text += f"- **{TRANS['main'][l]}**: {meal_name}\n"
                    
                    # Smart Recipe Link fallback
                    recipe_url = aux.get_recipe_link(meal)
                    if recipe_url:
                         summary_text += f"  - 🔗 {recipe_url}\n"
                    summary_text += "\n"
            st.markdown(summary_text)
            
            # Export as file
            file_name = f"meal_plan_{pd.Timestamp.now().strftime('%Y%m%d')}.txt"
            st.download_button(
                label=TRANS['export'][l],
                data=summary_text,
                file_name=file_name,
                mime="text/plain",
                use_container_width=True
            )

else:
    st.error(TRANS['db_error'][l])
