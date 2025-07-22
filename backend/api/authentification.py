from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication sans vérification CSRF pour les API REST
    """
    def enforce_csrf(self, request):
        return  # Ne rien faire, désactive la vérification CSRF