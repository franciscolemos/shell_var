<details open>
<summary>Install</summary>

git clone https://github.com/franciscolemos/shell_var.git
<br>
cd shell_var
<br>
pip install -r requirements.txt  
</details>

<details open>
<summary>Save time series of electricity</summary>
python3 save2pickle.py --pkf datasets/electricity.pkl --sid ELEC.PRICE.TX-ALL.M
</details>


<details open>
<summary>Check seasonality</summary>
python3 seasonality.py --pkf datasets/electricity.pkl
</details>

<details open>
<summary>Save time series of natural gas</summary>
python3 save2pickle.py --pkf datasets/natural_gas.pkl --sid NG.N3035TX3.M
</details>

<details open>
<summary>Merge 2 time series</summary>
python3 merge2series.py --m2s datasets/natural_gas.pkl datasets/electricity.pkl --l2s Nat_Gas_Price Electricity_Price
</details>

<details open>
<summary>Stationary test</summary>
python3 stationary_test.py --oms datasets/m2s.pkl

<details open>
<summary>VAR model</summary>
python3 var_model.py --oss datasets/m2s_stationary.pkl
</details>

<details open>
<summary>VAR accuracy
python3 model_accuracy.py --otr datasets/train.npy  --ote datasets/test.npy --oss datasets/m2s_stationary.pkl
</details>