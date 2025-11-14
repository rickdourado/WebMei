import axios from 'axios';

const API_BASE_URL = 'http://localhost:5010/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Configurações
  getConfig: () => api.get('/config'),

  // Serviços
  getServicos: () => api.get('/servicos'),
  getServico: (filename) => api.get(`/servicos/${filename}`),
  createServico: (data) => api.post('/servicos', data),
  deleteServico: (filename) => api.delete(`/admin/servicos/${filename}`),
  downloadServico: (filename) => `${API_BASE_URL}/download/${filename}`,

  // Autenticação
  login: (username, password) => api.post('/auth/login', { username, password }),
  logout: () => api.post('/auth/logout'),
  checkAuth: () => api.get('/auth/check'),
};

export default api;
