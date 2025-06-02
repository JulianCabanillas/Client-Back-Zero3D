from .base import *

# Utilizamos el archivo correspondiente para las variante del entorno:
environ.Env.read_env( BASE_DIR / '.env.example')

# Aqui activamos la bandera para el debug (dev):
DEBUG = True

# Definicion de la llave:
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-key')

# Puertos permitidos para la conexion:
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Defincion de la base de datos de desarrollo:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='zero3d_dev_db'),
        'USER': env('DB_USER', default='admin'),
        'PASSWORD': env('DB_PASSWORD', default='admin'),
        'HOST': env('DB_HOST', default='db'),  
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Definimos la ruta de los estaticos:
STATICFILES_DIRS = [ BASE_DIR / 'static' ]