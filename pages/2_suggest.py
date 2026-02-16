import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📋 Recipe & Meal Suggestions")

st.markdown("""
Welcome to the suggestions page! Here you'll find helpful resources 
for meal planning and recipe inspiration.
""")

# Section 1: Popular Recipe Sources
st.header("👨‍🍳 Recommended Recipe Websites")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hebrew Sites")
    st.markdown("""
    - **[Kitchencoach](https://kitchencoach.co.il/)** - Professional recipes
    - **[Krutit](https://krutit.co.il/)** - Israeli food blog
    - **[10 Dakot](https://www.10dakot.co.il/)** - Quick meals
    - **[Mako Recipes](https://www.mako.co.il/food-recipes)** - Variety of dishes
    """)

with col2:
    st.subheader("English Sites")
    st.markdown("""
    - **[Serious Eats](https://www.seriouseats.com/)** - In-depth cooking
    - **[NYT Cooking](https://cooking.nytimes.com/)** - Curated recipes
    - **[Budget Bytes](https://www.budgetbytes.com/)** - Budget-friendly
    - **[AllRecipes](https://www.allrecipes.com/)** - Community favorites
    """)

# Section 2: Meal Planning Tips
st.header("📅 Meal Planning Tips")

with st.expander("Weekly Planning Strategy"):
    st.markdown("""
    1. **Plan on weekends** - Dedicate 30 minutes to plan next week
    2. **Mix it up** - Alternate protein sources (meat, dairy, parve)
    3. **Batch cooking** - Make extras for easy midweek meals
    4. **Theme nights** - Pasta Monday, Taco Tuesday, etc.
    5. **Use your database** - Review what you haven't made recently
    """)

with st.expander("Shopping List Tips"):
    st.markdown("""
    - Check pantry before shopping to avoid duplicates
    - Buy seasonal produce for better prices and flavor
    - Plan meals around sales/discounts
    - Keep backup easy meals for emergencies
    - Stock staples: pasta, rice, canned tomatoes, onions, garlic
    """)

with st.expander("Time-Saving Hacks"):
    st.markdown("""
    - **Prep vegetables on Sunday** for the whole week
    - **Use your freezer** - freeze portions, bread, herbs in ice cubes
    - **One-pot meals** - Less cleanup, more time
    - **Slow cooker** - Set it and forget it
    - **Mise en place** - Prep all ingredients before cooking
    """)

# Section 3: From Your Database
st.header("💡 Your Meal Ideas")

MEAL_LIST = "../data/meal_list.csv"
absolute_path = Path(__file__).parent.parent / MEAL_LIST

try:
    meals_db = pd.read_csv(absolute_path, index_col=0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Meals in Database", len(meals_db))
    
    with col2:
        if 'TA' in meals_db.columns:
            ta_count = len(meals_db[meals_db['TA'] == 1])
            st.metric("Takeaway Options", ta_count)
    
    with col3:
        if 'times_made' in meals_db.columns:
            never_made = len(meals_db[meals_db['times_made'] == 0])
            st.metric("Never Made", never_made)
    
    # Show top-ranked meals
    if 'Rank' in meals_db.columns:
        st.subheader("🌟 Your Top-Ranked Meals")
        top_meals = meals_db.nlargest(5, 'Rank')
        for idx, meal in top_meals.iterrows():
            rank_str = f"Rank: {meal['Rank']}" if 'Rank' in meal else ""
            st.write(f"⭐ **{meal['Name']}** - {rank_str}")
    
    # Show most-made meals
    if 'times_made' in meals_db.columns and meals_db['times_made'].sum() > 0:
        st.subheader("🔥 Most Frequently Made")
        most_made = meals_db.nlargest(5, 'times_made')
        for idx, meal in most_made.iterrows():
            if meal['times_made'] > 0:
                st.write(f"🍽️ **{meal['Name']}** - {meal['times_made']} times")

except FileNotFoundError:
    st.info("💡 Load your meal database to see personalized statistics!")
except Exception as e:
    st.warning(f"Could not load meal statistics: {str(e)}")

# Section 4: Quick Meal Ideas
st.header("⚡ Quick Meal Ideas")

with st.expander("15-Minute Meals"):
    st.markdown("""
    - **Pasta aglio e olio** - Garlic, olive oil, pasta, done
    - **Shakshuka** - Eggs in tomato sauce, serve with bread
    - **Stir-fry** - Any vegetables + protein + soy sauce
    - **Quesadillas** - Cheese, tortillas, whatever you have
    - **Omelet** - Eggs + cheese + vegetables
    """)

with st.expander("30-Minute Meals"):
    st.markdown("""
    - **Sheet pan chicken** - Chicken + vegetables, roast together
    - **Curry** - Use curry paste, coconut milk, vegetables
    - **Tacos** - Ground meat, seasoning, toppings
    - **Fried rice** - Day-old rice + vegetables + egg + soy sauce
    - **Soup** - Broth + vegetables + protein, simmer
    """)

st.markdown("---")
st.caption("💡 Tip: Add these recipes to your DeepCook database for easy random selection!")
