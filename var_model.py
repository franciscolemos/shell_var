import pandas as pd
import numpy as np
from utils import options
from statsmodels.tsa.api import VAR

def run_var(param):
    master_df = pd.read_pickle(param.oss[0])
    #Convert the dataframe to a numpy array
    master_array=np.array(master_df[['Price_x_Differenced', 'Price_y_Differenced']].dropna())
    #Generate a training and test set for building the model: 95/5 split
    training_set = master_array[:int(0.70*(len(master_array)))]
    test_set = master_array[int(0.30*(len(master_array))):]
    #import pdb; pdb.set_trace()
    #Fit to a VAR model
    model = VAR(endog=training_set)
    model_fit = model.fit()
    #Print a summary of the model results
    print(model_fit.summary())
    if options.yes_no("Do you wish to save the training set? (y/n): "):
        answer = input("Please write the path to save the .npy file: ")
        print("Saved data:\n ", training_set)
        np.save(answer, training_set)
    if options.yes_no("Do you wish to save the test set? (y/n): "):
        answer = input("Please write the path to save the .npy file: ")
        print("Saved data:\n ", test_set)
        np.save(answer, test_set)

if __name__ == "__main__":
    param = options.parse_opt()
    run_var(param)