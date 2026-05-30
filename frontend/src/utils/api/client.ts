import axios from "axios";

export const apiClient = axios.create({
  baseURL: "https://api.journal-app.a-t-dev.com/api/",
  headers: {
    "Content-Type": "application/json",
  },
});