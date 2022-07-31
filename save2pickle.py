from dal import connect
from dal.connect import Api
import pandas as pd
from utils import options

class TimeSeries(Api):
    def __init__(self, ) -> None:
        super().__init__()
    
    def retrieve_time_series(self, series_ID):
        try:
            series_search = self.api.data_by_series(series=series_ID)
            df = pd.DataFrame(series_search)
            df.reset_index(level=0, inplace=True)
            #Rename the columns for easer analysis
            df.rename(columns={'index':'Date', df.columns[1]:'Price'}, inplace=True)
            return df
        except Exception as e:
            print("An exception as occurred. The series %s could not be retrieved." % (series_ID))
            return None

def main(param):
    try:
        #reading from EIA API
        api = connect.Api() #connect to the API
        api_series = TimeSeries() #instantiate object to retrieve data series for electricity price
        series_ID = param.sid
        df = api_series.retrieve_time_series(series_ID)
        pickle_file = param.pkf
        df.to_pickle(pickle_file)
        print(df)
        print("Successfuly save series %s to %s" % (series_ID, pickle_file))
    except Exception as e:
        print("An exception as occurred. The series %s could not be save to %s \n %s" % (series_ID, pickle_file, e))

if __name__ == "__main__":
    param = options.parse_opt()
    main(param)