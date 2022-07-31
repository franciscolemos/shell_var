Install
git clone 
cd PVAR #Price Forecasting using a Vector Autoregression (VAR) Model
pip install -r requirements.txt  # install

Check seasonality
python .\seasonality.py --pkf .\datasets\electricity.pkl

Save time series of natural gas
python .\save2pickle.py --pkf .\datasets\natural_gas.pkl --sid NG.N3035TX3.M

Merge 2 time series
python merge2series.py --m2s .\datasets\natural_gas.pkl .\datasets\electricity.pkl --l2s Nat_Gas_Price Electricity_Price

Stationary test
python stationary_test.py --oms .\datasets\m2s.pkl

VAR model
python var_model.py --oss .\datasets\m2s_stationary.pkl

VAR accuracy
python model_accuracy.py --otr .\datasets\train.npy  --ote .\datasets\test.npy --oss datasets\m2s_stationary.pkl