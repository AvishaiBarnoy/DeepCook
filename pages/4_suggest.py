import streamlit as st
import pandas as pd
from pathlib import Path

# Language State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
l = st.session_state.lang

TRANS = {
    'title': {'EN': "📋 Recipe & Meal Suggestions", 'HE': "📋 הצעות למתכונים וארוחות"},
    'intro': {
        'EN': "Welcome to the suggestions page! Here you'll find helpful resources for meal planning and recipe inspiration.",
        'HE': "ברוכים הבאים לדף ההצעות! כאן תמצאו משאבים מועילים לתכנון ארוחות והשראה למתכונים."
    },
    'sources_header': {'EN': "👨‍🍳 Recommended Recipe Websites", 'HE': "👨‍🍳 אתרי מתכונים מומלצים"},
    'hebrew_sites': {'EN': "Hebrew Sites", 'HE': "אתרים בעברית"},
    'english_sites': {'EN': "English Sites", 'HE': "אתרים באנגלית"},
    'planning_header': {'EN': "📅 Meal Planning Tips", 'HE': "📅 טיפים לתכנון ארוחות"},
    'planning_strategy': {'EN': "Weekly Planning Strategy", 'HE': "אסטרטגיית תכנון שבועי"},
    'shopping_tips': {'EN': "Shopping List Tips", 'HE': "טיפים לרשימת קניות"},
    'time_saving': {'EN': "Time-Saving Hacks", 'HE': "טיפים לחיסכון בזמן"},
    'db_header': {'EN': "💡 Your Meal Ideas", 'HE': "💡 רעיונות מהמאגר שלכם"},
    'db_total': {'EN': "Total Meals in Database", 'HE': "סה''כ ארוחות במאגר"},
    'db_ta': {'EN': "Takeaway Options", 'HE': "אפשרויות משלוח"},
    'db_never': {'EN': "Never Made", 'HE': "מעולם לא הוכנו"},
    'top_ranked': {'EN': "🌟 Your Top-Ranked Meals", 'HE': "🌟 הארוחות המדורגות ביותר"},
    'most_made': {'EN': "🔥 Most Frequently Made", 'HE': "🔥 הארוחות הנפוצות ביותר"},
    'quick_header': {'EN': "⚡ Quick Meal Ideas", 'HE': "⚡ רעיונות לארוחות מהירות"},
    'm15': {'EN': "15-Minute Meals", 'HE': "ארוחות ב-15 דקות"},
    'm30': {'EN': "30-Minute Meals", 'HE': "ארוחות ב-30 דקות"},
    'tip': {'EN': "💡 Tip: Add these recipes to your DeepCook database for easy random selection!", 'HE': "💡 טיפ: הוסיפו את המתכונים האלה למאגר DeepCook שלכם לבחירה אקראית קלה!"}
}

st.title(TRANS['title'][l])
st.write(TRANS['intro'][l])

# Section 1: Popular Recipe Sources
st.header(TRANS['sources_header'][l])

col1, col2 = st.columns(2)

with col1:
    st.subheader(TRANS['hebrew_sites'][l])
    st.markdown("""
    - **[Kitchencoach](https://kitchencoach.co.il/)** - Professional recipes
    - **[Krutit](https://krutit.co.il/)** - Israeli food blog
    - **[10 Dakot](https://www.10dakot.co.il/)** - Quick meals
    - **[Mako Recipes](https://www.mako.co.il/food-recipes)** - Variety of dishes
    """)

with col2:
    st.subheader(TRANS['english_sites'][l])
    st.markdown("""
    - **[Serious Eats](https://www.seriouseats.com/)** - In-depth cooking
    - **[NYT Cooking](https://cooking.nytimes.com/)** - Curated recipes
    - **[Budget Bytes](https://www.budgetbytes.com/)** - Budget-friendly
    - **[AllRecipes](https://www.allrecipes.com/)** - Community favorites
    """)

# Section 2: Meal Planning Tips
st.header(TRANS['planning_header'][l])

with st.expander(TRANS['planning_strategy'][l]):
    if l == 'EN':
        st.markdown("""
        1. **Plan on weekends** - Dedicate 30 minutes to plan next week
        2. **Mix it up** - Alternate protein sources (meat, dairy, parve)
        3. **Batch cooking** - Make extras for easy midweek meals
        4. **Theme nights** - Pasta Monday, Taco Tuesday, etc.
        5. **Use your database** - Review what you haven't made recently
        """)
    else:
        st.markdown("""
        1. **תכננו בסופ"ש** - הקדישו 30 דקות לתכנון השבוע הבא
        2. **גוונות** - החליפו מקורות חלבון (בשרי, חלבי, פרווה)
        3. **בישול בכמויות** - הכינו תוספת לארוחות קלות באמצע השבוע
        4. **ערבים עם נושא** - פסטה בשני, טאקו בשלישי וכו'
        5. **השתמשו במאגר** - בדקו מה לא הכנתם בזמן האחרון
        """)

with st.expander(TRANS['shopping_tips'][l]):
    if l == 'EN':
        st.markdown("""
        - Check pantry before shopping to avoid duplicates
        - Buy seasonal produce for better prices and flavor
        - Plan meals around sales/discounts
        - Keep backup easy meals for emergencies
        - Stock staples: pasta, rice, canned tomatoes, onions, garlic
        """)
    else:
        st.markdown("""
        - בדקו את המזווה לפני הקניות כדי למנוע כפילויות
        - קנו תוצרת עונתית למחירים וטעם טובים יותר
        - תכננו ארוחות סביב מבצעים
        - שמרו מנות גיבוי קלות למקרי חירום
        - החזיקו מוצרי יסוד: פסטה, אורז, עגבניות משומרות, בצל, שום
        """)

with st.expander(TRANS['time_saving'][l]):
    if l == 'EN':
        st.markdown("""
        - **Prep vegetables on Sunday** for the whole week
        - **Use your freezer** - freeze portions, bread, herbs in ice cubes
        - **One-pot meals** - Less cleanup, more time
        - **Slow cooker** - Set it and forget it
        - **Mise en place** - Prep all ingredients before cooking
        """)
    else:
        st.markdown("""
        - **הכינו ירקות מראש בראשון** לכל השבוע
        - **השתמשו במקפיא** - הקפיאו מנות, לחם, עשבי תיבול בקוביות קרח
        - **ארוחות בסיר אחד** - פחות ניקיונות, יותר זמן
        - **סיר לבישול איטי** - שימו ושכחו
        - **Mise en place** - הכינו את כל המרכיבים לפני הבישול
        """)

# Section 3: From Your Database
st.header(TRANS['db_header'][l])

MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent.parent / MEAL_LIST

try:
    meals_db = pd.read_csv(absolute_path, index_col=0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(TRANS['db_total'][l], len(meals_db))
    
    with col2:
        if 'TA' in meals_db.columns:
            ta_count = len(meals_db[meals_db['TA'] == 1])
            st.metric(TRANS['db_ta'][l], ta_count)
    
    with col3:
        if 'times_made' in meals_db.columns:
            never_made = len(meals_db[meals_db['times_made'] == 0])
            st.metric(TRANS['db_never'][l], never_made)
    
    # Show top-ranked meals
    if 'Rank' in meals_db.columns:
        st.subheader(TRANS['top_ranked'][l])
        top_meals = meals_db.nlargest(5, 'Rank')
        for idx, meal in top_meals.iterrows():
            rank_str = f"Rank: {meal['Rank']}" if 'Rank' in meal else ""
            display_name = meal['Name_HE'] if l == 'HE' and isinstance(meal.get('Name_HE'), str) else meal['Name']
            st.write(f"⭐ **{display_name}** - {rank_str}")
    
    # Show most-made meals
    if 'times_made' in meals_db.columns and meals_db['times_made'].sum() > 0:
        st.subheader(TRANS['most_made'][l])
        most_made = meals_db.nlargest(5, 'times_made')
        for idx, meal in most_made.iterrows():
            if meal['times_made'] > 0:
                display_name = meal['Name_HE'] if l == 'HE' and isinstance(meal.get('Name_HE'), str) else meal['Name']
                times_text = "פעמים" if l == 'HE' else "times"
                st.write(f"🍽️ **{display_name}** - {meal['times_made']} {times_text}")

except FileNotFoundError:
    st.info("💡 Load your meal database to see personalized statistics!")
except Exception as e:
    st.warning(f"Could not load meal statistics: {str(e)}")

# Section 4: Quick Meal Ideas
st.header(TRANS['quick_header'][l])

with st.expander(TRANS['m15'][l]):
    if l == 'EN':
        st.markdown("""
        - **Pasta aglio e olio** - Garlic, olive oil, pasta, done
        - **Shakshuka** - Eggs in tomato sauce, serve with bread
        - **Stir-fry** - Any vegetables + protein + soy sauce
        - **Quesadillas** - Cheese, tortillas, whatever you have
        - **Omelet** - Eggs + cheese + vegetables
        """)
    else:
        st.markdown("""
        - **פסטה אליו אוליו** - שום, שמן זית, פסטה, וזהו
        - **שקשוקה** - ביצים ברוטב עגבניות, להגיש עם לחם
        - **מוקפץ** - כל ירק + חלבון + רוטב סויה
        - **קסדייה** - גבינה, טורטיות, מה שיש בבית
        - **חביתה משודרגת** - ביצים + גבינה + ירקות
        """)

with st.expander(TRANS['m30'][l]):
    if l == 'EN':
        st.markdown("""
        - **Sheet pan chicken** - Chicken + vegetables, roast together
        - **Curry** - Use curry paste, coconut milk, vegetables
        - **Tacos** - Ground meat, seasoning, toppings
        - **Fried rice** - Day-old rice + vegetables + egg + soy sauce
        - **Soup** - Broth + vegetables + protein, simmer
        """)
    else:
        st.markdown("""
        - **עוף בתבנית** - עוף + ירקות, לצלות ביחד
        - **קארי** - משחת קארי, חלב קוקוס, ירקות
        - **טאקו** - בשר טחון, תבלינים, תוספות
        - **אורז מטוגן** - אורז מאתמול + ירקות + ביצה + סויה
        - **מרק מהיר** - ציר + ירקות + חלבון, לבשל
        """)

st.markdown("---")
st.caption(TRANS['tip'][l])
