from django.dispatch import Signal
from django.apps import AppConfig


class SharesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shares'
    label = 'shares'
    verbose_name = 'Shares'


update_price = Signal(providing_args=['pk'])
