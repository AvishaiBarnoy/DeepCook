'''
This is depracted and was only used to make the inital DataFrame and save it as a csv file
'''

import pandas as pd

meal_names = ["Pasta Rose", "Stir Fried Vegetables", "Hot Salad", "Hamburger and Fries"]

# 0 - Milchik, 1 - Parve, 2 - Fleysh
kosher_type = [0, 1, 1, 2] 
# Lower ease is better
ease_of_making = [2, 6, 7, 4]
# Higher rank is better
rank = [4, 8, 8, 7]


dinner_ideas = pd.DataFrame(
			{
				"Name": meal_names,
				"KoserType": kosher_type,
				"Ease": ease_of_making,
				"Rank": rank,
                                "times_made": 0
}
)

if __name__ == '__main__':
    print(dinner_ideas)
    #print(make_random(dinner_ideas))
    #print(dinner_ideas)
    #dinner_ideas.to_csv("meal_list.csv")


