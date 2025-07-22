from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SimulationViewSet, FiveGSimulationViewSet
from .auth import register, login

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'simulations', SimulationViewSet)

# Créer un routeur pour les vues 5G
fiveg_router = DefaultRouter()
fiveg_router.register(r'5g', FiveGSimulationViewSet, basename='5g-simulations')

# URL d'authentification personnalisées
urlpatterns = [
    path('', include(router.urls)),
    path('api/5g/', include(fiveg_router.urls)),  # Nouveaux endpoints 5G
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
]