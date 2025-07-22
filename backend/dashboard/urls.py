from django.urls import path
from . import views

urlpatterns = [
    # Statistiques globales du tableau de bord
    path('stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    
    # Données de couverture pour la carte
    path('coverage/', views.CoverageDataView.as_view(), name='coverage-data'),
    
    # Métriques de performance détaillées
    path('performance-metrics/', views.PerformanceMetricsView.as_view(), name='performance-metrics'),
]
