from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import pickle
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend to access backend

# Load the trained model
MODEL_PATH = "backend/tcs_stock_model.h5"
model = keras.models.load_model(MODEL_PATH)

# Load the trained scaler
SCALER_PATH = "backend/scaler.pkl"

if os.path.exists(SCALER_PATH):
    with open(SCALER_PATH, "rb") as scaler_file:
        scaler = pickle.load(scaler_file)
else:
    raise FileNotFoundError("Scaler file not found. Ensure it was saved during training.")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    prices = data.get("prices") 

    if not prices or len(prices) != 60:
        return jsonify({"error": "Invalid input. Provide exactly 60 prices."}), 400

    try:
        # Normalize input using pre-fitted scaler
        prices = np.array(prices).reshape(-1, 1)
        prices_scaled = scaler.transform(prices)  # Use transform, NOT fit_transform
        prices_scaled = prices_scaled.reshape(1, 60, 1)

        # Predict
        prediction = model.predict(prices_scaled)
        predicted_price = scaler.inverse_transform([[prediction[0][0]]])[0][0]

        return jsonify({"predicted_price": float(predicted_price)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)