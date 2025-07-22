import json
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)

class CsrfExemptMiddleware(MiddlewareMixin):
    """Middleware pour désactiver la vérification CSRF sur les endpoints d'API spécifiques."""
    def process_request(self, request):
        if request.path.startswith('/api/auth/'):
            setattr(request, '_dont_enforce_csrf_checks', True)


class ExceptionHandlingMiddleware(MiddlewareMixin):
    """Middleware global pour la gestion des exceptions et la journalisation."""
    
    def process_exception(self, request, exception):
        """Gère les exceptions non capturées et renvoie une réponse JSON appropriée."""
        # Journalisation de l'erreur
        logger.error(
            f"Erreur non gérée: {str(exception)}\n"
            f"Méthode: {request.method}\n"
            f"URL: {request.build_absolute_uri()}\n"
            f"Corps: {request.body.decode('utf-8', 'ignore')}",
            exc_info=True
        )

        # Définition du code de statut et du message d'erreur par défaut
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_detail = "Une erreur serveur inattendue s'est produite."
        
        # Gestion des exceptions spécifiques
        if isinstance(exception, APIException):
            status_code = exception.status_code
            error_detail = str(exception.detail)
        elif hasattr(exception, 'status_code'):
            status_code = exception.status_code
            error_detail = str(exception)
        
        # Préparation de la réponse d'erreur
        response_data = {
            'status': 'error',
            'code': status_code,
            'message': error_detail,
            'path': request.path,
        }
        
        # Ajout de détails supplémentaires en mode debug
        if settings.DEBUG:
            response_data['exception'] = exception.__class__.__name__
            response_data['traceback'] = str(exception)
        
        return JsonResponse(response_data, status=status_code, safe=False)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware pour journaliser les requêtes et réponses de l'API."""
    
    def process_request(self, request):
        """Enregistre les détails de la requête entrante."""
        if request.path.startswith('/api/'):
            logger.info(
                f"Requête reçue: {request.method} {request.path}\n"
                f"En-têtes: {dict(request.headers)}\n"
                f"Paramètres: {dict(request.GET)}\n"
                f"Données: {request.body.decode('utf-8', 'ignore')}"
            )
    
    def process_response(self, request, response):
        """Enregistre les détails de la réponse sortante."""
        if request.path.startswith('/api/'):
            logger.info(
                f"Réponse envoyée: {request.method} {request.path} - {response.status_code}\n"
                f"Contenu: {response.content.decode('utf-8', 'ignore')}"
            )
        return response