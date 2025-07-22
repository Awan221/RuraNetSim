from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .authentification import CsrfExemptSessionAuthentication
from rest_framework.authentication import TokenAuthentication
from .models import UserProfile
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication, TokenAuthentication])
def register(request):
    try:
        # Récupérer les données
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        organization = request.data.get('organization', '')
        
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Ce nom d\'utilisateur est déjà pris.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Cet email est déjà utilisé.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Créer le profil utilisateur
        UserProfile.objects.create(
            user=user,
            organization=organization
        )
        
        return Response({'detail': 'Inscription réussie!'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication, TokenAuthentication])
def login(request):
    try:
        # Vérifier que la requête est en JSON
        if not request.data or not isinstance(request.data, dict):
            return Response(
                {'detail': 'Les données doivent être au format JSON'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Vérifier que les champs requis sont présents
        if not username or not password:
            return Response(
                {'detail': 'Le nom d\'utilisateur et le mot de passe sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authentifier l'utilisateur en passant la requête
        user = authenticate(request=request, username=username, password=password)
        
        if user is not None and user.is_active:
            # Créer ou récupérer un token
            token, created = Token.objects.get_or_create(user=user)
            
            # Préparer la réponse
            response_data = {
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }
            
            # Ajouter des informations supplémentaires si disponibles
            # Vérifier si le modèle UserProfile existe et est accessible
            if hasattr(user, 'userprofile'):
                try:
                    response_data['user']['organization'] = user.userprofile.organization
                except Exception as e:
                    # Enregistrer l'erreur mais continuer sans les informations du profil
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f'Erreur lors de la récupération du profil utilisateur: {str(e)}')
                
            return Response(response_data)
        else:
            # Ne pas révéler si c'est le nom d'utilisateur ou le mot de passe qui est incorrect
            return Response(
                {'detail': 'Nom d\'utilisateur ou mot de passe incorrect'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        # Journaliser l'erreur pour le débogage
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Erreur lors de la connexion: {str(e)}', exc_info=True)
        
        # Retourner une réponse d'erreur générique
        return Response(
            {'detail': 'Une erreur est survenue lors de la tentative de connexion'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )