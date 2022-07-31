from utils import options
import pandas as pd
import matplotlib.pyplot as plt
from actions import model
import pdb

def extract_series(p):
    series = pd.read_pickle(p)
    #Convert the Date column into a date object
    series['Date']=pd.to_datetime(series['Date'])
    #Set Date as a Pandas DatetimeIndex
    series.index=pd.DatetimeIndex(series['Date'])
    return series

def merge2series(param):
    #retrieve series
    series = [ extract_series(val) for val in param.m2s]
    #Merge the two time series together based on Date Index
    master_df=pd.merge(series[1]['Price'], series[0]['Price'], left_index=True, right_index=True)
    master_df.reset_index(level=0, inplace=True)
    #Plot the two variables in the same plot
    lbs = [lb for lb in param.l2s]
    plt.plot(master_df['Date'], master_df['Price_x'], label=lbs[1])
    print(lbs[1], master_df['Price_x'])
    plt.plot(master_df['Date'], master_df['Price_y'], label=lbs[0])
    print(lbs[0], master_df['Price_y'])
    # Place a legend to the right.
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    #title = lb2 + ' vs.' + lb1
    plt.title(lbs[0] + ' vs.' + lbs[1] + ' over Time') #
    plt.show()
    if options.yes_no("Do you wish to save the merged series? (y/n): "):
        answer = input("Please write the path to save the .pkl file: ")
        print("Saved data:\n ", master_df)
        master_df.to_pickle(answer)

if __name__ == "__main__":
    param = options.parse_opt()
    merge2series(param)