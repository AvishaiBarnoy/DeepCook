'''
Functions for data input/ouput and update of data
This whole library needs to undergo a thorough revamp and remodelling, removing redundant and depracted code parts, adding new functionality, descriptions, etc.
'''

import pandas as pd

def add_meal(data, new_data):
    '''
    ideas ::: pandas dataframe of meal ideas
    name ::: list of meal names
    kosher ::: 0 - Milchik, 1 - Parve, 2 - Fleish
    ease ::: [0,10] how easy is it to make, lower is better
    rank ::: how much do we like [0,10], higher is better
    TA ::: is Take Away, 0 - NO, 1 - YES
    times_made ::: default is 0
    Timestamp ::: nan by default, when meal is prepared this updates to a the latest date prepared
    '''
    #new_data = pd.DataFrame({"Name":name,"KosherType":kosher,"Ease":ease,"Rank":rank,"TA":TA,"times_made":times_made,\
            #"Timestamp":""})
    new_ideas = pd.concat([data,new_data], ignore_index = True, axis = 0)
    return new_ideas

def add_meal_questions(meal_data):
    '''
    Ask user to enter information about meal, then stores in the data model,  
    '''
    # Here add a description of all relevant data
    data = meal_data
    inp = {key:"NaN" for key in data}
    # loop over keys, maybe skip times_made, timestamp, and recipe suggestion
    inp_inst = {}
    for i in data:
        print(f"Input instructions for {i}:")
        #print(inp_inst[i])
        inp[i] = input("Enter value for {i}:")
    inp["Timestamp"] = "NaN"
    inp["times_made"] = "NaN"
    print(inp)

    #while check_values(inp) == False:
        #break
    
    return pd.DataFrame(inp,index=[0])


    print("Manual new meals entry function.")
    print("At any point write break to enter the function midway without \
            saving the entry, or the novel method of Ctrl+C")
    new_meal = {}
    name = input("Enter meal name:\n")
    while True:
        kosher = input("Enter kosher type (0-Milchik, 1-Parve, 2-Fleish, 3-Vegan):")
        if kosher== "0" or kosher == "1" or kosher == "2" or kosher == "3" :
            kosher = int(kosher)
            break
        else:
            print("Please enter a valid input")
            kosher = input("Enter kosher type (0-Milchik, 1-Parve, 2-Fleish, 3-Vegan):")
    
    while True:
        ease = input("Enter ease of preparation between 0-10 lower is easier:")
        if ease == "break":
            break
        elif int(ease) >= 0 or int(ease) <= 10:
            ease = int(ease)
            break
        else:
            print("Please enter a valid input")
            ease = int(input("Enter ease of preparation between 0-10 lower is easier:"))
    
    while True:
        rank = input("Enter meal's rank between 0-10 higher is better:")
        if rank == "break":
            break
        elif int(rank) >= 0 or int(rank) <= 10:
            rank = int(rank)
            break
        else:
            print("Please enter a valid input")
            rank = input("Enter meal's rank between 0-10 higher is better:")

    while True:
        TA = input("Is meal a take away? (Yes/yes/Y/y/No/no/N/n)")
        if TA == "break":
            break
        elif TA == "yes" or TA == "Yes" or TA == "y" or TA == "Y":
            TA = 1
            break
        elif TA == "no" or TA == "No" or TA == "n" or TA == "N":
            TA = 0
            break
        else:
            print("Please enter a valid input")
            TA = input("Is meal a take away? (Yes/yes/Y/y/No/no/N/n)")
    meal_data = add_meal(meal_data,[name],[kosher],[ease],[rank],[TA])
    print(meal_data)
    #save_data(meal_data)

def check_meal_inp(inp):
    '''
    check meal input if values are correct
    '''
    invalid_inp = []
    for i in invalid_inp:
        pass
    pass

def write_to_log(choice):
    now = str(pd.Timestamp.now())
    choice = str(choice["Name"].iloc[0])
    log = "{},{}\n".format(choice,now)
    with open("meal.log","a") as f:
        f.writelines(log)
        return 0

def update_column(data,column):
    '''
    data    ::: df to update
    column  ::: str, column name to update
    '''
    for idx,row in data.iterrows():
        print(idx,row.iloc[0],column)
        data.loc[idx,column] = input("Enter new value: ")

def update_column_nan(data,column):
    '''
    same as update_column() but won't update rows with values
    '''
    pass

def update_values_meal():
    '''
    modification of specific meal's attributes
    maybe print all meal names, ask for user numeric input by also showing their index.
    '''
    pass

def save_data(data,filename="meal_list.csv"):
    '''
    maybe add an overwrite warning?
    '''
    data.drop_duplicates()
    data.to_csv(filename)

if __name__ == "__main__":
    FILENAME = "./data/meal_list.csv"
    data = pd.read_csv(FILENAME,index_col=0)
    add_meal_questions(data)
    data = pd.read_csv(FILENAME,index_col=0)
    print(data.tail(5))
