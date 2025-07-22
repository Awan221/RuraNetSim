from rest_framework import viewsets, permissions, status, throttling
from rest_framework.decorators import action, throttle_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.cache import cache

from .models import UserProfile
from simulation.models import Simulation, SimulationParameter
from .serializers import UserSerializer, SimulationSerializer, SimulationParameterSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint qui permet d'afficher ou de modifier les utilisateurs.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    throttle_scope = 'user'

    def get_queryset(self):
        """
        Filtre les utilisateurs pour ne montrer que l'utilisateur connecté,
        sauf pour les administrateurs qui voient tout.
        """
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60 * 15))  # Cache de 15 minutes
    @method_decorator(vary_on_cookie)
    def me(self, request):
        """
        Endpoint pour récupérer les informations de l'utilisateur connecté.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Surcharge de la création avec validation des entrées.
        """
        # Validation des données d'entrée
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validation de base
        if not all([username, email, password]):
            return Response(
                {'error': 'Tous les champs sont obligatoires'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validation de l'email
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {'error': 'Adresse email invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Ce nom d\'utilisateur est déjà pris'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Cette adresse email est déjà utilisée'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si tout est valide, création de l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        serializer = self.get_serializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class SimulationViewSet(viewsets.ModelViewSet):
    """
    API endpoint qui permet de gérer les simulations.
    """
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Configuration du throttling
    throttle_classes = [throttling.AnonRateThrottle]

    def get_queryset(self):
        """
        Filtre les simulations pour ne montrer que celles de l'utilisateur connecté,
        sauf pour les administrateurs qui voient tout.
        """
        user = self.request.user
        if user.is_staff:
            return Simulation.objects.all().order_by('-created_at')
        return Simulation.objects.filter(user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """
        Associe l'utilisateur connecté à la nouvelle simulation.
        """
        serializer.save(user=self.request.user)
    
    throttle_classes = [throttling.AnonRateThrottle]
    
    def list(self, request, *args, **kwargs):
        """
        Liste les simulations avec un cache pour améliorer les performances.
        """
        cache_key = f'simulations_user_{request.user.id}'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)  # Cache de 5 minutes
        return response
    
    def create(self, request, *args, **kwargs):
        """
        Crée une nouvelle simulation avec validation des entrées.
        """
        # Validation des données d'entrée
        required_fields = ['name', 'parameters']
        if not all(field in request.data for field in required_fields):
            return Response(
                {'error': f'Les champs suivants sont obligatoires: {", ".join(required_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validation des paramètres de simulation
        try:
            parameters = request.data.get('parameters', {})
            if not isinstance(parameters, dict):
                raise ValidationError("Les paramètres doivent être un objet JSON")
            
            # Exemple de validation spécifique des paramètres
            if 'frequency' in parameters and not (100 <= parameters['frequency'] <= 6000):
                raise ValidationError("La fréquence doit être comprise entre 100 et 6000 MHz")
            
        except (ValueError, TypeError, ValidationError) as e:
            return Response(
                {'error': f'Paramètres de simulation invalides: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], throttle_classes=[throttling.UserRateThrottle])
    def duplicate(self, request, pk=None):
        """
        Duplique une simulation existante.
        """
        try:
            simulation = self.get_object()
            simulation.pk = None
            simulation.name = f"{simulation.name} (Copie)"
            simulation.save()
            
            # Dupliquer les paramètres
            for param in simulation.parameters.all():
                param.pk = None
                param.simulation = simulation
                param.save()
                
            serializer = self.get_serializer(simulation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la duplication: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class FiveGSimulationViewSet(viewsets.ViewSet):
    """
    API endpoint pour gérer spécifiquement les simulations 5G.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.AnonRateThrottle]
    
    @action(detail=False, methods=['post'])
    def run_5g_simulation(self, request):
        """
        Exécute une simulation 5G avec les paramètres fournis.
        """
        try:
            # Valider les données d'entrée
            serializer = SimulationParameterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Créer une nouvelle simulation
            simulation = Simulation.objects.create(
                user=request.user,
                name=request.data.get('name', 'Nouvelle simulation 5G'),
                description=request.data.get('description', '')
            )
            
            # Créer les paramètres de simulation
            params_data = request.data.copy()
            params_data['simulation'] = simulation.id
            
            # Ajouter les paramètres 5G spécifiques
            for field in ['scenario', 'los_condition', 'h_bs', 'h_ut', 'h', 'w']:
                if field in request.data:
                    params_data[field] = request.data[field]
            
            param_serializer = SimulationParameterSerializer(data=params_data)
            if not param_serializer.is_valid():
                simulation.delete()  # Supprimer la simulation en cas d'erreur
                return Response(param_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            param_serializer.save()
            
            # Ici, vous pourriez appeler votre logique de simulation 5G
            # Par exemple :
            # from simulation.propagation_models_5g import FiveGPropagationModel
            # model = FiveGPropagationModel(...)
            # result = model.calculate_path_loss(...)
            
            # Pour l'instant, retourner une réponse de succès
            return Response({
                'status': 'success',
                'simulation_id': simulation.id,
                'message': 'Simulation 5G démarrée avec succès',
                'parameters': param_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la simulation 5G: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def get_5g_scenarios(self, request):
        """
        Récupère la liste des scénarios 5G disponibles.
        """
        return Response({
            'scenarios': dict(SimulationParameter.SCENARIO_CHOICES),
            'los_conditions': dict(SimulationParameter.LOS_CONDITION_CHOICES)
        })