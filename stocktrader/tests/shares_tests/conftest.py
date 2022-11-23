from shares.models import Broker, Order, Stock, AccountHistory
from shares.views import StockViewSet
from model_bakery import baker
import pytest


@pytest.fixture()
def _request(mocker):
    return mocker.MagicMock()


@pytest.fixture()
def broker():
    return baker.make(Broker)


@pytest.fixture()
def order(broker):
    return baker.make(Order, broker=broker, type='buy')


@pytest.fixture()
def stock():
    return baker.make(Stock, company='Apple', amount=100)


@pytest.fixture()
def account_history(account):
    return baker.make(AccountHistory, account=account)


@pytest.fixture()
def stockperm(mocker):
    mock = mocker.MagicMock(return_value=True)
    mocker.patch.object(StockViewSet, 'check_permissions', mock)
    mocker.patch.object(StockViewSet, 'check_object_permissions', mock)
