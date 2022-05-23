# Dinner Generator
Dinner Generator is a Python program that randomly suggests ideas to prepare for dinner, so you can have [Class with Zero Strain](https://www.youtube.com/watch?v=NpDAFKqeUDw).

> DeepCook, developed by ABN electronics was the first computer to defeat a human competitor in MasterChef.
>
> -- [*Neria Baris*](https://twitter.com/NerBaris/status/1526462586266570753)
 
Feel free to help in anyway you wish, even adding more meals, recipe suggestions, etc.

# Description
## Background
I love cooking but I also hate deciding what to make for middle-week dinners. Hence, this project was born. It is supposed to randomly give a suggestion for a meal to prepare for dinner.
I created a meal database (saved in the `data/meal_list.csv` file) and added some features to each meal. Each meal idea is based on meals I found that worked for me and my family, or something I wanted to try but never had the chance. Every meal is ranked according to my own preferances.

Fun fact: I am a crazy person who develops in vim...

## Features
Currently, the main enegine will randomly choose a meal from the *< describe the different options implemented and how the choice is done, too_late() etc. >*

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
Initially one should run the `reboot_timestamps.py` script to reset all the timestamp in the folder. 

To generate a random meal idea run:

```bash
python main.py
```
This will promt the user with a suggestion and asking if he will make it, if the user answers `y` then the meal is logged.

## Help
In order to read the help section run (which is a fun bonus of implementing a cli), this will also give you current CLI methods implemented.

```bash
python main.py --help
```

There are no known issues, but the program is not really in any mature phase, and testing was done on-the-fly as I was writing the code. This is a terrible practice and should not be dont by anyone. Since I am not a programmer, just a computational chemsit / theoretical biophysicist no one holds me accountable for anything related to code.
 
## Contributions
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to write tests as appropriate, I (Avishai) didn't do the proper and appropriate work so there are currently no tests.

Please don't hesitate to open an issue or pull request. You can also [send me a message on Twitter](https://twitter.com/messages/compose?recipient_id=2895652525).

## Author
Contributors names and contact info

Avishai Barnoy [@avishai231](https://twitter.com/avishai231)

# License
This project is licensed under the MIT License - see the LICENSE.md file for details.
