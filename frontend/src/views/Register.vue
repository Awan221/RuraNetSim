<template>
    <div class="register">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-5">
            <div class="card">
              <div class="card-header bg-primary text-white">
                <h4 class="mb-0">Inscription</h4>
              </div>
              <div class="card-body">
                <div v-if="error" class="alert alert-danger">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ error }}
                </div>
                
                <div v-if="success" class="alert alert-success">
                  <i class="fas fa-check-circle me-2"></i>
                  {{ success }}
                </div>
                
                <form @submit.prevent="register" v-if="!success">
                  <div class="mb-3">
                    <label for="username" class="form-label">Nom d'utilisateur</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="username" 
                      v-model="formData.username" 
                      required
                      autocomplete="username"
                    >
                  </div>
                  <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input 
                      type="email" 
                      class="form-control" 
                      id="email" 
                      v-model="formData.email" 
                      required
                      autocomplete="email"
                    >
                  </div>
                  <div class="mb-3">
                    <label for="password1" class="form-label">Mot de passe</label>
                    <input 
                      type="password" 
                      class="form-control" 
                      id="password1" 
                      v-model="formData.password1" 
                      required
                      autocomplete="new-password"
                    >
                  </div>
                  <div class="mb-3">
                    <label for="password2" class="form-label">Confirmer le mot de passe</label>
                    <input 
                      type="password" 
                      class="form-control" 
                      id="password2" 
                      v-model="formData.password2" 
                      required
                      autocomplete="new-password"
                    >
                  </div>
                  <div class="mb-3">
                    <label for="organization" class="form-label">Organisation (optionnel)</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="organization" 
                      v-model="formData.organization"
                    >
                  </div>
                  <div class="d-grid">
                    <button type="submit" class="btn btn-primary" :disabled="isLoading">
                      <span v-if="isLoading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                      S'inscrire
                    </button>
                  </div>
                </form>
                
                <div class="mt-3 text-center">
                  <p>Vous avez déjà un compte? <router-link to="/login">Connectez-vous</router-link></p>
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
    name: 'Register',
    data() {
      return {
        formData: {
          username: '',
          email: '',
          password1: '',
          password2: '',
          organization: ''
        },
        error: null,
        success: null
      }
    },
    computed: {
      ...mapGetters(['isLoading'])
    },
    methods: {
      async register() {
        try {
          this.error = null
          this.success = null
          
          // Validate passwords match
          if (this.formData.password1 !== this.formData.password2) {
            this.error = 'Les mots de passe ne correspondent pas'
            return
          }
          
          await this.$store.dispatch('register', {
            username: this.formData.username,
            email: this.formData.email,
            password: this.formData.password1,
            organization: this.formData.organization
          })
          
          this.success = 'Inscription réussie! Vous pouvez maintenant vous connecter.'
          this.formData = {
            username: '',
            email: '',
            password1: '',
            password2: '',
            organization: ''
          }
        } catch (error) {
          this.error = error.response?.data?.detail || 'Erreur lors de l\'inscription'
          console.error('Registration error:', error)
        }
      }
    }
  }
  </script>