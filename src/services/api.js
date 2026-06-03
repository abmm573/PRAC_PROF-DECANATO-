import axios from 'axios';

// Creamos una instancia configurada para apuntar a tu FastAPI local
const api = axios.create({
  baseURL: 'http://localhost:8000/api', 
});

// Interceptor: Adjunta el Token automáticamente a cada petición
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token_acceso');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;