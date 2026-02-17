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

# --- Sidebar Documentation ---
with st.sidebar:
    st.header("📖 Schema Guide")
    st.markdown("""
    ### 🍽️ Meal Info
    - **Name**: English name of the meal.
    - **Name_HE**: Hebrew name of the meal.
    
    ### 🥬 Dietary & Physics
    - **KosherType**: `parve`, `milchik`, `fleisch`, or `nonkosher`.
    - **Diet**: String tag (`vegan`, `vegetarian`, `glutenfree`, `keto`). Leave empty if none.
    - **Rank**: Quality score from **1** (poor) to **10** (excellent).
    
    ### ⚙️ Toggle Fields (0 or 1)
    - **Scaling**: `1` = Good for crowds (large batches), `0` = Hard to scale.
    - **Kids**: `1` = Kid-friendly, `0` = Grownups mostly.
    - **TA**: `1` = Takeaway option, `0` = Home cooked.
    
    ### ⏱️ Difficulty & Time
    - **Prep_Ease**: Difficulty from **1** (Easiest) to **10** (Hardest).
    - **Prep_Time / Cook_Time**: Relative duration (`short`, `medium`, `long`).
    """)
    st.divider()
    st.caption("DeepCook Admin v1.1.0")


MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent.parent / MEAL_LIST

if absolute_path.exists():
    df = pd.read_csv(absolute_path, index_col=0)
    
    tab1, tab2 = st.tabs(["📊 Missing Data", "🔍 Full Database"])
    
    with tab1:
        st.subheader("Missing or Default Info")
        
        # Define missing/default criteria
        # Diet: empty/null
        # Scaling: null
        # Rank: null or exactly 5.0 (system default)
        # Prep_Ease: null or exactly 5.0 (system default)
        # Kids: null
        
        # Ensure columns exist to avoid KeyErrors
        cols = df.columns
        missing_diet = (df['Diet'].isna() | (df['Diet'].astype(str) == "")) if 'Diet' in cols else pd.Series(False, index=df.index)
        missing_scaling = df['Scaling'].isna() if 'Scaling' in cols else pd.Series(False, index=df.index)
        missing_rank = (df['Rank'].isna() | (df['Rank'] == 5.0)) if 'Rank' in cols else pd.Series(False, index=df.index)
        missing_ease = (df['Prep_Ease'].isna() | (df['Prep_Ease'] == 5.0)) if 'Prep_Ease' in cols else pd.Series(False, index=df.index)
        missing_kids = df['Kids'].isna() if 'Kids' in cols else pd.Series(False, index=df.index)
        
        to_fix = df[missing_diet | missing_scaling | missing_rank | missing_ease | missing_kids]
        
        if to_fix.empty:
            st.success("✨ Everything looks perfect! No missing or default data to fix.")
        else:
            st.warning(f"Found {len(to_fix)} meals that might need more details.")
            st.write("Double-click cells to edit. Values are saved locally to `meal_list.csv`.")
            
            # Focused editor
            all_edit_cols = ['Name', 'Name_HE', 'Diet', 'Scaling', 'Rank', 'Prep_Ease', 'Kids']
            available_edit_cols = [c for c in all_edit_cols if c in df.columns]
            
            edited_df = st.data_editor(
                to_fix[available_edit_cols],
                column_config={
                    "Diet": st.column_config.TextColumn("Diet (vegan, vegetarian, ...)"),
                    "Scaling": st.column_config.NumberColumn("Scaling (1=Large, 0=Small)", min_value=0, max_value=1),
                    "Rank": st.column_config.NumberColumn("Rank (1-10)", min_value=1, max_value=10),
                    "Prep_Ease": st.column_config.NumberColumn("Ease (1=Easy, 10=Hard)", min_value=1, max_value=10),
                    "Kids": st.column_config.NumberColumn("Kids (1=Yes, 0=No)", min_value=0, max_value=1),
                },
                use_container_width=True,
                num_rows="fixed",
                key="maintenance_editor"
            )
            
            if st.button("Save Maintenance Updates"):
                # Update main dataframe with edited values
                for idx, row in edited_df.iterrows():
                    for col in available_edit_cols:
                        df.at[idx, col] = row[col]
                
                df.to_csv(absolute_path)
                st.success("✅ Database updated!")
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
