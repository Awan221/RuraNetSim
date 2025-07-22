<template>
    <footer class="footer mt-auto py-3 bg-dark text-white">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <h5>RuraNetSim</h5>
            <p class="text-muted">Outil de simulation et dimensionnement des réseaux mobiles en zones rurales</p>
          </div>
          <div class="col-md-3">
            <h5>Liens</h5>
            <ul class="list-unstyled">
              <li><router-link to="/" class="text-white">Accueil</router-link></li>
              <li><router-link to="/simulation" class="text-white">Simulation</router-link></li>
              <li><router-link to="/about" class="text-white">À propos</router-link></li>
            </ul>
          </div>
          <div class="col-md-3">
            <h5>Contact</h5>
            <ul class="list-unstyled">
              <li><a href="mailto:contact@ruranetsim.com" class="text-white">contact@ruranetsim.com</a></li>
              <li><a href="https://github.com/ruranetsim" target="_blank" class="text-white"><i class="fab fa-github me-1"></i> GitHub</a></li>
            </ul>
          </div>
        </div>
        <hr>
        <div class="text-center">
          <p>&copy; {{ new Date().getFullYear() }} RuraNetSim. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  </template>
  
  <script>
  export default {
    name: 'Footer'
  }
  </script>