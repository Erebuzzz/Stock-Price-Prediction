import axios from "axios";

const API_URL = "http://localhost:5000";

export const predictStock = async (prices) => {
  try {
    const response = await axios.post(`${API_URL}/predict`, { prices });
    return response.data.predicted_price;
  } catch (error) {
    console.error("Prediction error:", error);
    throw error;
  }
};