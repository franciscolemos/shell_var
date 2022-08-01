#!/bin/sh
python3 auto_var_model.py --oss datasets/m2s_stationary.pkl --tts $1
python3 auto_model_accuracy.py --otr datasets/train$1.npy  --ote datasets/test$1.npy --oss datasets/m2s_stationary.pkl --tts $1