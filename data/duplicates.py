import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Finds and removes duplicates from data.')
parser.add_argument('filename',  help='data filename')
args = parser.parse_args()
#print(args.filename)

data = pd.read_csv(args.filename, index_col=0)
dup = data[data["meal_name"].duplicated() == True]

#print(dup)
for i in dup["meal_name"]:
    #print(i)
    print(data[data["meal_name"]==i])
    #dups = data[i]
    #dups = data["meal_name"][i]
    #dups = data[data["meal_name"] == data["meal_name"][dup[0]]]
    #print(dups)
