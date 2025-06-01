from .base import *

# Utilizamos el archivo correspondiente para las variante del entorno:
environ.Env.read_env( BASE_DIR / '.env.staging')

# Aqui desactivamos la bandera para el debug (dev)
#  y activamos la bandera de STAGING:
DEBUG = False
STAGING = True

# Definicion de la llave:
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-key')

# Puertos permitidos para la conexion:
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["staging.zero3d.com"])

# Defincion de la base de datos de staging:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='zero3d_stage_db'),
        'USER': env('DB_USER', default='admin'),
        'PASSWORD': env('DB_PASSWORD', default='admin'),
        'HOST': env('DB_HOST', default='db'),  
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Nueva ruta para los archivos estaticos servidos por DJango:
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Para evitar ataques de XXS reflejado:
SECURE_BROWSER_XSS_FILTER = True

# Para evitar que el navegador ejecute contenido equivocado:
SECURE_CONTENT_TYPE_NOSNIFF = True

# Protegemos cotra ataque tipo clickjacking:
X_FRAME_OPTIONS = 'DENY'

# Evita ataques de dowgrade o strip SSL:
SECURE_HSTS_SECONDS = 31536000

# Para aplicar las politicas de seguridad a todos los submodulos:
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Incluir dominio en las listas internas de los navegadores:
SECURE_HSTS_PRELOAD = True