'''
Here I will have the main logic
'''

import pandas as pd
import auxillary as aux
import io_data as iod

if __name__ == "__main__":
    data = pd.read_csv("meal_list.csv", index_col=0)
    #print(data)
    random_choice = aux.choose_random(data)
    #print(type(random_choice))
    
    # uncomment to reset timestamps and times_made
    #aux.reboot_time_timestamps(data)
