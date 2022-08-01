import argparse
import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
class options():
    def parse_opt(known=False):
        parser = argparse.ArgumentParser()
        parser.add_argument('--sid', type=str, default='', help='Series ID')
        parser.add_argument('--pkf', type=str, default='', help='Pickle file')
        parser.add_argument('--m2s', type=str, nargs='+', default='', help='Merge 2 series')
        parser.add_argument('--l2s', type=str, nargs='+', default='', help='Labels for 2 series')
        parser.add_argument('--oms', type=str, nargs='+', default='', help='Open merged series')
        parser.add_argument('--oss', type=str, nargs='+', default='', help='Open stationary series')
        parser.add_argument('--otr', type=str, nargs='+', default='', help='Open training set')
        parser.add_argument('--ote', type=str, nargs='+', default='', help='Open test set')
        parser.add_argument('--tts', type=int, default=70, help='Train test split')
        opt = parser.parse_known_args()[0] if known else parser.parse_args()
        return opt

    def yes_no(question):
        i = 0
        while i < 2:
            answer = input(question)
            if any(answer.lower() == f for f in ["yes", 'y', '1', 'ye', 'Y']):
                return True
            elif any(answer.lower() == f for f in ['no', 'n', '0', 'N']):
                return False
            else:
                i += 1
                if i < 2:
                    print('Please enter y or n')
                else:
                    print("Nothing done")

class var_model_accuracy():
    def __init__(self, param):
        self.training_set = np.load(param.otr[0])
        self.test_set = np.load(param.ote[0])
        self.master_df = pd.read_pickle(param.oss[0])
        self.tts = param.tts
    
    def calculate_model_accuracy_metrics(self, actual, predicted):
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

    def var_model(self):
        model = VAR(endog=self.training_set)
        model_fit = model.fit()
        
        #Compare the forecasted results to the real data
        lagged_Values = self.training_set[-8:]
        prediction = model_fit.forecast(lagged_Values, steps=len(self.test_set))
        #Merge the array data back into the master dataframe, and un-difference and back-transform
        data_with_predictions=pd.DataFrame(np.vstack((self.training_set, prediction))).rename(columns={0:'Electricity_Price_Transformed_Differenced_PostProcess', 1:'Nat_Gas_Price_MCF_Transformed_Differenced_PostProcess'})
        #Define which data is predicted and which isn't in the 'Predicted' column
        data_with_predictions.loc[:,'Predicted']=1
        data_with_predictions.loc[(data_with_predictions.index>=0) & 
                                        (data_with_predictions.index<=(len(self.training_set)-1)),'Predicted']=0
        
        #Add a row of NaN at the begining of the df
        data_with_predictions.loc[-1] = [None, None, None]  # adding a row
        data_with_predictions.index = data_with_predictions.index + 1  # shifting index
        data_with_predictions.sort_index(inplace=True) 
        #Add back into the original dataframe
        self.master_df.loc[:,'Electricity_Price_Transformed_Differenced_PostProcess'] = data_with_predictions['Electricity_Price_Transformed_Differenced_PostProcess']
        self.master_df.loc[:,'Predicted'] = data_with_predictions['Predicted']
            
        #Un-difference the data
        for i in range(1,len(self.master_df.index)-1):
            self.master_df.at[i,'Price_x_Transformed']= self.master_df.at[i-1,'Price_x_Transformed']+self.master_df.at[i,'Electricity_Price_Transformed_Differenced_PostProcess']
        
        #Back-transform the data
        self.master_df.loc[:,'Predicted_Electricity_Price']=np.exp(self.master_df['Price_x_Transformed'])
        
        #Compare the forecasted data to the real data
        print(self.master_df[self.master_df['Predicted']==1][['Date','Price_x', 'Predicted_Electricity_Price']])

        self.kpi = self.calculate_model_accuracy_metrics(list(self.master_df[self.master_df['Predicted']==1]['Price_x']), 
                                    list(self.master_df[self.master_df['Predicted']==1]['Predicted_Electricity_Price']))

    def save_results(self):
        fileKPI = 'results.csv'
        kpi = [self.tts, 100 - self.tts] + self.kpi
        dataSetSizes = pd.DataFrame(kpi).T
        dataSetSizes.to_csv(fileKPI, mode='a', index=False, header = False)