import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

class Seasonality():
    def __init__(self) -> None: #https://stackoverflow.com/questions/64933298/why-should-we-use-in-def-init-self-n-none
        pass
    def decompose_time_series(self, series):
        """
        Decompose a time series and plot it in the console
        Arguments: 
            series: series. Time series that we want to decompose
        Outputs: 
            Decomposition plot in the console
        """
        result = seasonal_decompose(series, model='additive')
        result.plot()
        plt.show()