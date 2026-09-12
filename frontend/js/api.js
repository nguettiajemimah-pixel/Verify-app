/* API client for VERIFY GH */

const API_BASE_URL = 'https://verify-backend-3d2z.onrender.com';

class ApiClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async patch(endpoint, data) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // Products
  async searchProducts(query, category = null) {
    const params = new URLSearchParams({ query });
    if (category) params.append('category', category);
    return this.get(`/products/search?${params}`);
  }

  async getProduct(productId) {
    return this.get(`/products/${productId}`);
  }

  // Verifications
  async createVerification(data) {
    return this.post('/verifications', data);
  }

  async getVerification(verificationId) {
    return this.get(`/verifications/${verificationId}`);
  }

  // Reports
  async createReport(data) {
    return this.post('/reports', data);
  }

  async getReports(status = null) {
    const params = status ? `?status=${status}` : '';
    return this.get(`/reports${params}`);
  }

  async getReport(reportId) {
    return this.get(`/reports/${reportId}`);
  }

  async updateReportStatus(reportId, data) {
    return this.patch(`/reports/${reportId}`, data);
  }

  // Auth
  async login(email, password) {
    return this.post('/auth/login', { email, password });
  }

  async register(email, password, role = 'CONSUMER') {
    return this.post('/auth/register', { email, password, role });
  }

  async getCurrentUser() {
    return this.get('/auth/me');
  }

  // Dashboard
  async getDashboardSummary() {
    return this.get('/dashboard/summary');
  }

  async getRecentReports(limit = 10) {
    return this.get(`/dashboard/recent-reports?limit=${limit}`);
  }
}

const api = new ApiClient();
