import pandas as pd
import numpy as np
from utils import options
#from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.api import VAR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt

def calculate_model_accuracy_metrics(actual, predicted):
    """
    Output model accuracy metrics, comparing predicted values
    to actual values.
    Arguments:
        actual: list. Time series of actual values.
        predicted: list. Time series of predicted values
    Outputs:
        Forecast bias metrics, mean absolute error, mean squared error,
        and root mean squared error in the console
    """
    #Calculate forecast bias
    forecast_errors = [actual[i]-predicted[i] for i in range(len(actual))]
    bias = sum(forecast_errors) * 1.0/len(actual)
    print('Bias: %f' % bias)
    #Calculate mean absolute error
    mae = mean_absolute_error(actual, predicted)
    print('MAE: %f' % mae)
    #Calculate mean squared error and root mean squared error
    mse = mean_squared_error(actual, predicted)
    print('MSE: %f' % mse)
    rmse = sqrt(mse)
    print('RMSE: %f' % rmse)
    return [bias, mae, mse, rmse]

def accuracy(param):
    training_set = np.load(param.otr[0])
    test_set = np.load(param.ote[0])
    master_df = pd.read_pickle(param.oss[0])
    
    model = VAR(endog=training_set)
    model_fit = model.fit()
    
    #Compare the forecasted results to the real data
    lagged_Values = training_set[-8:]
    prediction = model_fit.forecast(lagged_Values, steps=len(test_set))
    #Merge the array data back into the master dataframe, and un-difference and back-transform
    data_with_predictions=pd.DataFrame(np.vstack((training_set, prediction))).rename(columns={0:'Electricity_Price_Transformed_Differenced_PostProcess', 1:'Nat_Gas_Price_MCF_Transformed_Differenced_PostProcess'})
    #Define which data is predicted and which isn't in the 'Predicted' column
    data_with_predictions.loc[:,'Predicted']=1
    data_with_predictions.loc[(data_with_predictions.index>=0) & 
                                     (data_with_predictions.index<=(len(training_set)-1)),'Predicted']=0
    
    #Add a row of NaN at the begining of the df
    data_with_predictions.loc[-1] = [None, None, None]  # adding a row
    data_with_predictions.index = data_with_predictions.index + 1  # shifting index
    data_with_predictions.sort_index(inplace=True) 
    #Add back into the original dataframe
    master_df.loc[:,'Electricity_Price_Transformed_Differenced_PostProcess'] = data_with_predictions['Electricity_Price_Transformed_Differenced_PostProcess']
    master_df.loc[:,'Predicted'] = data_with_predictions['Predicted']
        
    #Un-difference the data
    for i in range(1,len(master_df.index)-1):
        master_df.at[i,'Price_x_Transformed']= master_df.at[i-1,'Price_x_Transformed']+master_df.at[i,'Electricity_Price_Transformed_Differenced_PostProcess']
    
    #Back-transform the data
    master_df.loc[:,'Predicted_Electricity_Price']=np.exp(master_df['Price_x_Transformed'])
    
    #Compare the forecasted data to the real data
    print(master_df[master_df['Predicted']==1][['Date','Price_x', 'Predicted_Electricity_Price']])
    
    #Evaluate the accuracy of the results, pre un-differencing and back-transformation
    kpi = calculate_model_accuracy_metrics(list(master_df[master_df['Predicted']==1]['Price_x']), 
                                    list(master_df[master_df['Predicted']==1]['Predicted_Electricity_Price']))
    
    fileKPI = 'results.csv'
    kpi = [param.tts, 100 - param.tts] + kpi
    dataSetSizes = pd.DataFrame(kpi).T
    dataSetSizes.to_csv(fileKPI, mode='a', index=False, header = False)

if __name__ == "__main__":
    param = options.parse_opt()
    accuracy(param)