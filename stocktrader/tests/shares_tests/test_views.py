from shares.views import (
    BrokerViewSet, OrderViewSet, AccountViewSet,
    StockViewSet, AccountHistoryViewSet
)
from rest_framework.permissions import IsAuthenticated
from shares.apps import update_price
from shares.models import Account, Stock, Order
from rest_framework import status
from model_bakery import baker
import pytest


pytestmark = pytest.mark.django_db

create_order_view = OrderViewSet.as_view({'post': 'create'})
create_account_view = AccountViewSet.as_view({'post': 'create'})
update_account_view = AccountViewSet.as_view({'put': 'update'})
list_account_view = AccountViewSet.as_view({'get': 'list'})
retrieve_account_view = AccountViewSet.as_view({'get': 'retrieve'})
list_stock_view = StockViewSet.as_view({'get': 'list'})
retrieve_stock_view = StockViewSet.as_view({'get': 'retrieve'})


class TestBrokerViewSet:
    def test_get_permissions(self):
        broker_viewset = BrokerViewSet()
        broker_viewset.action = 'list'
        assert isinstance(broker_viewset.get_permissions()[0], IsAuthenticated) is True


class TestOrderViewSet:
    def test_get_permissions(self):
        order_viewset = OrderViewSet()
        order_viewset.action = 'list'
        assert isinstance(order_viewset.get_permissions()[0], IsAuthenticated) is True

    def test_get_queryset(self, _request, admin, user):
        _request.user = user
        order_viewset = OrderViewSet()
        order_viewset.request = _request
        result = order_viewset.get_queryset()
        assert len(result) == len(user.orders.all())
        _request.user = admin
        order_viewset.request = _request
        result = order_viewset.get_queryset()
        assert len(result) == len(Order.objects.all())


class TestAccountViewSet:
    def test_get_permissions(self):
        account_viewset = AccountViewSet()
        account_viewset.action = 'list'
        assert isinstance(account_viewset.get_permissions()[0], IsAuthenticated) is True

    def test_get_queryset(self, _request, admin, user):
        _request.user = user
        account_viewset = AccountViewSet()
        account_viewset.request = _request
        result = account_viewset.get_queryset()
        assert len(result) == len(user.accounts.all())
        _request.user = admin
        account_viewset.request = _request
        result = account_viewset.get_queryset()
        assert len(result) == len(Account.objects.all())


class TestStockViewSet:
    def test_get_permissions(self):
        stock_viewset = StockViewSet()
        stock_viewset.action = 'list'
        assert isinstance(stock_viewset.get_permissions()[0], IsAuthenticated) is True

    def test_get_queryset(self, _request, user, account, stock):
        account2 = baker.make(Account, user=user, balance=5000)
        account.shares.add(stock)
        account2.shares.add(stock)
        _request.user = user
        account_history_viewset = StockViewSet()
        account_history_viewset.request = _request
        result = account_history_viewset.get_queryset()
        assert result[0] == stock

    def test_list(self, api_factory, mocker, stockperm, stock):
        request = api_factory.get('', '', format='json')
        send = mocker.MagicMock()
        mocker.patch.object(update_price, 'send', send)
        get_queryset = mocker.MagicMock(return_value=Stock.objects.all())
        mocker.patch.object(StockViewSet, 'get_queryset', get_queryset)
        response = list_stock_view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve(self, api_factory, mocker, stockperm, stock):
        request = api_factory.get('', '', format='json')
        send = mocker.MagicMock()
        mocker.patch.object(update_price, 'send', send)
        get_queryset = mocker.MagicMock(return_value=Stock.objects.all())
        mocker.patch.object(StockViewSet, 'get_queryset', get_queryset)
        response = retrieve_stock_view(request, pk=stock.pk)
        assert response.status_code == status.HTTP_200_OK


class TestAcconutHistoryViewSet:
    def test_get_permissions(self):
        account_history_viewset = AccountHistoryViewSet()
        account_history_viewset.action = 'list'
        assert isinstance(account_history_viewset.get_permissions()[0], IsAuthenticated) is True

    def test_get_queryset(self, _request, user, account_history):
        user.accounts.add(account_history.account)
        account = baker.make(Account, user=user, balance=5000)
        user.accounts.add(account)
        _request.user = user
        account_history_viewset = AccountHistoryViewSet()
        account_history_viewset.request = _request
        result = account_history_viewset.get_queryset()
        assert result[0] == account_history
