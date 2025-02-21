import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
import seaborn as sns
import os
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('Indian_Stock_Market_Data.csv', delimiter=',', on_bad_lines='skip') 
#print(data.shape)
#print(data.sample(7))
data['Date'] = pd.to_datetime(data['Date'])

#Checking frequency of different companies stocks
"""freq={}
for item in data['Company']:
   if item in freq:
      freq[item] += 1
   else:
      freq[item] = 1
print(freq)

#data.info()"""

companies = ['ADANIPORTS', 'BPCL', 'COALINDIA', 'HDFC', 'RELIANCE', 'TCS', 'TATASTEEL', 'TITAN', 'WIPRO']

#Market Performance of Different Companies Stocks
plt.figure(figsize=(15, 8)) 
for index, company in enumerate(companies, 1): 
    plt.subplot(3, 3, index) 
    c = data[data['Company'] == company] 
    plt.plot(c['Date'], c['Close'], c="r", label="close", marker="+") 
    plt.plot(c['Date'], c['Open'], c="g", label="open", marker="^") 
    plt.title(company) 
    plt.legend() 
    plt.tight_layout()

#Market Performance as a function of time
plt.figure(figsize=(15, 8))
for index, company in enumerate(companies, 1):
    plt.subplot(3, 3, index)
    c = data[data['Company'] == company]
    plt.plot(c['Date'], c['Volume'], c='purple', marker='*')
    plt.title(f"{company} Volume")
    plt.tight_layout()

#TCS Stock Prices
plt.figure(figsize=(10, 5))
tcs = data[data['Company'] == 'TCS']
prediction_range = tcs.loc[(tcs['Date'] > datetime(2017,1,1)) & (tcs['Date'] < datetime(2023,1,1))]
plt.plot(tcs['Date'], tcs['Close'], color="blue")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.title("TCS Stock Prices Over Time")
plt.show()

close_data = tcs.filter(['Close'])
dataset = close_data.values
training = int(np.ceil(len(dataset) * .95))
print(training)

#Training and Prediction of Dataset
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

train_data = scaled_data[0:int(training), :]
# preparing feature and labels
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = keras.models.Sequential()
model.add(keras.layers.LSTM(units=64,return_sequences=True,input_shape=(x_train.shape[1], 1)))
model.add(keras.layers.LSTM(units=64))
model.add(keras.layers.Dense(32))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(1))
model.summary

model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(x_train, y_train, epochs=10)

test_data = scaled_data[training - 60:, :]
x_test = []
y_test = dataset[training:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# predict the testing data
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# evaluation metrics
mse = np.mean(((predictions - y_test) ** 2))
print("MSE", mse)
print("RMSE", np.sqrt(mse))

train = tcs[:training]
test = tcs[training:]
test['Predictions'] = predictions

plt.figure(figsize=(10, 8))
plt.plot(train['Date'], train['Close'])
plt.plot(test['Date'], test[['Close', 'Predictions']])
plt.title('TCS Stock Close Price')
plt.xlabel('Date')
plt.ylabel("Close")
plt.legend(['Train', 'Test', 'Predictions'])