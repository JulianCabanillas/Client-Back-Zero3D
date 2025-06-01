#!/bin/sh

# Llama al script para realizar espera hasta la preparacion de la BD:
./wait-for.sh db:5432
echo "Base de datos disponible"


echo "Ejecutando migraciones..."

# Ejecutamos migraciones en Django
# Creamos migraciones por si hay cambios en las bd
python manage.py makemigrations 
# Aplicamos las migraciones pertienentes:
python manage.py migrate --noinput
# Creacion del superUser para Django:
python manage.py createadmin

echo "Añadiendo cliente de ejemplo si no existe..."

# Añadimos un usuario de ejemplo la primera vez que se levanta la Suite:
python << END
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appBackClient.settings")  # Ajusta esto según tu proyecto
django.setup()

from api.models import Client
from django.contrib.auth.hashers import make_password
from django.utils import timezone

if not Client.objects.filter(username="invitado").exists():
    Client.objects.create(
        username="invitado",
        email="invitado@invitado.com",
        password=make_password("invitado"),
        date_register=timezone.now(),
    )
    print("Cliente de ejemplo creado.")
else:
    print("Cliente de ejemplo ya existe.")
END

# Aqui lanzamos para levantar el servidor que dara pie a Django:
echo "Levantando servidor..."
