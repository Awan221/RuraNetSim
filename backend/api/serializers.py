from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from simulation.models import Simulation, SimulationParameter, SimulationResult

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'organization', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id']

class SimulationParameterSerializer(serializers.ModelSerializer):
    # Surcharge pour gérer les champs optionnels 5G
    scenario = serializers.ChoiceField(
        choices=SimulationParameter.SCENARIO_CHOICES, 
        required=False, 
        allow_null=True,
        help_text="Scénario de déploiement 5G (UMa, UMi, RMa, etc.)"
    )
    los_condition = serializers.ChoiceField(
        choices=SimulationParameter.LOS_CONDITION_CHOICES,
        required=False,
        allow_null=True,
        help_text="Condition de visibilité (LOS/NLOS)"
    )
    h_bs = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Hauteur de la station de base (m)"
    )
    h_ut = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Hauteur de l'utilisateur (m)"
    )
    h = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Hauteur moyenne des bâtiments (m)"
    )
    w = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Largeur moyenne des routes (m)"
    )
    
    class Meta:
        model = SimulationParameter
        fields = [
            'id', 'simulation', 'technology', 'propagation_model', 'frequency',
            'bandwidth', 'antenna_height', 'antenna_power', 'terrain_type',
            'location', 'radius', 'population_density', 'created_at', 'updated_at',
            # Champs spécifiques 5G
            'scenario', 'los_condition', 'h_bs', 'h_ut', 'h', 'w'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate(self, data):
        """
        Validation personnalisée pour s'assurer que les champs 5G sont cohérents
        """
        technology = data.get('technology')
        propagation_model = data.get('propagation_model')
        
        # Si c'est une simulation 5G avec le modèle 3GPP
        if technology == '5G' and propagation_model == '3GPP_TR_38901':
            required_fields = ['scenario', 'los_condition', 'h_bs', 'h_ut']
            missing_fields = [field for field in required_fields if field not in data or data[field] is None]
            
            if missing_fields:
                raise serializers.ValidationError({
                    'error': f"Les champs suivants sont requis pour une simulation 5G avec le modèle 3GPP: {', '.join(missing_fields)}"
                })
                
            # Validation supplémentaire pour les scénarios qui nécessitent h et w
            scenario = data.get('scenario')
            if scenario in ['UMa', 'RMa'] and (data.get('h') is None or data.get('w') is None):
                missing = []
                if data.get('h') is None:
                    missing.append('h (hauteur moyenne des bâtiments)')
                if data.get('w') is None:
                    missing.append('w (largeur moyenne des routes)')
                raise serializers.ValidationError({
                    'error': f"Pour le scénario {scenario}, les champs suivants sont requis: {', '.join(missing)}"
                })
        
        return data

class SimulationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationResult
        fields = '__all__'

class SimulationSerializer(serializers.ModelSerializer):
    parameters = SimulationParameterSerializer(many=True, read_only=True)
    results = SimulationResultSerializer(many=True, read_only=True)
    
    class Meta:
        model = Simulation
        fields = ['id', 'name', 'description', 'user', 'created_at', 'updated_at', 'parameters', 'results']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        simulation = Simulation.objects.create(user=user, **validated_data)
        return simulation