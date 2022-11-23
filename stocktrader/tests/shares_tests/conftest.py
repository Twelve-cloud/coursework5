from shares.models import Broker, Order, Stock, AccountHistory
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
