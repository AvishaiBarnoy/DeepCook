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
    Ask user to enter information about meal, then stores in the data model,  
    '''
    # Here add a description of all relevant data
    data = meal_data
    inp = {key:"NaN" for key in data}
    # loop over keys, skip times_made, timestamp
    inp_inst = {}
    cols = ["Timestamp", "times_made"]
    print("Enter meal data:")
    instructions_dict = {} # here have instructions for each meal feature 
    for i in data.loc[:, ~data.columns.isin(cols)]:
        # uncomment once instructions_dict is implemented
        #print(f"Input instructions for {i}:")
        #print(instructions_dict[i])
        inp[i] = input(f"Enter value for {i}: ")
    inp["Timestamp"] = "NaN"
    inp["times_made"] = "NaN"
    print(inp)

    #while check_values(inp) == False:
        #break
    
    return pd.DataFrame(inp,index=[0])

def check_meal_inp(inp):
    '''
    Check meal input if values are correct
    '''
    pass

def write_to_log(choice,logfile="meal.log"):
    '''
    Appends a prepared eal to meal log
    '''
    now = str(pd.Timestamp.now())
    log = "{},{}\n".format(choice,now)
    with open(f"data/{logfile}","a") as f:
        f.writelines(log)

def update_column(data, column):
    '''
    data    ::: df to update
    column  ::: str, column name to update
    '''
    for idx,row in data.iterrows():
        print(idx,row.iloc[0],column)
        data.loc[idx,column] = input("Enter new value: ")
    return data

def update_missing_data(data, column):
    '''
    same as update_column() but won't update rows with values
    '''
    for idx,row in data.iterrows():
        print(idx,row.iloc[0],column)
        if data.loc[idx,column] == "NaN":
            data.loc[idx,column] = input("Enter new value: ")
    return data

def update_values_meal():
    '''
    modification of specific meal's attributes
    maybe print all meal names, ask for user numeric input by also showing their index.
    '''
    pass

def save_data(data, filename):
    '''
    maybe add an overwrite warning?
    '''
    data.drop_duplicates()
    data.to_csv(filename)
    return 0

if __name__ == "__main__":
    FILENAME = "../data/meal_list.csv"
    PATH = os.path.join(os.path.dirname(__file__), f"../data/{FILENAME}")
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
