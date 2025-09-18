/**
 * API utility functions for making authenticated requests
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Get the stored access token from localStorage
 */
const getAuthToken = () => {
  return localStorage.getItem('accessToken');
};

/**
 * Get common headers for API requests
 */
const getHeaders = (includeAuth = true) => {
  const headers = {
    'Content-Type': 'application/json',
  };

  if (includeAuth) {
    const token = getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  return headers;
};

/**
 * Make an authenticated API request
 */
export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const {
    method = 'GET',
    body,
    includeAuth = true,
    ...fetchOptions
  } = options;

  const config = {
    method,
    headers: getHeaders(includeAuth),
    ...fetchOptions,
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, config);
    
    // Handle different response types
    if (response.headers.get('content-type')?.includes('application/json')) {
      const data = await response.json();
      return { response, data };
    } else {
      const text = await response.text();
      return { response, data: text };
    }
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

/**
 * Make a GET request
 */
export const apiGet = async (endpoint, options = {}) => {
  const { response, data } = await apiRequest(endpoint, { method: 'GET', ...options });
  
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  
  return data;
};

/**
 * Make a POST request
 */
export const apiPost = (endpoint, body, options = {}) => {
  return apiRequest(endpoint, { method: 'POST', body, ...options });
};

/**
 * Make a PUT request
 */
export const apiPut = (endpoint, body, options = {}) => {
  return apiRequest(endpoint, { method: 'PUT', body, ...options });
};

/**
 * Make a DELETE request
 */
export const apiDelete = (endpoint, options = {}) => {
  return apiRequest(endpoint, { method: 'DELETE', ...options });
};

/**
 * Make a PATCH request
 */
export const apiPatch = (endpoint, body, options = {}) => {
  return apiRequest(endpoint, { method: 'PATCH', body, ...options });
};

/**
 * Handle API response and throw errors for non-2xx status codes
 */
export const handleApiResponse = async (response) => {
  if (!response.ok) {
    let errorMessage = `Request failed with status ${response.status}`;
    
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.message || errorMessage;
    } catch {
      // If response is not JSON, use the status text
      errorMessage = response.statusText || errorMessage;
    }
    
    throw new Error(errorMessage);
  }
  
  return response;
};

/**
 * Make an authenticated API request with error handling
 */
export const authenticatedRequest = async (endpoint, options = {}) => {
  const { response, data } = await apiRequest(endpoint, options);
  await handleApiResponse(response);
  return data;
};

export default {
  apiRequest,
  apiGet,
  apiPost,
  apiPut,
  apiDelete,
  apiPatch,
  handleApiResponse,
  authenticatedRequest,
  getAuthToken,
  getHeaders,
};
