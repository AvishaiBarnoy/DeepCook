'''
Auxillary functions
'''
import pandas as pd
import random as rnd

def choose_random(meals, rank=False, times=False, last_made=False, TA=None):
    '''
    Changes to make:
    1. test time stamping

    makes either a fully (pseudo) random choice from all meal options
        or a weighted choice based on rank.
    Future:
        1. Adjust weights according to times made.
        2. Make choice by ease
        3. Give k-choices ranked by ease and/or rank
        4. make choice by kosher type
        5. if last_made don't make choice made in last 5 days or if last_made==int then that amount of days
    meals     ::: DataFrame with meal information
    rank      ::: if True gives weights to meals based on rank
    last_made ::: *NOT IMPLEMENTED* should take into account when last made, maybe combine with times?
    TA        ::: True - choose only from takeawy, False - choose only from homecooking, None - anything may come
    '''
    use_rank = None
    if rank == True:
        use_rank = choice["Rank"]

    if TA == "True": 
        choice = meals[meals["TA"] == 1].sample(n=1, weights=use_rank)
    if TA == "False":
        choice = meals[meals["TA"] == 0].sample(n=1, weights=use_rank)
    else:
        choice = meals.sample(n=1, weights=use_rank)
    #print(choice.get(["Name"]))
    return choice

    if rank == False:
        choice = rnd.choices(population=list(range(len(meals))),k=1)
    elif rank == True:
        choice = rnd.choices(population=list(range(len(meals))),weights=meals["Rank"],k=1)
    print(meals.Name[choice[0]]) #meals.Rank[choice[0]]
    make_it = input("Are you going to make this meal? (y/n)")
    while True:
        if make_it.lower() == "y":
            meals.loc[choice[0],'times_made'] += 1
            meals.loc[choice[0],'Timestamp'] = pd.Timestamp.now()
            save_data(meals,filename="meal_list.csv")
            #save_data(choice,filename="meals_made.log") # logger file for prepared meals
            break
        elif make_it.lower() == "n":
            print("meal not logged.")
            break
        else:
            print("Please enter a valid answer.")
            make_it = input("Are you going to make this meal? (y/n)")
    return meals.Name[choice[0]] #meals.Rank[choice[0]]

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
    #choose_TA(data)
    #data = add_meal(data,["Pasta tomato","Stir Fried Veggies Frozen Bag"],[1,1],[4,4],[3,7])
    #save_data(data)
    #print(data)

