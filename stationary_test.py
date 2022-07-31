from utils import options
from doctest import master
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def augmented_dickey_fuller_statistics(time_series):
    """
    Run the augmented Dickey-Fuller test on a time series
    to determine if it's stationary.
    Arguments: 
        time_series: series. Time series that we want to test 
    Outputs: 
        Test statistics for the Augmented Dickey Fuller test in 
        the console 
    """
    result = adfuller(time_series.values)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value)) 

def stationary(param):
    master_df = pd.read_pickle(param.oms[0])
    print("Reading the merged series")
    print(master_df)
    master_df['Price_x_Transformed']=np.log(master_df['Price_x'])
    master_df['Price_y_Transformed']=np.log(master_df['Price_y'])
    print("Transformed series")
    print(master_df)
    #Difference the data by 1 month
    n=1
    master_df['Price_x_Differenced'] = master_df['Price_x_Transformed'] - master_df['Price_x_Transformed'].shift(n)
    master_df['Price_y_Differenced'] = master_df['Price_y_Transformed'] - master_df['Price_y_Transformed'].shift(n)
    print("Differenced series")
    print(master_df)
    #Execute in the main block
    #Run each transformed, differenced time series thru the Augmented Dickey Fuller test
    print('Augmented Dickey-Fuller Test: Price Time Series for x ')
    augmented_dickey_fuller_statistics(master_df['Price_x_Differenced'].dropna())
    print('Augmented Dickey-Fuller Test: Price Time Series y')
    augmented_dickey_fuller_statistics(master_df['Price_y_Differenced'].dropna())
    
    if options.yes_no("Do you wish to save the stationary series? (y/n): "):
        answer = input("Please write the path to save the .pkl file: ")
        print("Saved data:\n ", master_df)
        master_df.to_pickle(answer)


    return master_df


if __name__ == "__main__":
    param = options.parse_opt()
    stationary(param)