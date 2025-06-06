from .base import *

# Utilizamos el archivo correspondiente para las variante del entorno:
environ.Env.read_env( BASE_DIR / '.env.production')

# Aqui desactivamos la bandera para el debug (dev)
#  y activamos la bandera de STAGING:
DEBUG = False

# Definicion de la llave:
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-key')

# Puertos permitidos para la conexion:
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["zero3d.shop,www.zero3d.shop,backend,127.0.0.1,localhost"])

# Defincion de la base de datos de staging:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME', default='zero3d_prod_db'),
        'USER': env('DATABASE_USER', default='admin'),
        'PASSWORD': env('DATABASE_PASSWORD', default='admin'),
        'HOST': env('DATABASE_HOST', default='db'),  
        'PORT': env('DATABASE_PORT', default='5432'),
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