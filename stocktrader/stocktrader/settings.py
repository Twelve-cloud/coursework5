"""
Django settings for stocktrader project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""


from celery.schedules import crontab
from pathlib import Path
import dns.resolver
import os

# -------------------------- MAIN SETTINGS ------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('CONFIG_DEBUG')

ALLOWED_HOSTS = os.getenv('CONFIG_ALLOWED_HOSTS', 'localhost').split(',')

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
    'corsheaders',
]

# -------------------------- MIDDLEWARES --------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
srv_records = dns.resolver.query('service-database-headless.deploy.svc.cluster.local', 'SRV')
master_host = srv_records[0].target

DATABASES = {
    'master': {
        'ENGINE': os.getenv('POSTGRES_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('POSTGRES_DB', 'StockTrader'),
        'HOST': master_host,
        'PORT': os.getenv('POSTGRES_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'CONN_MAX_AGE': int(os.getenv('CONFIG_CONN_MAX_AGE', '0')),
    },
    'default': {
        'ENGINE': os.getenv('POSTGRES_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('POSTGRES_DB', 'StockTrader'),
        'HOST': os.getenv('SERVICE_DATABASE_PUBLIC_SERVICE_HOST'),
        'PORT': os.getenv('SERVICE_DATABASE_PUBLIC_SERVICE_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'CONN_MAX_AGE': int(os.getenv('CONFIG_CONN_MAX_AGE', '0')),
    }
}

DATABASE_ROUTERS = ['stocktrader.dbrouters.DbRouter']
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
    'ACCESS_TOKEN_LIFETIME_MINUTES': 15 * 4 * 24,
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
    'HOST': os.getenv('SERVICE_RABBITMQ_SERVICE_HOST'),
    'PORT': os.getenv('SERVICE_RABBITMQ_SERVICE_PORT'),
    'USER': os.getenv('RABBITMQ_USER'),
    'PASSWORD': os.getenv('RABBITMQ_PASSWORD'),
}

# ------------------------- CELERY SETTINGS -----------------------------------
CELERY_BROKER_URL = (
    f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:"
    f"{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_BEAT_SCHEDULE = {
    'add-every-midnight':
    {
        'task': 'stocktrader.tasks.clear_database_from_waste_accounts',
        'schedule': crontab(minute=0, hour='*/3')
    },
    'update-every-month':
    {
        'task': 'stocktrader.tasks.update_users_balance',
        'schedule': crontab(0, 0, day_of_month='1')
    }
}

CELERY_ENABLE_UTC = True

CELERY_TIMEZONE = 'UTC'

# ----------------------- DJANGO EMAIL SETTINGS -------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# --------------------- CORS SETTINGS -----------------------------------------
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:5000',
    'http://127.0.0.1:5000'
]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:5000',
    'http://127.0.0.1:5000'
]

CORS_ALLOW_CREDENTIALS = True
