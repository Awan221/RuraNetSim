<template>
    <div class="about">
      <div class="container">
        <h1 class="mb-4">À propos de RuraNetSim</h1>
        
        <div class="row">
          <div class="col-lg-8">
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">Contexte</h5>
                <p>La couverture mobile en zones rurales reste un défi majeur en raison de la topographie, du coût des infrastructures et des besoins de connectivité spécifiques. RuraNetSim vise à offrir une simulation réaliste permettant aux opérateurs et décideurs de tester différentes configurations de réseau avant déploiement.</p>
              </div>
            </div>
            
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">Objectifs du projet</h5>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">Simuler la propagation radio pour différentes technologies (2G, 3G, 4G)</li>
                  <li class="list-group-item">Visualiser la couverture réseau sur une carte interactive</li>
                  <li class="list-group-item">Optimiser l'emplacement des stations de base en tenant compte du relief et des pertes de signal</li>
                  <li class="list-group-item">Évaluer la capacité du réseau en fonction du nombre d'utilisateurs et de la bande passante</li>
                  <li class="list-group-item">Offrir une interface utilisateur intuitive permettant de configurer et d'interpréter les simulations</li>
                </ul>
              </div>
            </div>
            
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">Technologies utilisées</h5>
                <div class="row">
                  <div class="col-md-6">
                    <h6>Backend</h6>
                    <ul class="list-unstyled">
                      <li><i class="fab fa-python me-2"></i> Django</li>
                      <li><i class="fas fa-database me-2"></i> PostgreSQL</li>
                      <li><i class="fas fa-server me-2"></i> Django REST Framework</li>
                    </ul>
                  </div>
                  <div class="col-md-6">
                    <h6>Frontend</h6>
                    <ul class="list-unstyled">
                      <li><i class="fab fa-vuejs me-2"></i> Vue.js</li>
                      <li><i class="fas fa-map me-2"></i> Leaflet</li>
                      <li><i class="fas fa-chart-bar me-2"></i> Chart.js</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Perspectives d'évolution</h5>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">Intégration de la 5G et de nouveaux modèles de propagation</li>
                  <li class="list-group-item">Optimisation avec machine learning pour affiner les simulations</li>
                  <li class="list-group-item">Développement d'une version mobile pour consultation rapide</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div class="col-lg-4">
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">Responsable du projet</h5>
                <div class="text-center mb-3">
                  <img src="@/assets/profile.svg" alt="Awa Ndiaye" class="rounded-circle img-fluid" style="max-width: 150px;">
                </div>
                <h6 class="text-center">Awa Ndiaye</h6>
                <p class="text-center text-muted">Ingénieure en télécommunications</p>
              </div>
            </div>
            
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Modèles de propagation</h5>
                <div class="accordion" id="accordionModels">
                  <div class="accordion-item">
                    <h2 class="accordion-header" id="headingOne">
                      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                        Okumura-Hata
                      </button>
                    </h2>
                    <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionModels">
                      <div class="accordion-body">
                        <p>Le modèle Okumura-Hata est un modèle empirique de propagation radio utilisé pour prédire la perte de trajet dans les environnements urbains. Il est valide pour des fréquences de 150 à 1500 MHz.</p>
                      </div>
                    </div>
                  </div>
                  <div class="accordion-item">
                    <h2 class="accordion-header" id="headingTwo">
                      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                        COST-231
                      </button>
                    </h2>
                    <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionModels">
                      <div class="accordion-body">
                        <p>Le modèle COST-231 (Walfisch-Ikegami) est une extension du modèle Okumura-Hata pour les fréquences de 1500 à 2000 MHz, adapté aux environnements urbains et suburbains.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'About'
  }
  </script>