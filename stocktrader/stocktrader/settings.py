"""
Django settings for stocktrader project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""


from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()

# -------------------------- MAIN SETTINGS ------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

ROOT_URLCONF = 'stocktrader.urls'

DEFAULT_CHARSET = 'utf8'

# -------------------------- INSTALLED APPS -----------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shares.apps.SharesConfig',
    'jauth.apps.JauthConfig',
    'user.apps.UserConfig',
    'pyex.apps.PyexConfig',
    'rest_framework',
    'django_filters',
]

# -------------------------- MIDDLEWARES --------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'jauth.middlewares.JWTMiddleware'
]

# --------------------------- TEMPLATES ---------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# ---------------------------- DATABASES --------------------------------------

DATABASES = {
    'default': {
        'ENGINE': os.getenv('POSTGRES_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('POSTGRES_DB', 'StockTrader'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', '0')),
    }
}

# ------------------------- LANGUAGE SETTINGS ---------------------------------

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L18N = True

TIME_ZONE = 'UTC'

USE_TZ = True

# -------------------------- OTHER SETTINGS -----------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
            ),
    },
]

WSGI_APPLICATION = 'stocktrader.wsgi.application'

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

# --------------------------- JWT SETTINGS ------------------------------------
JWT_TOKEN = {
    'ACCESS_TOKEN_LIFETIME_MINUTES': 15,
    'REFRESH_TOKEN_LIFETIME_DAYS': 30,
    'ALGORITHMS': ['HS256'],
    'SECURE': True,
    'HTTP_ONLY': True,
}

# -------------------------- DRF SETTINGS -------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

# ----------------------------- PYEX SETTINGS ---------------------------------
PYEX_KEY = os.getenv('PYEX_KEY')

# -------------------------- RABBITMQ SETTINGS --------------------------------
RABBITMQ = {
    'PROTOCOL': os.getenv('RABBITMQ_PROTOCOL'),
    'HOST': os.getenv('RABBITMQ_HOST'),
    'PORT': os.getenv('RABBITMQ_PORT'),
    'USER': os.getenv('RABBITMQ_USER'),
    'PASSWORD': os.getenv('RABBITMQ_PASSWORD'),
}

# ------------------------- CELERY SETTINGS -----------------------------------
CELERY_BROKER_URL = (
    f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:"
    f"{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
