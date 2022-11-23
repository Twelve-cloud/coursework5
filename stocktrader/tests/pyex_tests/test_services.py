from shares.apps import update_price
from shares.models import Stock
import pytest


pytestmark = pytest.mark.django_db


class TestBrokerModel:
    def test_user_str(self, broker):
        assert broker.__str__() == f'{broker.pk}. {broker.name}'

    def test_user_get_absolute_url(self, broker):
        assert broker.get_absolute_url() == f'/brokers/{broker.pk}/'


class TestOrderModel:
    def test_user_str(self, order):
