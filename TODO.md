
# To Do:
1. add a field-format text file
2. change add_meal_questions():
	1.1 add description printed before everything to explain what's going on.
	1.2 create a "def check_input(inp)" function to test if the input is correct
	1.3 option to look for specific koshertype - milchik/fleisch
3. check convention for column naming with pandas. Choose one - camel, snake_eye, pascal
4. add enumerative classes
5. recipe suggestions
6. add scaling factor - define 3 main functions: linear, sub-linear, superlinear
7. look by kosher/diet:
	7.1 kosher - vegan, vegeterian, parve, milchik, fleisch
		7.1.1 change kosher type to parve, milchik, fleisch in meal_list 
	7.2 Diet - vegan, glutenfree, vegeterian, keto
8. add logic function for input mode: choices: (1) new meal, (2) update values, etc.
9. last_prepared - should not suggest meal if was prepared in past 3-4 days

# Empty Functions:
## Auxillary
	
## Iodata
	1. check_meal_input - check that every field in a new added meal is in the correct format
	2. update_missing_data - goes over db and asks user to fill in empty data

## main
	1. suprise me flag?

# Things to Add to functions:

## Data organization:

## Features:
	1. meal scaling factor - can be used for weekly meal planning
	2. recipe suggestion - Krutit, Kitchencoach

## Random choice:
	1. Adjust weights according to times made - maybe timestamp and then weight adjustment
			is only made if meal was prepared in the last n days.
    2. make choice by kosher type

## Choose TA:
	1. choice by type.
	2. Time dilation - TA is only availabe in random if TA was not ordered in the past X days. 

