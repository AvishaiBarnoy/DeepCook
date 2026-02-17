'''
Functions for data input/ouput and update of data
This whole library needs to undergo a thorough revamp and remodelling, removing redundant and depracted code parts, adding new functionality, descriptions, etc.
'''

import pandas as pd
import os
from pathlib import Path

def add_meal(data, new_data):
    '''
    concats a new meal into a meal data set
    '''
    new_ideas = pd.concat([data,new_data], ignore_index = True, axis = 0)
    return new_ideas

def meal_questions(meal_data):
    '''
    Ask user to enter information about meal, then stores in the data model.
    Includes input validation.
    '''
    print("\n" + "="*30)
    print("ADDING NEW MEAL TO DATABASE")
    print("="*30)
    print("Please follow the prompts to add a new meal.")
    print("Enter 'q' at any time to cancel.\n")

    data = meal_data
    inp = {key: "NaN" for key in data.columns}
    cols_to_skip = ["Timestamp", "times_made"]
    
    # Define valid options for specific columns
    valid_options = {
        "KosherType": ["parve", "milchik", "fleisch", "nonkosher"],
        "Prep_Time": ["short", "medium", "long"],
        "Cook_Time": ["short", "medium", "long"],
        "TA": ["0", "1"],
        "Kids": ["0", "1"],
        "Scaling": ["0.0", "1.0", "0", "1"],
        "Rank": [str(i) for i in range(1, 11)],
        "Prep_Ease": [str(i) for i in range(1, 11)]
    }

    for col in data.columns:
        if col in cols_to_skip:
            inp[col] = "NaN" if col == "Timestamp" else 0
            continue
            
        while True:
            prompt = f"Enter value for {col}"
            if col in valid_options:
                prompt += f" ({'/'.join(valid_options[col])})"
            
            val = input(f"{prompt}: ").strip()
            
            if val.lower() == 'q':
                print("Operation cancelled.")
                return None
            
            # Basic validation
            is_valid, msg = check_meal_inp(col, val, valid_options)
            if is_valid:
                inp[col] = val
                break
            else:
                print(f"❌ Invalid input: {msg}. Please try again.")

    print("\nNew meal summary:")
    for k, v in inp.items():
        if k not in cols_to_skip:
            print(f"  {k}: {v}")
    
    confirm = input("\nSave this meal? (y/n): ").lower()
    if confirm == 'y':
        return pd.DataFrame([inp])
    else:
        print("Meal not saved.")
        return None

def check_meal_inp(col, val, valid_options):
    '''
    Check if a value is valid for a given column.
    Returns (bool, message)
    '''
    # Allow empty only for Diet or optional fields if we decide so, 
    # but for now let's be strict except for specific ones.
    if not val and col not in ["Diet", "recipe_suggestion", "Name_HE"]:
        return False, "Value cannot be empty"
        
    if col in valid_options:
        if val not in valid_options[col]:
            return False, f"Must be one of: {', '.join(valid_options[col])}"
            
    if col in ["Rank", "Prep_Ease"]:
        try:
            r = int(float(val))
            if not 1 <= r <= 10:
                return False, f"{col} must be between 1 and 10"
        except ValueError:
            return False, f"{col} must be an integer"
            
    if col == "Diet":
        # Check if tags are valid
        valid_tags = ["vegan", "vegetarian", "glutenfree", "keto"]
        tags = [t.strip().lower() for t in val.split(',') if t.strip()]
        for tag in tags:
            if tag not in valid_tags:
                return False, f"Unknown diet tag '{tag}'. Valid: {', '.join(valid_tags)}"

    return True, "OK"

def write_to_log(choice,logfile="meal.log"):
    '''
    Appends a prepared eal to meal log
    '''
    now = str(pd.Timestamp.now())
    log = "{},{}\n".format(choice,now)
    with open(f"data/{logfile}","a") as f:
        f.writelines(log)

def maintenance_wizard(data, file_path=None):
    '''
    A CLI-based wizard to fill in missing or default data.
    '''
    print("\n" + "🧙" * 15)
    print("DATABASE MAINTENANCE WIZARD")
    print("🧙" * 15)
    
    valid_options = {
        "KosherType": ["parve", "milchik", "fleisch", "nonkosher"],
        "Prep_Time": ["short", "medium", "long"],
        "Cook_Time": ["short", "medium", "long"],
        "TA": ["0", "1", 0, 1],
        "Kids": ["0", "1", 0, 1],
        "Scaling": ["0.0", "1.0", "0", "1", 0.0, 1.0, 0, 1],
        "Rank": [str(i) for i in range(1, 11)] + list(range(1, 11)),
        "Prep_Ease": [str(i) for i in range(1, 11)] + list(range(1, 11))
    }

    modified = False
    
    for idx, row in data.iterrows():
        meal_name = row.get('Name_HE', row.get('Name', 'Unknown'))
        needs_attention = False
        
        # Check for missing or placeholder values in key columns
        # We define "placeholders" as things that might have been auto-filled
        check_cols = ["Diet", "Scaling", "Prep_Ease", "Rank", "Kids"]
        
        for col in check_cols:
            if col not in data.columns: continue
            
            val = row[col]
            is_placeholder = False
            
            if pd.isna(val) or val == "" or val == "NaN" or val == "nan":
                is_placeholder = True
            elif col == "Rank" and float(val) == 5.0: # Default rank 5
                is_placeholder = True
            elif col == "Prep_Ease" and float(val) == 5.0: # Default ease 5
                is_placeholder = True
                
            if is_placeholder:
                print(f"\n🍴 Meal: {meal_name}")
                print(f"❓ Field '{col}' is missing or default ({val}).")
                
                while True:
                    prompt = f"Enter value for {col}"
                    if col in valid_options:
                        # Show options for clarity
                        clean_opts = [str(o) for o in valid_options[col] if isinstance(o, str)]
                        prompt += f" ({'/'.join(clean_opts[:4])}...)"
                    
                    new_val = input(f"{prompt} (or Enter to skip, 'q' to quit): ").strip()
                    
                    if new_val.lower() == 'q':
                        return data if not modified else data # Exit immediately
                    
                    if not new_val:
                        break # Skip this field
                        
                    is_valid, msg = check_meal_inp(col, new_val, valid_options)
                    if is_valid:
                        data.at[idx, col] = new_val
                        modified = True
                        break
                    else:
                        print(f"❌ {msg}")
                        
    if modified and file_path:
        confirm = input("\n💾 Save changes to file? (y/n): ").lower()
        if confirm == 'y':
            data.to_csv(file_path)
            print("Successfully saved!")
            
    return data

def save_data(data, filename):
    '''
    maybe add an overwrite warning?
    '''
    data.drop_duplicates()
    data.to_csv(filename)
    return 0

if __name__ == "__main__":
    FILENAME = "../data/meal_list.csv"
#    PATH = os.path.join(os.path.dirname(__file__), f"../data/{FILENAME}")
    PATH = Path(__file__).parent / FILENAME
    data = pd.read_csv(PATH, index_col=0)
    #data.insert(2, "Diet", "NaN", True)
    print(data.head(n=5))
    #data["KosherType"] = data["KosherType"].replace({0:"parve",1:"parve",2:"milchik",3:"fleisch"})
    #save_data(data, PATH)
    #data = pd.read_csv(FILENAME,index_col=0)
    #data_new = meal_questions(data)
    #combined_arms = add_meal(data, data_new) 
    #save_data(combined_arms, FILENAME)
