
import pandas as pd
import random as rnd

def choose_random(ideas,rank=False, times=False, last_made=False):
    '''
    makes either a fully (pseudo) random choice from all meal options
        or a weighted choice based on rank.
    Future:
        1. Adjust weights according to times made.
        2. Make choice by ease
        3. Give k-choices ranked by ease and/or rank
        4. make choice by kosher type
        5. if last_made don't make choice made in last 5 days or if last_made==int then that amount of days
    '''
    if rank == False:
        choice = rnd.choices(population=list(range(len(ideas))),k=1)
    elif rank == True:
        choice = rnd.choices(population=list(range(len(ideas))),weights=ideas["Rank"],k=1)
    print(ideas.Name[choice[0]]) #ideas.Rank[choice[0]]
    make_it = input("Are you going to make this meal? (y/n)")
    while True:
        if make_it.lower() == "y":
            ideas.loc[choice[0],'times_made'] += 1
            ideas.loc[choice[0],'Timestamp'] = pd.Timestamp.now()
            save_data(ideas,filename="meal_list.csv")
            break
        elif make_it.lower() == "n":
            print("meal not logged.")
            break
        else:
            print("Please enter a valid answer.")
            make_it = input("Are you going to make this meal? (y/n)")
    return ideas.Name[choice[0]] #ideas.Rank[choice[0]]

def choose_TA(meal_data,rank=False,times=False,last_made=False):
    '''
    randomly makes a choice from the meals marked as take aways 
    '''
    ideas = meal_data
    print(ideas.loc[ideas["TA"] == 1])
    choice = rnd.choices(population=list(range(len(ideas))),weights=ideas["TA"],k=1)
    print(ideas.Name[choice[0]])

def add_meal(ideas,name,kosher,ease,rank,TA=0,times_made=0):
    '''
    ideas ::: pandas dataframe of meal ideas
    name ::: list of meal names
    kosher ::: 0 - Milchik, 1 - Parve, 2 - Fleish
    ease ::: [0,10] how easy is it to make, lower is better
    rank ::: how much do we like [0,10], higher is better
    TA ::: is Take Away, 0 - NO, 1 - YES
    times_made ::: default is 0
    '''
    new_data = pd.DataFrame({"Name":name,"KosherType":kosher,"Ease":ease,"Rank":rank,"TA":TA,"times_made":times_made,\
            "Timestamp":'nan'})
    new_ideas = pd.concat([ideas,new_data], ignore_index = True, axis = 0)
    return new_ideas

def update_rank():
    '''
    update rank of one meal
    '''
    pass

def update_ranks():
    '''
    update rank of many many meals
    '''
    pass

def save_data(data,filename="meal_list.csv"):
    '''
    maybe add an overwrite warning?
    '''
    data.drop_duplicates()
    data.to_csv(filename)

if __name__ == "__main__":
    FILENAME = "meal_list.csv"
    data = pd.read_csv(FILENAME,index_col=0)
    
    #choose_random(data, rank=False, times=False)
    choose_TA(data)
    #data = add_meal(data,["Pasta tomato","Stir Fried Veggies Frozen Bag"],[1,1],[4,4],[3,7])
    #save_data(data)
    #print(data)

