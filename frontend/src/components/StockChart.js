import React from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

const StockChart = ({ prices, predicted }) => {
  const data = {
    labels: Array.from({ length: prices.length }, (_, i) => `Day ${i + 1}`),
    datasets: [
      {
        label: "Stock Prices",
        data: prices,
        borderColor: "blue",
        fill: false,
      },
      {
        label: "Predicted Price",
        data: [...Array(prices.length - 1).fill(null), predicted],
        borderColor: "red",
        fill: false,
      },
    ],
  };

  return <Line data={data} />;
};

export default StockChart;