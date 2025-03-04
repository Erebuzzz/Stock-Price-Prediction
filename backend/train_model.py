import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

# Load dataset
DATA_PATH = "data/Indian_Stock_Market_Data.csv"
df = pd.read_csv(DATA_PATH)

# Extract stock price column (Modify if needed)
prices = df["Close"].values.reshape(-1, 1)  

# Initialize and fit MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(prices)

# Save the fitted scaler
SCALER_PATH = "backend/scaler.pkl"
with open(SCALER_PATH, "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

# Create dataset for training (last 60 days as input, next day as output)
X_train, y_train = [], []
for i in range(60, len(scaled_prices)):
    X_train.append(scaled_prices[i-60:i, 0])
    y_train.append(scaled_prices[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)  # Reshape for LSTM

# Build LSTM Model
model = keras.Sequential([
    keras.layers.LSTM(50, return_sequences=True, input_shape=(60, 1)),
    keras.layers.LSTM(50, return_sequences=False),
    keras.layers.Dense(25),
    keras.layers.Dense(1)
])

model.compile(optimizer="adam", loss="mean_squared_error")

# Train the model
model.fit(X_train, y_train, batch_size=1, epochs=10)

# Save trained model
MODEL_PATH = "../backend/tcs_stock_model.h5"
model.save(MODEL_PATH)

print(f"Model and scaler saved successfully!")