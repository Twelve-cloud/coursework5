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
        assert order.__str__() == f'{order.pk}. {order.broker.name}[{order.get_type_display()}]'

    def test_user_get_absolute_url(self, order):
        assert order.get_absolute_url() == f'/orders/{order.pk}/'


class TestAccountModel:
    def test_user_str(self, account):
        assert account.__str__() == f'{account.pk}. {account.user.username}[{account.balance}]'

    def test_user_get_absolute_url(self, account):
        assert account.get_absolute_url() == f'/accounts/{account.pk}/'


class TestStockModel:
    def test_user_str(self, stock):
        assert stock.__str__() == f'{stock.pk}. {stock.company}[{stock.amount}]'

    def test_user_get_absolute_url(self, stock):
        assert stock.get_absolute_url() == f'/stocks/{stock.pk}/'

    def test_update_current_price(self, stock, mocker):
        get_stock_latest_price = mocker.MagicMock(return_value=5000)
        mocker.patch('shares.models.get_stock_latest_price', get_stock_latest_price)
        update_price.send(Stock, pk=stock.pk)
        get_stock_latest_price.assert_called_once()
        update_price.send(Stock)
        assert get_stock_latest_price.call_count == 2


class TestAccountHistoryModel:
    def test_user_str(self, account_history):
        assert account_history.__str__() == f'history of account #{account_history.account.pk}'

    def test_user_get_absolute_url(self, account_history):
        assert account_history.get_absolute_url() == f'/history/{account_history.pk}/'
