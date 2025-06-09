from corsheaders.defaults import default_headers, default_methods 
from pathlib import Path
from datetime import timedelta
import environ


# Archivo base para las configuraciones de DJango:
# Iniciamos la gestion de las variable de entorno y 
# capturamos el path de la raiz:
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

# Definicion de las aplicaciones instaladas:
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',

]

# En este apartado, procesaremos las peticiones y respuesta HTTP:
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Esta es la definicion de como buscar y procesar las plantillas HTML:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Validadores de las contraseñas:
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# JWT para el uso de la cokies:
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.ClientJWTAuthentication",
    ],
}

#Tiempos que queremos mantener la validacion de dichas cokies y otros 
# aspectos como el id cliente:
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),   # cortito
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "USER_ID_FIELD": "client_id",
    "USER_ID_CLAIM": "client_id",
}

# Aqui indicamos las configuraciones de rutas y servidores:
ROOT_URLCONF = 'appBackClient.urls'

WSGI_APPLICATION = 'appBackClient.wsgi.application'

ASGI_APPLICATION = 'appBackClient.asgi.application'


# Aqui definimos configuraciones de idioma y de pais, esto nos 
# ayuda con las conversiones:
LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Aqui tenemos las rutas a archivos estaticos: 
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media/'


# Aqui definimos las configuraciones de CORS:
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = ["http://localhost:3000","http://localhost"]    

CORS_ALLOW_HEADERS = list(default_headers) + ["content-type",]


# Esta verificacion es para permitir peticiones POST si 
# la peticion viene desde otro dominio o puerto:
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000","http://localhost"]


# Aqui tenenos las opciones de las cookies:
SESSION_COOKIE_SAMESITE = 'None'

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# Definimos las rutas a el Slicer:
SLIC3R_PATH = env('SLIC3R_PATH', default='/usr/bin/slic3r')

SLICER_PROFILES_DIR = BASE_DIR / 'slicer_profiles'


