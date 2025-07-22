# RuraNetSim

Outil avancé de simulation et de dimensionnement des réseaux mobiles en zones rurales.

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Démonstration](#-démonstration)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Déploiement](#-déploiement)
- [Documentation](#-documentation)

## 🌍 Présentation

RuraNetSim est une solution complète conçue pour les opérateurs télécoms et les décideurs souhaitant évaluer et optimiser le déploiement de réseaux mobiles en zones rurales ou à faible densité de population. L'outil permet de modéliser différents scénarios de couverture réseau en tenant compte des spécificités géographiques et topographiques des zones concernées.

### Objectifs principaux

- **Prédiction précise** de la couverture réseau dans des environnements ruraux
- **Optimisation des coûts** de déploiement des infrastructures
- **Analyse comparative** entre différentes technologies (2G, 3G, 4G, 5G)
- **Aide à la décision** pour les investissements en infrastructures

## ✨ Fonctionnalités

### 🛰️ Simulation de propagation radio
- Support des principales technologies mobiles (2G, 3G, 4G, 5G)
- Modèles de propagation avancés (Okumura-Hata, COST-231, SUI, etc.)
- Prise en compte des obstacles naturels et du relief
- Simulation multi-fréquences et multi-technologies

### 🗺️ Visualisation interactive
- Carte géographique interactive avec couches personnalisables
- Affichage des zones de couverture avec code couleur
- Visualisation 3D du terrain et des signaux
- Export des cartes et rapports au format PDF/PNG

### 📊 Analyse et rapports
- Tableau de bord personnalisable avec indicateurs clés
- Rapports détaillés sur la qualité de service
- Analyse comparative des scénarios
- Export des données au format CSV/Excel

### 🔧 Outils avancés
- Optimisation automatique de l'emplacement des antennes
- Calcul du bilan de liaison
- Estimation des coûts de déploiement
- Gestion des interférences

## 🛠️ Technologies utilisées

### Backend
- **Framework**: Django 4.2+
- **Base de données**: PostgreSQL avec PostGIS
- **API**: Django REST Framework
- **Calculs scientifiques**: NumPy, SciPy
- **Traitement géospatial**: GDAL, GeoDjango
- **Cache**: Redis
- **File d'attente**: Celery

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **Cartographie**: Leaflet, OpenStreetMap
- **Visualisation**: Chart.js, Plotly.js
- **UI/UX**: Bootstrap 5, Font Awesome
- **Gestion d'état**: Vuex
- **Routage**: Vue Router

### Modèles de propagation
- Okumura-Hata (zones urbaines, suburbaines et rurales)
- COST-231 Hata
- SUI (Stanford University Interim)
- Modèles propriétaires adaptés aux environnements ruraux

### Infrastructure
- **Conteneurisation**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)

## 📚 Documentation

Pour une documentation technique complète, consultez notre [rapport technique détaillé](docs/RAPPORT_TECHNIQUE_RuraNetSim.md). Ce document couvre :

- L'architecture technique détaillée
- Les modèles de propagation implémentés
- Les cas d'utilisation avancés
- Les résultats des tests de performance
- Les bonnes pratiques de déploiement

## 🎥 Démonstration

Pour voir RuraNetSim en action, consultez notre démonstration vidéo complète :

[![Voir la démonstration](https://img.shields.io/badge/📽️-Voir_la_démo_sur_Google_Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/drive/folders/1IPg1VfdGOkxCZcscHfsOJHletF3OX6TO?usp=sharing)

Cette vidéo couvre :
- L'interface utilisateur et la navigation
- La création d'une nouvelle simulation
- L'analyse des résultats
- L'export des rapports

## 🚀 Installation

### Prérequis

- Docker 20.10+
- Docker Compose 2.0+
- Git
- 4 Go de RAM minimum (8 Go recommandés)

### Étapes d'installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/username/ruranet_sim.git
   cd ruranet_sim
   ```

2. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   # Éditer le fichier .env selon vos besoins
   ```

3. **Démarrer les services**
   ```bash
   docker-compose up --build -d
   ```

4. **Appliquer les migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Créer un superutilisateur (admin)**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

6. **Accéder à l'application**
   - Frontend: http://localhost:8080
   - Backend admin: http://localhost:8000/admin
   - API documentation: http://localhost:8000/api/docs/

## ⚙️ Configuration

Le fichier `.env` à la racine du projet permet de configurer :

- **Variables Django** : SECRET_KEY, DEBUG, ALLOWED_HOSTS
- **Base de données** : Noms d'utilisateur, mots de passe, hôte
- **Cache** : Configuration Redis
- **CORS** : Origines autorisées
- **Stockage** : Configuration pour les fichiers statiques et médias
- **Email** : Paramètres SMTP pour les notifications

## 🖥️ Utilisation

### 1. Création d'un compte
- Inscrivez-vous via le formulaire d'inscription
- Validez votre adresse email (si activé)
- Connectez-vous avec vos identifiants

### 2. Créer une nouvelle simulation
1. Accédez à l'onglet "Nouvelle simulation"
2. Sélectionnez la zone d'étude sur la carte
3. Configurez les paramètres de simulation (technologie, fréquence, puissance, etc.)
4. Lancez la simulation

### 3. Analyser les résultats
- Visualisez la couverture sur la carte interactive
- Consultez les indicateurs de performance
- Exportez les résultats au format souhaité

### 4. Gérer les projets
- Créez des dossiers pour organiser vos simulations
- Partagez les résultats avec votre équipe
- Suivez l'historique des modifications

## ☁️ Déploiement

### Environnement de production

1. **Configurer un serveur** (ex: Ubuntu 22.04 LTS)
2. **Installer Docker et Docker Compose**
3. **Configurer un reverse proxy** (Nginx recommandé)
4. **Mettre en place SSL** avec Let's Encrypt
5. **Configurer les sauvegardes**

### Variables critiques pour la production
- `DEBUG=False`
- `SECRET_KEY` fort et sécurisé
- `ALLOWED_HOSTS` correctement configuré
- `DATABASE_URL` pour la base de données
- `CORS_ALLOWED_ORIGINS` restreint aux domaines autorisés

<div align="center">
  Projet réalisé dans le cadre du cours de Réseaux Télécoms - DIC2 Informatique - 2025
</div>
