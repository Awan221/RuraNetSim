from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models

class Simulation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SimulationParameter(models.Model):
    TECHNOLOGY_CHOICES = [
        ('2G', '2G - GSM'),
        ('3G', '3G - UMTS'),
        ('4G', '4G - LTE'),
        ('5G', '5G - NR (New Radio)'),
    ]
    
    PROPAGATION_MODEL_CHOICES = [
        ('OKUMURA_HATA', 'Okumura-Hata'),
        ('COST_231', 'COST-231'),
        ('3GPP_TR_38901', '3GPP TR 38.901 (5G)'),
    ]
    
    # Scénarios 5G
    SCENARIO_CHOICES = [
        ('UMa', 'Urban Macro (UMa)'),
        ('UMi', 'Urban Micro (UMi)'),
        ('RMa', 'Rural Macro (RMa)'),
        ('InH-Office', 'Indoor Hotspot - Office'),
        ('InH-ShoppingMall', 'Indoor Hotspot - Shopping Mall'),
    ]
    
    # Conditions de visibilité
    LOS_CONDITION_CHOICES = [
        ('LOS', 'Line of Sight (LOS)'),
        ('NLOS', 'Non-Line of Sight (NLOS)'),
    ]
    
    TERRAIN_TYPE_CHOICES = [
        ('URBAN', 'Urban'),
        ('SUBURBAN', 'Suburban'),
        ('RURAL', 'Rural'),
        ('OPEN', 'Open'),
    ]
    
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='parameters')
    technology = models.CharField(max_length=10, choices=TECHNOLOGY_CHOICES)
    propagation_model = models.CharField(max_length=20, choices=PROPAGATION_MODEL_CHOICES)
    frequency = models.FloatField(help_text="Frequency in MHz")
    
    # Paramètres spécifiques à la 5G
    scenario = models.CharField(max_length=20, choices=SCENARIO_CHOICES, blank=True, null=True, 
                              help_text="5G deployment scenario")
    los_condition = models.CharField(max_length=10, choices=LOS_CONDITION_CHOICES, blank=True, null=True,
                                   help_text="Line of sight condition")
    h_bs = models.FloatField(blank=True, null=True, help_text="Hauteur de la station de base (m)")
    h_ut = models.FloatField(blank=True, null=True, help_text="Hauteur de l'utilisateur (m)")
    h = models.FloatField(blank=True, null=True, help_text="Hauteur moyenne des bâtiments (m)")
    w = models.FloatField(blank=True, null=True, help_text="Largeur moyenne des routes (m)")
    bandwidth = models.FloatField(help_text="Bandwidth in MHz", default=5.0)
    antenna_height = models.FloatField(help_text="Antenna height in meters")
    antenna_power = models.FloatField(help_text="Antenna power in dBm")
    terrain_type = models.CharField(max_length=10, choices=TERRAIN_TYPE_CHOICES)
    location = gis_models.PointField(help_text="Antenna location (longitude, latitude)")
    radius = models.FloatField(help_text="Simulation radius in kilometers")
    population_density = models.FloatField(help_text="Population density per square kilometer", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parameters for {self.simulation.name}"

class SimulationResult(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='results')
    coverage_area = gis_models.MultiPolygonField(help_text="Coverage area polygons")
    coverage_percentage = models.FloatField(help_text="Percentage of area covered")
    population_covered = models.IntegerField(help_text="Estimated population covered", blank=True, null=True)
    signal_strength_data = models.JSONField(help_text="Signal strength data for visualization")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Results for {self.simulation.name}"