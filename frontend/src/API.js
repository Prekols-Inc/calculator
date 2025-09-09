import axios from 'axios';
import { toast } from "react-toastify";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
});

export const calculate = async (expression) => {
  try {;
    const response = await API.post('/v1/calculate', { expression });
    return response.data.result;
  } catch (error) {
    if (!error.response) {
      toast.error("Server error. Please try again later");
    } else if (error.response.status === 400) {
      toast.error("Invalid expression");
    }
    throw error;
  }
};

export const getHistory = async () => {
  try {
    const response = await API.get('/v1/history');
    return response.data;
  } catch (error) {
    console.error('Error in history request:', error);
    throw error;
  }
};
