<template>
    <div class="home">
      <section class="hero">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-6">
              <h1 class="display-4 fw-bold mb-4">Simulez et optimisez vos réseaux mobiles en zones rurales</h1>
              <p class="lead mb-4">RuraNetSim est un outil puissant de simulation et dimensionnement des réseaux mobiles spécialement conçu pour les zones rurales.</p>
              <div class="d-grid gap-2 d-md-flex justify-content-md-start">
                <router-link to="/simulation" class="btn btn-primary btn-lg px-4 me-md-2">Commencer une simulation</router-link>
                <router-link to="/about" class="btn btn-outline-secondary btn-lg px-4">En savoir plus</router-link>
              </div>
            </div>
            <div class="col-lg-6 d-none d-lg-block">
              <img src="@/assets/logo.svg" alt="RuraNetSim" class="img-fluid">
            </div>
          </div>
        </div>
      </section>
      
      <section class="features py-5">
        <div class="container">
          <h2 class="text-center mb-5">Fonctionnalités principales</h2>
          <div class="row g-4">
            <div class="col-md-4">
              <div class="card h-100">
                <div class="card-body text-center">
                  <div class="feature-icon mb-3">
                    <i class="fas fa-broadcast-tower fa-3x text-primary"></i>
                  </div>
                  <h5 class="card-title">Simulation de propagation radio</h5>
                  <p class="card-text">Modèles Okumura-Hata et COST-231 pour une simulation précise de la propagation des ondes radio en fonction du terrain.</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card h-100">
                <div class="card-body text-center">
                  <div class="feature-icon mb-3">
                    <i class="fas fa-map-marked-alt fa-3x text-primary"></i>
                  </div>
                  <h5 class="card-title">Visualisation cartographique</h5>
                  <p class="card-text">Visualisez la couverture réseau sur des cartes interactives avec des données de terrain réelles.</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card h-100">
                <div class="card-body text-center">
                  <div class="feature-icon mb-3">
                    <i class="fas fa-chart-line fa-3x text-primary"></i>
                  </div>
                  <h5 class="card-title">Analyse de performance</h5>
                  <p class="card-text">Évaluez la capacité du réseau et optimisez l'emplacement des stations de base pour une couverture maximale.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section class="technologies py-5 bg-light">
        <div class="container">
          <h2 class="text-center mb-5">Technologies supportées</h2>
          <div class="row justify-content-center">
            <div class="col-md-8">
              <div class="tech-grid">
                <div class="tech-item">
                  <div class="tech-icon">2G</div>
                  <div class="tech-name">GSM</div>
                </div>
                <div class="tech-item">
                  <div class="tech-icon">3G</div>
                  <div class="tech-name">UMTS</div>
                </div>
                <div class="tech-item">
                  <div class="tech-icon">4G</div>
                  <div class="tech-name">LTE</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section class="cta py-5">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-md-10">
              <div class="card bg-primary text-white">
                <div class="card-body text-center py-5">
                  <h2 class="card-title mb-3">Prêt à optimiser votre réseau rural?</h2>
                  <p class="card-text mb-4">Commencez dès maintenant à simuler et dimensionner votre réseau mobile pour les zones rurales.</p>
                  <router-link to="/simulation" class="btn btn-light btn-lg">Lancer une simulation</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home'
  }
  </script>
  
  <style scoped>
  .hero {
    padding: 80px 0;
    background-color: var(--light-bg);
  }
  
  .features, .technologies, .cta {
    padding: 60px 0;
  }
  
  .feature-icon {
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .tech-grid {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .tech-item {
    text-align: center;
    padding: 20px;
  }
  
  .tech-icon {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--primary-color);
    margin-bottom: 10px;
  }
  
  .tech-name {
    font-size: 1rem;
  }
  </style>