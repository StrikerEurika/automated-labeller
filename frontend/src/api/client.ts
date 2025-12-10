import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1", // Backend API with /api/v1 prefix
  timeout: 60000,
});

export default api;
