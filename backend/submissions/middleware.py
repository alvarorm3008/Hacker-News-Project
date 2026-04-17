from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin

class DefaultUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        User = get_user_model()
        default_user, created = User.objects.get_or_create(username='default_user', defaults={'password': 'default_password'})
        request.user = default_user