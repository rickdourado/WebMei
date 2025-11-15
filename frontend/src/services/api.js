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
  getServico: (servicoId) => api.get(`/servicos/${servicoId}`),
  createServico: (data) => api.post('/servicos', data),
  deleteServico: (servicoId) => api.delete(`/admin/servicos/${servicoId}`),
  downloadServico: (servicoId) => `${API_BASE_URL}/servicos/${servicoId}/export`,

  // Autenticação
  login: (username, password) => api.post('/auth/login', { username, password }),
  logout: () => api.post('/auth/logout'),
  checkAuth: () => api.get('/auth/check'),
};

export default api;
