import axios from 'axios';

const API_BASE = '/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercept requests to attach Bearer JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('scout_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercept 401 Unauthorized responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('scout_token');
      localStorage.removeItem('scout_user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (username, password) => {
    const res = await apiClient.post('/auth/login', { username, password });
    localStorage.setItem('scout_token', res.data.access_token);
    localStorage.setItem('scout_user', res.data.username);
    return res.data;
  },
  logout: () => {
    localStorage.removeItem('scout_token');
    localStorage.removeItem('scout_user');
    window.location.href = '/login';
  },
  getProfile: async () => {
    const res = await apiClient.get('/auth/me');
    return res.data;
  },
};

export const scansApi = {
  list: async () => {
    const res = await apiClient.get('/scans');
    return res.data;
  },
  get: async (scanId) => {
    const res = await apiClient.get(`/scans/${scanId}`);
    return res.data;
  },
  getLogs: async (scanId) => {
    const res = await apiClient.get(`/scans/${scanId}/logs`);
    return res.data;
  },
  start: async (payload) => {
    const res = await apiClient.post('/scans', payload);
    return res.data;
  },
  cancel: async (scanId) => {
    const res = await apiClient.post(`/scans/${scanId}/cancel`);
    return res.data;
  },
  delete: async (scanId) => {
    const res = await apiClient.delete(`/scans/${scanId}`);
    return res.data;
  },
};

export const credentialsApi = {
  list: async (provider) => {
    const params = provider ? { provider } : {};
    const res = await apiClient.get('/credentials', { params });
    return res.data;
  },
  create: async (credData) => {
    const res = await apiClient.post('/credentials', credData);
    return res.data;
  },
  delete: async (id) => {
    const res = await apiClient.delete(`/credentials/${id}`);
    return res.data;
  },
};

export const dashboardApi = {
  getStats: async () => {
    const res = await apiClient.get('/dashboard/stats');
    return res.data;
  },
};

export const createScanWebSocket = (scanId, onMessage, onError, onClose) => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  const wsUrl = `${protocol}//${host}/ws/scans/${scanId}/logs`;

  const ws = new WebSocket(wsUrl);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (onMessage) onMessage(data);
    } catch (err) {
      if (onMessage) onMessage({ type: 'log', message: event.data, level: 'INFO' });
    }
  };

  ws.onerror = (err) => {
    if (onError) onError(err);
  };

  ws.onclose = () => {
    if (onClose) onClose();
  };

  return ws;
};
