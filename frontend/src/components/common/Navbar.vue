<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">
          <i class="fas fa-broadcast-tower me-2"></i>
          RuraNetSim
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Accueil</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" to="/simulation">Simulation</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" to="/simulations">Mes simulations</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/about">À propos</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <template v-if="isAuthenticated">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="fas fa-user me-1"></i> {{ currentUser ? currentUser.username : 'Utilisateur' }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                  <li><a class="dropdown-item" href="#"><i class="fas fa-cog me-1"></i> Paramètres</a></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" href="#" @click.prevent="logout"><i class="fas fa-sign-out-alt me-1"></i> Déconnexion</a></li>
                </ul>
              </li>
            </template>
            <template v-else>
              <li class="nav-item">
                <router-link class="nav-link" to="/login">Connexion</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/register">Inscription</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'Navbar',
    computed: {
      ...mapGetters(['isAuthenticated', 'currentUser'])
    },
    methods: {
      logout() {
        this.$store.dispatch('logout')
        this.$router.push('/login')
      }
    }
  }
  </script>