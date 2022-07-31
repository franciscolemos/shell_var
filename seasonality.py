import pandas as pd
from actions import model
from utils import options

def main(param):
    #reading from pickle file
    pickle_file = param.pkf
    df = pd.read_pickle(pickle_file)
    #Convert the Date column into a date object
    df['Date']=pd.to_datetime(df['Date'])
    #Set Date as a Pandas DatetimeIndex
    df.index=pd.DatetimeIndex(df['Date'])
    #Decompose the time series into parts
    seasonality = model.Seasonality()
    seasonality.decompose_time_series(df['Price'])
    print(df)

if __name__ == "__main__":
    opt = options()
    param = options.parse_opt()
    main(param)