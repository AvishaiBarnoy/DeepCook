# DeepCook Meal Suggestion Engine
DeepCook is a Python program that randomly suggests ideas to prepare for dinner, so you can have [Class with Zero Strain](https://www.youtube.com/watch?v=NpDAFKqeUDw).

> DeepCook, developed by ABN electronics was the first computer to defeat a human competitor in MasterChef.
>
> -- [*Neria Baris*](https://twitter.com/NerBaris/status/1526462586266570753)
 
Feel free to help in anyway you wish, even adding more meals, recipe suggestions, etc.

# Description
## Background
I love cooking but I also hate deciding what to make for middle-week dinners. Hence, this project was born. It is supposed to randomly give a suggestion for a meal to prepare for dinner.
I created a meal database (saved in the `data/meal_list.csv` file) and added some features to each meal. Each idea is a meal I found that worked for me and my family, or something I wanted to try but never had the chance. Every meal is ranked according to my own preferances.

Fun fact: I am a crazy person who develops in vim...

## Features
Currently, the main engine will randomly choose a meal from `data/meals_list.csv`. There are several options implemented accessible by running `main --help`:

- **Weighted Selection** (`--rank`): Use preference rankings to weight random selection
- **Take-away Filtering** (`--ta/--no-ta`): Include/exclude or only show take-away options
- **Recently Made Filter** (`--last-made N`): Exclude meals prepared in the past N days (recommended: 3-5)
- **Kosher Filtering** (`--kosher`): Filter by kosher type (parve, milchik, fleisch, nonkosher)
- **Diet Filtering** (`--diet`): Filter by dietary preference (vegan, vegetarian, glutenfree, keto, any)
- **Smart Time Awareness** (`too_late()`):
    - **Late Night (8 PM - Midnight)**: Automatically filters out meals with `long` preparation times. Suggests only quick/medium options.
    - **Sleep Protection (Midnight - 5 AM)**: Suggests no cooking at all during sleeping hours.
- **Weighted Random Selection** (`choose_random`):
    - **Rank Bias**: Higher ranked meals (1-10) are more likely to be chosen.
    - **Frequency Penalty**: Meals made frequently get a weight penalty (`1 / (1 + 0.5 * times_made)`).
    - **Recency Decay**: Meals made recently get a temporary weight reduction that fades over 14 days.
    - **Surprise Factor**: "Surprise Me" mode heavily boosts never-made or rarely-made meals.
- **Filtering Logic**:
    - **Kosher**: Strict separation (Parve/Milchik/Fleisch). Parve is always included unless explicitly excluded.
    - **Diet**: Supports multiple tags per meal (e.g., "vegan, glutenfree").
    - **Leftover Mode**: Prioritizes repeat meals if the previous day had a large, scalable main dish.
- **Weekly Planner**: Full 7-day planning with day-locking and shopping list export.

Currently ranking is only based on my own preferences for meals, but in the future a quick reranking option will be added, also an easy meal insertion to the db will be implemented.

*< one day, here you, brave reader, will find a thorough and in-depth description of this project >*

# Getting Started
## Dependencies
Python3.9 was used for development, I believe that any Python3 version will be compatible.

See the [`requirements.txt`](./requirements.txt) for the dependencies.

## Installing
Just run and all will be good.
```bash
pip install -r requirements.txt
```

## Executing Program
Initially one should run the `reboot_timestamps.py` script to reset all timestamps. 

To generate a random meal idea run:

```bash
python main.py
```

## Running Tests
The project now includes a comprehensive test suite using pytest:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v
```

See [`tests/README.md`](./tests/README.md) for detailed information about the test suite.

## Help
In order to read the help section run (which is a fun bonus of implementing a cli), this will also give you current CLI methods implemented.

```bash
python main.py --help
```
 
## Contributions
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Also, don't forget to update the changes in the [`CHANGELOG.md`](./CHANGELOG.md) file.

Please make sure to write tests as appropriate, I (Avishai) didn't do the proper and appropriate work so there are currently no tests.

Please don't hesitate to open an issue or pull request. You can also [send me a message on Twitter](https://twitter.com/messages/compose?recipient_id=2895652525).

## Author
Contributors names and contact info

Avishai Barnoy [@avishai231](https://twitter.com/avishai231)

# License
This project is licensed under the MIT License - see the LICENSE.md file for details.
