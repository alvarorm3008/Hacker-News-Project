from django.core.management.base import BaseCommand
from accounts.models import Profile
import uuid  # Para generar claves únicas

class Command(BaseCommand):
    help = 'Asigna una api_key a los perfiles de usuario existentes'

    def handle(self, *args, **kwargs):
        users = Profile.objects.all()
        for user in users:
            if user.api_key == "default-api-key":
                # Genera una api_key única
                user.api_key = str(uuid.uuid4())  # O usa el valor por defecto que desees
                user.save()
                self.stdout.write(self.style.SUCCESS(f'api_key asignada a {user.user}'))
