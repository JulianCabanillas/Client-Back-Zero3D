#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Metodo ejecutor de DJango, metodo main:

def main():
    """Run administrative tasks."""

    # Aqui definimos las settings que deben recoger segun el entorno:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appBackClient.settings.production')
    try:
        from django.core.management import execute_from_command_line # type: ignore
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
