from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

# Script para la creacion de un superusuario:
class Command(BaseCommand):
    help = 'Crea un superusuario por defecto'
    
    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin',
                email='admin@example.com'
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado: username = admin, password = admin, email = admin@example.com'))
        else:
            self.stdout.write(self.style.WARNING('Superusuario ya existe'))