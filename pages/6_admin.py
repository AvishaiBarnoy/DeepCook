import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="DeepCook Admin", page_icon="🛠️")

# Language State (simple for admin)
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
l = st.session_state.lang

st.title("🛠️ Maintenance Dashboard")
st.write("Keep the meal database healthy by filling in missing information.")

MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent.parent / MEAL_LIST

if absolute_path.exists():
    df = pd.read_csv(absolute_path, index_col=0)
    
    tab1, tab2 = st.tabs(["📊 Missing Data", "🔍 Full Database"])
    
    with tab1:
        st.subheader("Missing Diet/Scaling Info")
        
        # Find missing values
        # Diet is missing if it's NaN or empty string
        # Scaling is missing if it's NaN
        missing_diet = df['Diet'].isna() | (df['Diet'] == "")
        missing_scaling = df['Scaling'].isna()
        
        to_fix = df[missing_diet | missing_scaling]
        
        if to_fix.empty:
            st.success("All caught up! No missing Diet or Scaling data.")
        else:
            st.warning(f"Found {len(to_fix)} meals needing attention.")
            
            # Use data editor for quick fixes
            st.write("Double-click to edit. Diet options: vegan, vegetarian, glutenfree, keto. Scaling: 1.0 (good), 0.0 (bad)")
            edited_df = st.data_editor(to_fix[['Name', 'Name_HE', 'Diet', 'Scaling']])
            
            if st.button("Save Changes to Missing Only"):
                # Update the main dataframe
                for idx, row in edited_df.iterrows():
                    df.at[idx, 'Diet'] = row['Diet']
                    df.at[idx, 'Scaling'] = row['Scaling']
                
                df.to_csv(absolute_path)
                st.success("Database updated!")
                st.rerun()

    with tab2:
        st.subheader("Entire Database")
        full_edited = st.data_editor(df)
        
        if st.button("Save All Changes"):
            full_edited.to_csv(absolute_path)
            st.success("Full database updated!")
            st.rerun()

else:
    st.error("Meal database not found!")

st.info("💡 Pro Tip: Keeping 'Scaling' updated helps when cooking for crowds. 'Diet' helps for guests with restrictions.")
