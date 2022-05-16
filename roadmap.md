
Ideas for extra features, algorithmic logic, directions of development, etc.

# Roadmap
## Extra Functionality and things to add:
1. divide meals to subuntis and generate combinations, i.e., main course + side dish + salad.
2. scaling factor for meals, i.e., how easy is to make more from the meal. E.g., soups and bread scale good while schnitzel scales bad.
4. twitter bot or whatsapp bot
5. GUI website for suggestions
6. Ranking Function - at t0 the meal_list.csv comes with all ranks set to None/nan/0/1/etc and with each suggestion if meal never came up in the loop it will ask for a rank. A combination can be made so that only ranked meals will be suggested, this can be implemented by setting rank=0 for all meals and, after sufficient meals were ranked (maybe fraction of meals), to use weights. This results in 0 weights for meals not ranked, or not liked. Maybe the secretary problem, when have we learned enought and it is time to make a choice?
7. Suprise me option, just give a meal that was never ranked - this is problematic with current ranking system. If someone ranks 0 then he doesn't want to eat it and it cannot resurface in the suprise_me. A workaround would be that if a meal was ranked 0 when asked to rank the meal will get a timestamp, and the combined 0+timestamp can allow for proper filtering.
8. In future website: create a user and login system so that knowledge can be stored. This should not impede the free usage of the system.
