"""
Django settings for voting_project project.
"""
import os
from pathlib import Path
import dj_database_url
from decouple import config # Necesitas instalar: pip install python-decouple

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
# Carga la clave secreta desde el entorno (más seguro)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-7o*ei85ff72s6$9cv55(a2(bm+-v43rc7ue##)7vq8(+igw=8=')

# SECURITY WARNING: don't run with debug turned on in production!
# Carga DEBUG desde el entorno (False en producción, True en desarrollo)
DEBUG = config('DEBUG', default=True, cast=bool)

# Permite hosts de desarrollo y producción (como Render)
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # --- Mi Aplicacion ---
    'voting', 
]

MIDDLEWARE = [
    # AÑADIDO: Para servir archivos estáticos (CSS/JS) en producción
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'voting_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'voting_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        # Busca la variable DATABASE_URL (usada por Render)
        default=config('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3'),
        conn_max_age=600 # Mantiene las conexiones abiertas
    )
}


# Password validation
# ... (Sin cambios respecto a tu código original)
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


# Internationalization
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# Configuración para que WhiteNoise y Django manejen los estáticos en producción
STATIC_URL = 'static/'

# Directorio donde Django recolectará todos los archivos estáticos para el despliegue
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Directorios adicionales donde buscar estáticos (si tienes una carpeta 'static' global en la raíz)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirección
LOGIN_REDIRECT_URL = '/voting/guia/'
LOGIN_URL = '/login/'


# ... al final de settings.py
# --- Configuración de Enlaces Externos ---
GITHUB_REPO_URL = "https://github.com/LilianaVo/Proyecto" # REEMPLAZA ESTO