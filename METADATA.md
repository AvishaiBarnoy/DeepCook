# Short
This document will describe the structure of the data

# Long

1. Name ::: meal name, English.
2. KosherType ::: kosher tag of meal, [parve|milchik|fleisch].
3. Diet	::: (NOT IMPLMENTED YET!) [vegan|glutenfree|vegeterian|keto|etc.]
4. Prep_Ease ::: how much technique and work does a meal needs, probably should be changed to either 0-5 or easy/medium/hard [numeric 0-10, 0 is easiest]
5. Prep_Time ::: how much work time does working does the meal needs, NOT cooking time. short-ready immediatly like fried eggs. Long would be pizza because of dough rising [short|medium|long] 
6. Cook_Time ::: how long does a meal takes to cook [short|medium|long]
7. Rank ::: how much we (@avishai231 and his family) like the food, can be used as weights for meal choice. 
8. Scaling ::: (NOT IMPLEMENTED YET!) how easy is it to make a lot from this specific meal
9. TA ::: Is it take-away food
10. times_made ::: how many times the meal has been made, after each suggestion (unless in mock mode) the user is prompted with a question "are you going to make this?" and then this field updates.
11. recipe_suggestion ::: (NOT IMPLEMENTED YET!) will have either a url to a vetted recipe or an indication that it does not need one as it is the simplest meal
12. Name_HE ::: meal name in Hebrew
