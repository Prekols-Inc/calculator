import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const calculate = async (expression) => {
  try {
    console.log(import.meta.env.VITE_API_URL);
    const response = await API.post('/calculate', { expression });
    return response.data.result;
  } catch (error) {
    console.error('Error in calculate request:', error);
    throw error;
  }
};
