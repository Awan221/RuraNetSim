import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8000/api/dashboard';

// Configuration d'axios pour inclure le token d'authentification
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    ...authHeader()
  },
  withCredentials: true
});

/**
 * Récupère les statistiques du tableau de bord
 * @param {Object} filters - Les filtres à appliquer
 * @returns {Promise} - Les statistiques du tableau de bord
 */
const getDashboardStats = async (filters = {}) => {
  try {
    const response = await api.get('/stats', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des statistiques:', error);
    throw error;
  }
};

/**
 * Récupère les simulations récentes
 * @param {number} limit - Nombre maximum de simulations à récupérer
 * @returns {Promise} - Les simulations récentes
 */
const getRecentSimulations = async (limit = 5) => {
  try {
    const response = await api.get('/recent-simulations', {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des simulations récentes:', error);
    throw error;
  }
};

/**
 * Récupère les données de couverture pour la carte
 * @param {Object} filters - Les filtres à appliquer
 * @returns {Promise} - Les données de couverture
 */
const getCoverageData = async (filters = {}) => {
  try {
    const response = await api.get('/coverage', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des données de couverture:', error);
    throw error;
  }
};

/**
 * Récupère les métriques de performance
 * @param {Object} filters - Les filtres à appliquer
 * @returns {Promise} - Les métriques de performance
 */
const getPerformanceMetrics = async (filters = {}) => {
  try {
    const response = await api.get('/performance-metrics', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des métriques de performance:', error);
    throw error;
  }
};

// Gestion des erreurs d'authentification
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Rediriger vers la page de connexion si l'utilisateur n'est pas authentifié
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default {
  getDashboardStats,
  getRecentSimulations,
  getCoverageData,
  getPerformanceMetrics
};
