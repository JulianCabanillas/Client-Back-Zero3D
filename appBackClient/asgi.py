"""
ASGI config for appBackClient project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application # type: ignore


# Aqui definimos las settings que deben recoger segun el entorno:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appBackClient.settings.production')

application = get_asgi_application()
