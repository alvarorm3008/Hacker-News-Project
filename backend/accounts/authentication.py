from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Profile

class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')  # Busca la API Key en los encabezados
        if not api_key:
            return None
        
        try:
            profile = Profile.objects.get(api_key=api_key)  # Busca el perfil por la API key
            user = profile.user  # Obtiene el usuario relacionado
        except Profile.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key')

        return (user, None)
