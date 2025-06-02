#!/bin/sh

# Llama al script para realizar espera hasta la preparacion de la BD:
./wait-for.sh db:5432 "Todo listo!!"
echo "Base de datos disponible"


echo "Ejecutando migraciones..."

# Ejecutamos migraciones en Django

# Aplicamos las migraciones pertienentes:
python manage.py migrate --noinput

python manage.py collectstatic --noinput --settings=appBackClient.settings.staging
# Creacion del superUser para Django:
python manage.py createadmin

echo "Añadiendo cliente de ejemplo si no existe..."

# Añadimos un usuario de ejemplo la primera vez que se levanta la Suite:
python << END
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appBackClient.settings.staging")  # Ajusta esto según tu proyecto
django.setup()

from api.models import Client
from django.contrib.auth.hashers import make_password
from django.utils import timezone

if not Client.objects.filter(username="invitado").exists():
    Client.objects.create(
        username="invitado",
        email="invitado@invitado.com",
        password="invitado",
        date_register=timezone.now(),
    )
    print("Cliente de ejemplo creado.")
else:
    print("Cliente de ejemplo ya existe.")
END



# Aqui lanzamos para levantar el servidor que dara pie a Django:
echo "Levantando servidor..."
exec gunicorn appBackClient.wsgi:application \
     --bind 0.0.0.0:8000 