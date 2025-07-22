import { createStore } from 'vuex'
import axios from 'axios'
import dashboard from './modules/dashboard'

// URL de l'API
const API_URL = 'http://localhost:8000/api'
console.log('API URL:', API_URL)

// Configuration d'axios pour inclure le token d'authentification par défaut
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Token ${token}`
}

export default createStore({
  modules: {
    dashboard
  },
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    simulations: [],
    currentSimulation: null,
    loading: false,
    error: null
  },
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user,
    simulations: state => state.simulations,
    currentSimulation: state => state.currentSimulation,
    isLoading: state => state.loading,
    error: state => state.error
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        //console.log('En-tête d\'autorisation défini pour les requêtes API')
      } else {
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
        //console.log('En-tête d\'autorisation supprimé')
      }
    },
    CLEAR_AUTH(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('token')
    },
    SET_SIMULATIONS(state, simulations) {
      state.simulations = simulations
    },
    SET_CURRENT_SIMULATION(state, simulation) {
      state.currentSimulation = simulation
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    // Action pour initialiser l'application
    async initializeApp({ commit, dispatch }) {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          // Vérifier si le token est toujours valide
          const response = await axios.get(`${API_URL}/users/me/`)
          commit('SET_USER', response.data)
          commit('SET_TOKEN', token)
          // Charger les données de l'utilisateur
          await dispatch('fetchSimulations')
          return true
        } catch (error) {
          console.error('Erreur lors de la vérification de la session:', error)
          // Si le token n'est plus valide, déconnecter l'utilisateur
          commit('CLEAR_AUTH')
          return false
        }
      }
      return false
    },

    // Récupérer les scénarios 5G disponibles
    async fetch5GScenarios({ commit }) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await axios.get(`${API_URL}/5g/5g/get_5g_scenarios/`)
        return response.data
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors de la récupération des scénarios 5G')
        console.error('Erreur 5G:', error)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // Exécuter une simulation 5G
    async run5GSimulation({ commit, state }, simulationData) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        // Préparer les données pour l'API
        const data = {
          ...simulationData,
          technology: '5G',  // Forcer la technologie à 5G
          propagation_model: '3GPP_TR_38901'  // Forcer le modèle 3GPP pour la 5G
        }
        
        // S'assurer que les paramètres 5G sont inclus
        if (simulationData.network5GParams) {
          Object.assign(data, simulationData.network5GParams)
        }
        
        const response = await axios.post(
          `${API_URL}/5g/5g/run_5g_simulation/`,
          data,
          {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Token ${state.token}`
            }
          }
        )
        
        // Recharger la liste des simulations
        await this.dispatch('fetchSimulations')
        
        return response.data
      } catch (error) {
        let errorMessage = 'Erreur lors de l\'exécution de la simulation 5G'
        
        if (error.response) {
          if (error.response.data && error.response.data.error) {
            errorMessage = error.response.data.error
          } else if (error.response.status === 400) {
            errorMessage = 'Données de simulation invalides'
          } else if (error.response.status === 401) {
            errorMessage = 'Authentification requise'
          } else if (error.response.status >= 500) {
            errorMessage = 'Erreur serveur lors de la simulation 5G'
          }
        }
        
        commit('SET_ERROR', errorMessage)
        console.error('Erreur 5G:', error.response?.data || error.message)
        throw new Error(errorMessage)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async login({ commit, dispatch }, credentials) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null) // Réinitialiser les erreurs précédentes
        
        // Vérifier que les identifiants sont valides
        if (!credentials.username || !credentials.password) {
          throw new Error('Veuillez fournir un nom d\'utilisateur et un mot de passe')
        }
        
        // Configuration de la requête pour forcer le format JSON
        const config = {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          // Ne pas suivre les redirections
          validateStatus: status => status >= 200 && status < 300
        }
        
        const response = await axios.post(
          `${API_URL}/auth/login/`, 
          JSON.stringify(credentials),
          config
        )
        
        // Vérifier que la réponse contient bien un token
        if (!response.data || !response.data.token) {
          throw new Error('Réponse du serveur invalide')
        }
        
        // Mettre à jour le token et les informations utilisateur
        commit('SET_TOKEN', response.data.token)
        commit('SET_USER', response.data.user || { username: credentials.username })
        
        // Configurer l'en-tête d'autorisation pour les requêtes futures
        axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`
        
        return response
      } catch (error) {
        let errorMessage = 'Échec de la connexion'
        
        if (error.response) {
          // Erreur de l'API
          if (error.response.status === 400 || error.response.status === 401) {
            errorMessage = 'Nom d\'utilisateur ou mot de passe incorrect'
          } else if (error.response.data && error.response.data.detail) {
            errorMessage = error.response.data.detail
          }
        } else if (error.message) {
          // Erreur réseau ou autre
          errorMessage = error.message
        }
        
        // Nettoyer les informations d'authentification en cas d'erreur
        commit('CLEAR_AUTH')
        delete axios.defaults.headers.common['Authorization']
        
        // Définir le message d'erreur
        const errorObj = new Error(errorMessage)
        errorObj.response = error.response
        commit('SET_ERROR', errorMessage)
        throw errorObj
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async register({ commit }, userData) {
      try {
        commit('SET_LOADING', true)
        const response = await axios.post(`${API_URL}/auth/register/`, userData)
        return response
      } catch (error) {
        commit('SET_ERROR', error.response ? error.response.data : error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    logout({ commit }) {
      commit('CLEAR_AUTH')
    },
    async fetchSimulations({ commit, state }) {
      try {
        commit('SET_LOADING', true);
        console.log('Récupération des simulations avec le token:', state.token ? 'token présent' : 'pas de token');
        
        const response = await axios.get(`${API_URL}/simulations/`, {
          headers: { 'Authorization': `Token ${state.token}` }
        });
        
        console.log('Réponse de l\'API pour /simulations/:', response.data);
        
        // Gestion de la réponse paginée
        let simulations = [];
        if (response.data && response.data.results) {
          // Format de réponse paginée
          simulations = response.data.results;
          console.log(`Récupération de ${simulations.length} simulations (total: ${response.data.count})`);
        } else if (Array.isArray(response.data)) {
          // Format de réponse simple (tableau)
          simulations = response.data;
        } else {
          console.warn("Format de réponse inattendu de l'API :", response.data);
        }
        
        commit('SET_SIMULATIONS', simulations);
        return simulations;
      } catch (error) {
        console.error('Erreur lors de la récupération des simulations :', error);
        commit('SET_ERROR', error.response ? error.response.data : error.message);
        commit('SET_SIMULATIONS', []); // Assure un tableau vide en cas d'erreur
        return [];
      } finally {
        commit('SET_LOADING', false);
      }
    },
    async fetchSimulation({ commit, state }, id) {
      try {
        commit('SET_LOADING', true)
        const response = await axios.get(`${API_URL}/simulations/${id}/`, {
          //headers: { Authorization: `Token ${state.token}` }
        })
        commit('SET_CURRENT_SIMULATION', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response ? error.response.data : error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async runSimulation({ commit, state }, simulationData) {
      try {
        commit('SET_LOADING', true)
        const response = await axios.post(`${API_URL}/simulation/run/`, simulationData, {
          //headers: { Authorization: `Token ${state.token}` }
        })
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response ? error.response.data : error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async deleteSimulation({ commit, state }, id) {
      try {
        await axios.delete(`${API_URL}/simulations/${id}/`, {
          //headers: { Authorization: `Token ${state.token}` }
        });
        // Mettre à jour la liste des simulations après suppression
        const updatedSimulations = state.simulations.filter(sim => sim.id !== id);
        commit('SET_SIMULATIONS', updatedSimulations);
        return true;
      } catch (error) {
        commit('SET_ERROR', error.response ? error.response.data : error.message);
        throw error;
      }
    },
    async exportSimulationPdf({commit,state }, simulationId) {
      try {
        const response = await axios.get(`${API_URL}/simulation/export/${simulationId}/`, {
          //headers: { Authorization: `Token ${state.token}` },
          responseType: 'blob'
        })
        
        // Create a blob link to download
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `simulation_${simulationId}.pdf`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        
        return response
      } catch (error) {
        commit('SET_ERROR', error.response ? error.response.data : error.message)
        throw error
      }
    }
  }
})