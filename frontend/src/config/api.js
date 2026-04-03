/**
 * API Configuration
 * Centralized management of API endpoints for development and production
 */

// Get backend URL from environment variable or use localhost default
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

// API endpoints
export const API_ENDPOINTS = {
  UPLOAD: `${BACKEND_URL}/upload`,
  HEALTH: `${BACKEND_URL}/health`,
  TEST: `${BACKEND_URL}/test`,
};

export default {
  BACKEND_URL,
  API_ENDPOINTS,
};
