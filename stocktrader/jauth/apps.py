from django.apps import AppConfig


class JauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jauth'
    label = 'jauth'
    verbose_name = 'JWT Authentification'
