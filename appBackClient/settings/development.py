from .base import *

environ.Env.read_env( BASE_DIR / '.env.development')

DEBUG = True

SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-key')

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='zero3d_dev'),
        'USER': env('DB_USER', default='admin'),
        'PASSWORD': env('DB_PASSWORD', default='admin'),
        'HOST': env('DB_HOST', default='db'),  
        'PORT': env('DB_PORT', default='5432'),
    }
}

STATICFILES_DIRS = [ BASE_DIR / 'static' ]