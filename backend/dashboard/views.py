from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, F, Q
from simulation.models import Simulation, SimulationParameter
from django.utils import timezone
from datetime import timedelta
import json

class DashboardStatsView(APIView):
    """
    Vue pour récupérer les statistiques du tableau de bord
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Récupère les filtres de la requête
        period = request.query_params.get('period', '7days')
        technology = request.query_params.get('technology', 'all')
        area_type = request.query_params.get('areaType', 'all')

        # Calcule la date de début en fonction de la période
        end_date = timezone.now()
        if period == '7days':
            start_date = end_date - timedelta(days=7)
        elif period == '30days':
            start_date = end_date - timedelta(days=30)
        elif period == '90days':
            start_date = end_date - timedelta(days=90)
        else:  # all
            start_date = timezone.make_aware(timezone.datetime.min)

        # Filtre de base pour les simulations de l'utilisateur
        simulations = Simulation.objects.filter(
            user=request.user,
            created_at__range=(start_date, end_date)
        )

        # Filtres supplémentaires
        if technology != 'all':
            simulations = simulations.filter(parameters__technology=technology)
        
        if area_type != 'all':
            simulations = simulations.filter(parameters__terrain_type=area_type)

        # Statistiques de base
        total_simulations = simulations.count()
        
        # Statistiques par statut
        status_stats = simulations.values('status').annotate(count=Count('id'))
        
        # Couverture moyenne
        avg_coverage = simulations.aggregate(avg=Avg('coverage_percentage'))['avg'] or 0
        
        # Dernières simulations
        recent_simulations = simulations.order_by('-created_at')[:5].values(
            'id', 'name', 'status', 'coverage_percentage', 'created_at'
        )
        
        # Statistiques par technologie
        tech_stats = simulations.values('parameters__technology').annotate(
            count=Count('id'),
            avg_coverage=Avg('coverage_percentage')
        )
        
        # Statistiques par type de zone
        area_stats = simulations.values('parameters__terrain_type').annotate(
            count=Count('id'),
            avg_coverage=Avg('coverage_percentage')
        )

        # Préparation de la réponse
        response_data = {
            'period': {
                'start': start_date,
                'end': end_date,
                'label': period
            },
            'total_simulations': total_simulations,
            'avg_coverage': round(avg_coverage, 1),
            'status_distribution': {s['status']: s['count'] for s in status_stats},
            'tech_distribution': {
                s['parameters__technology']: {
                    'count': s['count'],
                    'avg_coverage': round(s['avg_coverage'] or 0, 1)
                } for s in tech_stats
            },
            'area_distribution': {
                s['parameters__terrain_type']: {
                    'count': s['count'],
                    'avg_coverage': round(s['avg_coverage'] or 0, 1)
                } for s in area_stats
            },
            'recent_simulations': list(recent_simulations)
        }

        return Response(response_data)


class CoverageDataView(APIView):
    """
    Vue pour récupérer les données de couverture pour la carte
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Récupère les filtres de la requête
        period = request.query_params.get('period', '7days')
        technology = request.query_params.get('technology', 'all')
        area_type = request.query_params.get('areaType', 'all')

        # Calcule la date de début en fonction de la période
        end_date = timezone.now()
        if period == '7days':
            start_date = end_date - timedelta(days=7)
        elif period == '30days':
            start_date = end_date - timedelta(days=30)
        elif period == '90days':
            start_date = end_date - timedelta(days=90)
        else:  # all
            start_date = timezone.make_aware(timezone.datetime.min)

        # Filtre de base pour les simulations de l'utilisateur
        simulations = Simulation.objects.filter(
            user=request.user,
            created_at__range=(start_date, end_date)
        )

        # Filtres supplémentaires
        if technology != 'all':
            simulations = simulations.filter(parameters__technology=technology)
        
        if area_type != 'all':
            simulations = simulations.filter(parameters__terrain_type=area_type)

        # Récupère les données de couverture
        # Note: Cette partie dépend de votre modèle de données pour la couverture
        # Voici un exemple basé sur des hypothèses
        coverage_data = []
        
        for sim in simulations:
            try:
                # Supposons que vous ayez un champ 'coverage_data' qui stocke les données de couverture
                if hasattr(sim, 'coverage_data') and sim.coverage_data:
                    coverage_data.append({
                        'simulation_id': sim.id,
                        'name': sim.name,
                        'coverage': sim.coverage_percentage,
                        'data': sim.coverage_data  # Doit être un GeoJSON ou un format similaire
                    })
            except Exception as e:
                print(f"Erreur lors du traitement des données de couverture pour la simulation {sim.id}: {e}")

        return Response({
            'count': len(coverage_data),
            'results': coverage_data
        })


class PerformanceMetricsView(APIView):
    """
    Vue pour récupérer les métriques de performance détaillées
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Récupère les filtres de la requête
        period = request.query_params.get('period', '7days')
        technology = request.query_params.get('technology', 'all')
        area_type = request.query_params.get('areaType', 'all')

        # Calcule la date de début en fonction de la période
        end_date = timezone.now()
        if period == '7days':
            start_date = end_date - timedelta(days=7)
        elif period == '30days':
            start_date = end_date - timedelta(days=30)
        elif period == '90days':
            start_date = end_date - timedelta(days=90)
        else:  # all
            start_date = timezone.make_aware(timezone.datetime.min)

        # Filtre de base pour les simulations de l'utilisateur
        simulations = Simulation.objects.filter(
            user=request.user,
            created_at__range=(start_date, end_date)
        )

        # Filtres supplémentaires
        if technology != 'all':
            simulations = simulations.filter(parameters__technology=technology)
        
        if area_type != 'all':
            simulations = simulations.filter(parameters__terrain_type=area_type)

        # Calcule les métriques de performance
        metrics = simulations.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            failed=Count('id', filter=Q(status='failed')),
            running=Count('id', filter=Q(status='running')),
            avg_coverage=Avg('coverage_percentage'),
            avg_signal_strength=Avg('signal_strength'),
            avg_throughput=Avg('throughput')
        )

        # Calcule les tendances (comparaison avec la période précédente)
        previous_start = start_date - (end_date - start_date)
        previous_simulations = Simulation.objects.filter(
            user=request.user,
            created_at__range=(previous_start, start_date)
        )
        
        if technology != 'all':
            previous_simulations = previous_simulations.filter(parameters__technology=technology)
        
        if area_type != 'all':
            previous_simulations = previous_simulations.filter(parameters__terrain_type=area_type)

        previous_metrics = previous_simulations.aggregate(
            total=Count('id'),
            avg_coverage=Avg('coverage_percentage')
        )

        # Calcule les variations
        total_change = self.calculate_change(metrics['total'], previous_metrics['total'])
        coverage_change = self.calculate_change(
            metrics['avg_coverage'] or 0, 
            previous_metrics['avg_coverage'] or 0
        )

        # Prépare la réponse
        response_data = {
            'summary': {
                'total_simulations': metrics['total'],
                'total_change': total_change,
                'completed_simulations': metrics['completed'],
                'failed_simulations': metrics['failed'],
                'running_simulations': metrics['running'],
                'success_rate': (metrics['completed'] / metrics['total'] * 100) if metrics['total'] > 0 else 0,
                'avg_coverage': metrics['avg_coverage'] or 0,
                'coverage_change': coverage_change,
                'avg_signal_strength': metrics['avg_signal_strength'] or 0,
                'avg_throughput': metrics['avg_throughput'] or 0
            },
            'period': {
                'current': {
                    'start': start_date,
                    'end': end_date,
                    'label': period
                },
                'previous': {
                    'start': previous_start,
                    'end': start_date,
                    'label': f'previous_{period}'
                }
            }
        }

        return Response(response_data)

    def calculate_change(self, current, previous):
        """Calcule le pourcentage de changement entre deux valeurs"""
        if previous == 0:
            return 100 if current > 0 else 0
        return round(((current - previous) / previous) * 100, 1)
