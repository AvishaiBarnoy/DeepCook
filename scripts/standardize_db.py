import pandas as pd
from pathlib import Path
import numpy as np

def standardize_database(file_path):
    print(f"Standardizing database: {file_path}")
    
    if not Path(file_path).exists():
        print(f"Error: {file_path} not found.")
        return False
        
    df = pd.read_csv(file_path, index_col=0)
    
    # Check if this is a "meal-like" file
    if 'Name' not in df.columns and 'meal_name' not in df.columns:
        print(f"Skipping {file_path} - not a standard meal file.")
        return False

    # 1. Standardize Names
    if 'meal_name' in df.columns and 'Name' not in df.columns:
        df.rename(columns={'meal_name': 'Name'}, inplace=True)

    # 1. Standardize Kosher column name
    if 'Kosher' in df.columns and 'KosherType' not in df.columns:
        print("Renaming 'Kosher' to 'KosherType'...")
        df.rename(columns={'Kosher': 'KosherType'}, inplace=True)
    elif 'Kosher' in df.columns and 'KosherType' in df.columns:
        print("Both 'Kosher' and 'KosherType' exist. Merging and dropping 'Kosher'...")
        df['KosherType'] = df['KosherType'].fillna(df['Kosher'])
        df.drop(columns=['Kosher'], inplace=True)

    # 2. Standardize KosherType values
    if 'KosherType' in df.columns:
        df['KosherType'] = df['KosherType'].astype(str).str.lower().replace('nan', 'nonkosher').fillna('nonkosher')
        # Map any numeric legacy values if they still exist
        mapping = {'0': "parve", '1': "parve", '2': "milchik", '3': "fleisch", '0.0': "parve", '1.0': "parve", '2.0': "milchik", '3.0': "fleisch"}
        df['KosherType'] = df['KosherType'].replace(mapping)

    # 3. Standardize Numeric Columns
    numeric_cols = {
        'Scaling': 0.0,
        'Rank': 5.0,
        'Prep_Ease': 5.0,
        'Kids': 0.0,
        'TA': 0.0,
        'times_made': 0.0
    }
    
    for col, default in numeric_cols.items():
        if col in df.columns:
            print(f"Standardizing numeric column: {col}")
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(default)
        else:
            # Only add missing columns to "meal" files that have most of the schema
            if 'KosherType' in df.columns or 'Prep_Ease' in df.columns:
                 print(f"Warning: Column '{col}' missing. Creating with default {default}.")
                 df[col] = default

    # 4. Clean up strings
    string_cols = ['Diet', 'Name_HE', 'recipe_suggestion']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].replace('NaN', '').replace('nan', '').fillna('')
            df[col] = df[col].astype(str).str.strip()

    # 5. Remove duplicates
    if 'Name' in df.columns:
        initial_len = len(df)
        df = df.drop_duplicates(subset=['Name'])
        if len(df) < initial_len:
            print(f"Removed {initial_len - len(df)} duplicate entries.")

    # 6. Save
    df.to_csv(file_path)
    print("Standardization complete.")
    return True

if __name__ == "__main__":
    DATA_DIR = Path(__file__).parent.parent / "data"
    # Whitelist of files that follow the standard meal schema
    whitelist = [
        "meal_list.csv", 
        "maincourses.csv", 
        "sidedishes.csv", 
        "salads.csv", 
        "soups.csv", 
        "sandwiches.csv"
    ]
    for filename in whitelist:
        csv_file = DATA_DIR / filename
        if csv_file.exists():
            standardize_database(csv_file)
