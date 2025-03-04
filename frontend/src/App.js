import React, { useState } from "react";
import StockChart from "./components/StockChart";
import PredictionForm from "./components/PredictionForm";

const App = () => {
  const [prices, setPrices] = useState([]);
  const [prediction, setPrediction] = useState(null);

  return (
    <div>
      <h1>Stock Predictor</h1>
      <PredictionForm setPrediction={setPrediction} />
      {prediction && (
        <>
          <h2>Predicted Price: {prediction}</h2>
          <StockChart prices={prices} predicted={prediction} />
        </>
      )}
    </div>
  );
};

export default App;