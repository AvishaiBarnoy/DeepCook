'''
Here I will have the main logic
'''

import pandas as pd
import auxillary as aux
import io_data as iod



if __name__ == "__main__":
    data = pd.read_csv("meal_list.csv", index_col=0)
    #print(data)
    aux.choose_random(data)
