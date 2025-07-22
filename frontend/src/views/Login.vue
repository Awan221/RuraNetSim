<template>
    <div class="login">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-5">
            <div class="card">
              <div class="card-header bg-primary text-white">
                <h4 class="mb-0">Connexion</h4>
              </div>
              <div class="card-body">
                <div v-if="error" class="alert alert-danger">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ error }}
                </div>
                
                <form @submit.prevent="login">
                  <div class="mb-3">
                    <label for="username" class="form-label">Nom d'utilisateur</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="username" 
                      v-model="username" 
                      required
                      autocomplete="username"
                    >
                  </div>
                  <div class="mb-3">
                    <label for="password" class="form-label">Mot de passe</label>
                    <input 
                      type="password" 
                      class="form-control" 
                      id="password" 
                      v-model="password" 
                      required
                      autocomplete="current-password"
                    >
                  </div>
                  <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="remember" v-model="remember">
                    <label class="form-check-label" for="remember">Se souvenir de moi</label>
                  </div>
                  <div class="d-grid">
                    <button type="submit" class="btn btn-primary" :disabled="isLoading">
                      <span v-if="isLoading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                      Connexion
                    </button>
                  </div>
                </form>
                
                <div class="mt-3 text-center">
                  <p>Vous n'avez pas de compte? <router-link to="/register">Inscrivez-vous</router-link></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'Login',
    data() {
      return {
        username: '',
        password: '',
        remember: false,
        error: null
      }
    },
    computed: {
      ...mapGetters(['isLoading', 'isAuthenticated'])
    },
    created() {
      if (this.isAuthenticated) {
        const redirect = this.$route.query.redirect || '/dashboard'
        this.$router.push(redirect)
      }
    },
    methods: {
      async login() {
        try {
          this.error = null
          await this.$store.dispatch('login', {
            username: this.username,
            password: this.password
          })
          
          // Rediriger vers le tableau de bord par défaut
          const redirect = this.$route.query.redirect || '/dashboard'
          this.$router.push(redirect)
        } catch (error) {
          this.error = error.response?.data?.detail || 'Identifiants incorrects'
          console.error('Login error:', error)
        }
      }
    }
  }
  </script>