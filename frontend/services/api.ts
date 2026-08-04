import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getMetrics = async () => {
  const response = await api.get('/metrics');
  return response.data;
};

export const getLogs = async () => {
  const response = await api.get('/logs');
  return response.data;
};

export const runQuery = async (employee_id: string, user_query: string) => {
  const response = await api.post('/query', { employee_id, user_query });
  return response.data;
};

export const getSettings = async () => {
  const response = await api.get('/settings');
  return response.data;
};

export const uploadBatch = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export default api;
