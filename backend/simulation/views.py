from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
import json
import folium
import numpy as np
from django.contrib.gis.geos import Point, MultiPolygon, Polygon
from .models import Simulation, SimulationParameter, SimulationResult
from .propagation.okumura_hata import calculate_path_loss as okumura_hata_path_loss
from .propagation.cost_231 import calculate_path_loss as cost_231_path_loss
from .propagation_models_5g import (
    ThreeGPP_TR_38901 as FiveGPropagationModel,
    MillimeterWavePropagation
)

def get_available_5g_models():
    """Retourne la liste des modèles 5G disponibles"""
    return [
        {
            'id': '3GPP_TR_38901',
            'name': '3GPP TR 38.901',
            'description': 'Modèle 3GPP TR 38.901 pour les bandes FR1 et FR2',
            'scenarios': ['UMa', 'UMi', 'RMa', 'InH-Office', 'InH-ShoppingMall']
        },
        {
            'id': 'mmWave',
            'name': 'Ondes millimétriques',
            'description': 'Modèle pour les fréquences millimétriques (24-100 GHz)',
            'scenarios': ['LOS', 'NLOS']
        }
    ]

def get_5g_model_parameters(model_id):
    """Retourne les paramètres requis pour un modèle 5G spécifique"""
    if model_id == '3GPP_TR_38901':
        return {
            'required': ['scenario', 'los_condition', 'h_bs', 'h_ut'],
            'optional': ['h', 'w', 'h_roof', 'street_width'],
            'defaults': {
                'h': 20.0,
                'w': 20.0,
                'h_roof': 20.0,
                'street_width': 20.0
            }
        }
    elif model_id == 'mmWave':
        return {
            'required': ['los_condition'],
            'optional': ['material_attenuation'],
            'defaults': {
                'material_attenuation': 0.0
            }
        }
    return None
from utils.export import generate_pdf_report

@csrf_exempt
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def run_simulation(request):
    """
    Run a network simulation based on provided parameters.
    """
    # Si le corps de la requête est une chaîne, le convertir en JSON
    if isinstance(request.data, str):
        data = json.loads(request.data)
    else:
        data = request.data
        
    print("Données reçues:", data)  # Débogage
    
    # Créer simulation sans utilisateur
    simulation = Simulation.objects.create(
        name=data.get('name', 'New Simulation'),
        description=data.get('description', ''),
        #user=None  # Pas d'utilisateur associé
    )
    try:
        #data = json.loads(request.body)
        
        # Create simulation parameters
        location = Point(
            float(data['longitude']),
            float(data['latitude']),
            srid=4326
        )
        
        params = SimulationParameter.objects.create(
            simulation=simulation,
            technology=data['technology'],
            propagation_model=data['propagation_model'],
            frequency=float(data['frequency']),
            antenna_height=float(data['antenna_height']),
            antenna_power=float(data['antenna_power']),
            terrain_type=data['terrain_type'],
            location=location,
            radius=float(data['radius']),
            population_density=float(data.get('population_density', 0))
        )
        
        # Run the simulation
        result = run_propagation_model(params)
        
        return Response({
            'simulation_id': simulation.id,
            'result': result
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def run_propagation_model(params):
    """
    Run the selected propagation model and generate coverage data.
    """
    # Choose the appropriate propagation model
    if params.propagation_model == '3GPP_TR_38901':
        # Récupérer les paramètres 5G spécifiques
        network_5g_params = getattr(params, 'network5gparams', {}) or {}
        
        # Créer une instance du modèle 5G approprié
        scenario = network_5g_params.get('scenario', 'UMa')
        los_condition = network_5g_params.get('los_condition', 'LOS')
        
        # Fonction de calcul de l'affaiblissement de parcours
        def path_loss_func(distance, **kwargs):
            # Convertir la distance en mètres (car le modèle attend des mètres)
            distance_m = distance * 1000
            
            # Calculer la perte de propagation avec les paramètres 5G
            return FiveGPropagationModel.path_loss(
                frequency=params.frequency * 1e6,  # Convertir en Hz
                distance=distance_m,
                scenario=scenario,
                los_condition=los_condition,
                h_bs=float(network_5g_params.get('h_bs', 10.0)),
                h_ut=float(network_5g_params.get('h_ut', 1.5)),
                h=float(network_5g_params.get('h', 20.0)),
                w=float(network_5g_params.get('w', 20.0))
            )
            
    elif params.propagation_model == 'OKUMURA_HATA':
        path_loss_func = okumura_hata_path_loss
    else:  # COST_231
        path_loss_func = cost_231_path_loss
    
    # Generate grid points within the radius
    center_lon, center_lat = params.location.x, params.location.y
    grid_size = 0.1  # km
    radius_km = params.radius
    
    # Create a grid of points
    x = np.linspace(center_lon - radius_km/111, center_lon + radius_km/111, int(2*radius_km/grid_size))
    y = np.linspace(center_lat - radius_km/111, center_lat + radius_km/111, int(2*radius_km/grid_size))
    
    # Calculate signal strength at each point
    signal_strength = {}
    coverage_polygons = []
    
    for lon in x:
        for lat in y:
            # Calculate distance from center in km
            distance = ((lon - center_lon)**2 + (lat - center_lat)**2)**0.5 * 111  # Approximate km
            
            if distance <= radius_km:
                try:
                    # Calculate path loss
                    if params.propagation_model == '3GPP_TR_38901':
                        path_loss = path_loss_func(distance)
                    else:
                        path_loss = path_loss_func(
                            params.frequency,
                            params.antenna_height,
                            1.5,  # Default mobile height
                            distance,
                            params.terrain_type
                        )
                    
                    # Calculate received signal strength
                    signal = params.antenna_power - path_loss
                    
                    # Store signal strength
                    key = f"{lon:.6f},{lat:.6f}"
                    signal_strength[key] = signal
                    
                    # If signal is above threshold, add to coverage
                    if signal >= -100:  # -100 dBm threshold
                        # Create a small square around this point
                        square = Polygon.from_bbox((
                            lon - grid_size/222,
                            lat - grid_size/222,
                            lon + grid_size/222,
                            lat + grid_size/222
                        ))
                        coverage_polygons.append(square)
                        
                except ValueError:
                    # Skip points that are out of the valid range for the model
                    pass
    
    # Create coverage multipolygon
    if coverage_polygons:
        coverage_area = MultiPolygon(coverage_polygons)
    else:
        # Create an empty multipolygon if no coverage
        coverage_area = MultiPolygon([])
    
    # Calculate coverage percentage
    if params.radius > 0:
        total_area = np.pi * (params.radius ** 2)
        covered_area = sum(p.area * (111**2) for p in coverage_polygons)
        coverage_percentage = (covered_area / total_area) * 100
    else:
        coverage_percentage = 0
    
    # Calculate population covered
    if params.population_density:
        population_covered = int(covered_area * params.population_density)
    else:
        population_covered = None
    
    # Save the results
    result = SimulationResult.objects.create(
        simulation=params.simulation,
        coverage_area=coverage_area,
        coverage_percentage=coverage_percentage,
        population_covered=population_covered,
        signal_strength_data=signal_strength
    )
    
    return {
        'coverage_percentage': coverage_percentage,
        'population_covered': population_covered,
        'signal_strength_data': signal_strength
    }

@csrf_exempt
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def export_simulation_pdf(request,simulation_id):
    """
    Export simulation results as PDF.
    """
    simulation = get_object_or_404(Simulation, id=simulation_id, user=None)
    
    # Generate PDF
    pdf_file = generate_pdf_report(simulation)
    
    # Create response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="simulation_{simulation_id}.pdf"'
    
    return response