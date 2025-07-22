<template>
  <div v-if="!initializing" class="app-container">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
    <Footer />
  </div>
  <div v-else class="loading-container">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Chargement...</span>
    </div>
    <p class="mt-3">Chargement de l'application...</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import Navbar from '@/components/common/Navbar.vue';
import Footer from '@/components/common/Footer.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    Footer
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const initializing = ref(true);

    // Initialisation de l'application
    const initializeApp = async () => {
      try {
        // Vérifier l'état d'authentification et charger les données utilisateur si nécessaire
        const isAuthenticated = await store.dispatch('initializeApp');
        
        // Rediriger vers la page de connexion si non authentifié
        if (!isAuthenticated && router.currentRoute.value.meta.requiresAuth) {
          router.push('/login');
        }
      } catch (error) {
        console.error('Erreur lors de l\'initialisation de l\'application:', error);
      } finally {
        initializing.value = false;
      }
    };

    // Appeler l'initialisation au montage du composant
    onMounted(() => {
      initializeApp();
    });

    return {
      initializing
    };
  }
};
</script>

<style>
.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  background-color: #f8f9fa;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px;
}
</style>