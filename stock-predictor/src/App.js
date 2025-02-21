import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import 'chart.js/auto';

const StockPredictor = () => {
  const [data, setData] = useState({});
  const [mse, setMSE] = useState(null);
  const [rmse, setRMSE] = useState(null);

  useEffect(() => {
    // Simulating API call to fetch stock data (replace with actual API later)
    axios.get('/mock-stock-data.json') // Replace with backend API endpoint
      .then((response) => {
        const stockData = response.data;
        setData(stockData);
        setMSE(stockData.mse);
        setRMSE(stockData.rmse);
      })
      .catch((error) => console.error('Error fetching stock data:', error));
  }, []);

  const chartData = {
    labels: data.dates || [],
    datasets: [
      {
        label: 'Actual Close Price',
        data: data.actual || [],
        borderColor: 'blue',
        fill: false,
      },
      {
        label: 'Predicted Close Price',
        data: data.predicted || [],
        borderColor: 'red',
        fill: false,
      },
    ],
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>TCS Stock Price Prediction</h1>
      <p>Machine Learning model trained on historical stock data</p>
      <div style={{ width: '80%', margin: 'auto' }}>
        <Line data={chartData} />
      </div>
      <h3>Performance Metrics</h3>
      <p><b>Mean Squared Error (MSE):</b> {mse}</p>
      <p><b>Root Mean Squared Error (RMSE):</b> {rmse}</p>
    </div>
  );
};

export default StockPredictor;