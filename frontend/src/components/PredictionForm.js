import React, { useState } from "react";
import { predictStock } from "../services/api";

const PredictionForm = ({ setPrediction }) => {
  const [prices, setPrices] = useState(new Array(60).fill("")); // 60 input fields
  const [error, setError] = useState(null);

  const handleChange = (index, value) => {
    const newPrices = [...prices];
    newPrices[index] = value;
    setPrices(newPrices);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    if (prices.some((price) => price === "")) {
      setError("Please fill all 60 fields.");
      return;
    }

    try {
      const priceArray = prices.map((price) => parseFloat(price));
      const predictedPrice = await predictStock(priceArray);
      setPrediction(predictedPrice);
    } catch (err) {
      setError("Failed to fetch prediction. Try again.");
    }
  };

  return (
    <div>
      <h2>Enter Last 60 Stock Prices</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "5px" }}>
          {prices.map((price, index) => (
            <input
              key={index}
              type="number"
              placeholder={`Day ${index + 1}`}
              value={price}
              onChange={(e) => handleChange(index, e.target.value)}
              required
            />
          ))}
        </div>
        <button type="submit" style={{ marginTop: "10px" }}>Predict</button>
      </form>
    </div>
  );
};

export default PredictionForm;