const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

app.post("/api/predict", async (req, res) => {
  try {
    const response = await axios.post("http://localhost:5000/predict", req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch prediction" });
  }
});

app.listen(8080, () => {
  console.log("Proxy server running on port 8080");
});