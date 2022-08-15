import pandas as pd
from utils import options
from statsmodels.tsa.stattools import grangercausalitytests
import numpy as np

test = 'ssr_chi2test'
def grangers_causation_matrix(test='ssr_chi2test', verbose=False): #grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False):    
    """Check Granger Causality of all possible combinations of the Time series.
    The rows are the response variable, columns are predictors. The values in the table 
    are the P-Values. P-Values lesser than the significance level (0.05), implies 
    the Null Hypothesis that the coefficients of the corresponding past values is 
    zero, that is, the X does not cause Y can be rejected.

    data      : pandas dataframe containing the time series variables
    variables : list containing names of the time series variables.
    """

    master_df = pd.read_pickle(param.oss[0])
    maxlag = param.mxl
    test_result1 = grangercausalitytests(master_df[['Price_x', 'Price_y']], maxlag=maxlag, verbose=False)
    test_result2 = grangercausalitytests(master_df[['Price_y', 'Price_x']], maxlag=maxlag, verbose=False)
    return test_result1, test_result2


if __name__ == "__main__":
    param = options.parse_opt()
    grangers_causation_matrix(param)

  