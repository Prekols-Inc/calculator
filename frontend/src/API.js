import axios from 'axios';
import { toast } from "react-toastify";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const calculate = async (expression) => {
  try {
    console.log(import.meta.env.VITE_API_URL);
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

export const getHistory = async (expression) => {
  try {
    console.log(import.meta.env.VITE_API_URL);
    const response = await API.post('/calculate', { expression });
    return response.data.result;
  } catch (error) {
    console.error('Error in calculate request:', error);
    throw error;
  }
};


export const getHistoryStub = () => {
  return [
    { expression: "2+2", result: 2 + 2 },
    { expression: "10/5", result: 10 / 5 }
  ];
};

