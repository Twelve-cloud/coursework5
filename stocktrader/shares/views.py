from shares.serializers import (
    BrokerSerializer, OrderSerializer, AccountSerializer,
    StockSerializer, AccountHistorySerializer
)
from shares.permissions import IsOrderCreatorOrAdmin, IsBalanceOwnerOrAdmin
from shares.models import Broker, Order, Account, Stock, AccountHistory
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import AnonymousUser
from pyex.services import get_stock_latest_price
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from shares.apps import update_price
from rest_framework import status
from decimal import Decimal


class BrokerViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = BrokerSerializer
    filterset_fields = ['name', 'rate']
    ordering_fields = ['name', 'rate']
    search_fields = ['name', 'rate']
    queryset = Broker.objects.all()
    permission_map = {
        'create': (
            IsAuthenticated,
            IsAdminUser
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'update': (
            IsAuthenticated,
            IsAdminUser
        ),
        'partial_update': (
            IsAuthenticated,
            IsAdminUser
        ),
        'destroy': (
            IsAuthenticated,
            IsAdminUser
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    ordering_fields = [
        'type',
        'company',
        'created_at',
        'amount'
    ]
    filterset_fields = [
        'type',
        'company',
        'amount'
    ]
    search_fields = [
        'type',
        'company',
        'amount'
    ]
    permission_map = {
        'create': (
            IsAuthenticated,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'destroy': (
            IsAuthenticated,
            IsOrderCreatorOrAdmin,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
        if not isinstance(user, AnonymousUser) and user.is_staff is True:
            return Order.objects.all()
        else:
            return user.orders.all()

    def create(self, request, *args, **kwargs):
        broker_id, user_id = request.data.get('broker')
        user_id =  request.data.get('user')
        type = request.data.get('type')
        company = request.data.get('company')
        amount = int(request.data['amount'])
        latest_price = get_stock_latest_price(symbol=company)
        account = Account.objects.get(broker=broker_id, user=user_id)
        broker = Broker.objects.get(pk=broker_id)

        if type == 'buy':
            commission = Decimal(latest_price * amount) * broker.rate
            stocks_price = Decimal(latest_price * amount) + commission

            if account.balance < stocks_price:
                return Response(
                    data='Error: Not enough money',
                    status=status.HTTP_400_BAD_REQUEST
                )

            if Stock.objects.filter(company=company, account=account).exists():
                stocks = Stock.objects.get(company=company, account=account)
                stocks.amount += amount
                stocks.save()
            else:
                Stock.objects.create(
                    company=company,
                    amount=amount,
                    current_price=latest_price,
                    account=account
                )

            stocks = Stock.objects.get(company=company, account=account)
            account.balance -= stocks_price
            whole_balance = account.balance + stocks.current_price * amount
            account.balance_with_shares = whole_balance
            account.save()

            AccountViewSet.update(
                self,
                request,
                balance=account.balance,
                balance_with_shares=account.balance_with_shares
            )
        else:
            if Stock.objects.filter(company=company, account=account).exists():
                stocks = Stock.objects.get(company=company, account=account)

                if stocks.amount < amount:
                    return Response(
                        data='Error: Stocks to sell must be less than you own',
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    stocks.amount -= amount
                    stocks.save()

                    commission = Decimal(latest_price * amount) * broker.rate
                    stocks_price = Decimal(latest_price * amount) - commission

                    account.balance += stocks_price
                    whole_balance = account.balance + stocks.current_price * amount
                    account.balance_with_shares = whole_balance
                    account.save()

                    if not stocks.amount:
                        stocks.delete()

                    AccountViewSet.update(
                        self,
                        request,
                        balance=account.balance,
                        balance_with_shares=account.balance_with_shares
                    )
            else:
                return Response(
                    data='Error: You do not have stocks of this company',
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    ordering_fields = [
        'balance',
        'balance_with_shares',
        'updated_at'
    ]
    filterset_fields = [
        'balance',
        'balance_with_shares'
    ]
    search_fields = [
        'balance',
        'balance_with_shares'
    ]
    permission_map = {
        'create': (
            IsAuthenticated,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'update': (
            IsAuthenticated,
            IsAdminUser
        ),
        'partial_update': (
            IsAuthenticated,
            IsAdminUser
        ),
        'destroy': (
            IsAuthenticated,
            IsBalanceOwnerOrAdmin,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
        if not isinstance(user, AnonymousUser) and user.is_staff is True:
            return Account.objects.all()
        else:
            return user.accounts.all()

    def create(self, request, *args, **kwargs):
        if len(request.user.accounts.all()) == 3:
            return Response(
                data='Error: Number of accounts must be less than 3',
                status=status.HTTP_400_BAD_REQUEST
            )

        broker_id = request.data.get('broker')
        user_id = request.data.get('user')

        if Account.objects.filter(broker=broker_id, user=user_id).exists():
            return Response(
                data='Error: Number of accounts in one broker must be single',
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().create(request, *args, **kwargs)

        account = Account.objects.get(broker=broker_id, user=user_id)
        balance = request.data.get('balance')
        balance_with_shares = request.data.get('balance_with_shares')

        AccountHistory.objects.create(
            account=account,
            balance=balance,
            balance_with_shares=balance_with_shares
        )

        return response

    def update(self, request, *args, **kwargs):
        account = Account.objects.get(
            pk=kwargs.get('pk'),
            None
        )

        balance = request.data.get(
            'balance',
            account.balance
        )

        balance_with_shares = request.data.get(
            'balance_with_shares',
            account.balance_with_shares
        )

        AccountHistory.objects.create(
            account=account,
            balance=balance,
            balance_with_shares=balance_with_shares
        )

        return super().update(request, *args, **kwargs)


class StockViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    ordering_fields = [
        'company',
        'amount',
        'purchase_price'
    ]
    filterset_fields = [
        'company',
        'amount',
        'purchase_price'
    ]
    search_fields = [
        'company',
        'amount',
        'purchase_price'
    ]
    permission_map = {
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
        accounts = user.accounts.all()
        if accounts:
            shares = accounts[0].shares.all()
            for account in accounts[1:]:
                shares |= account.shares.all()
            return shares

    def list(self, request, *args, **kwargs):
        update_price.send(Stock)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        update_price.send(Stock, pk=kwargs['pk'])
        return super().retrieve(request, *args, **kwargs)


class AccountHistoryViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = AccountHistory.objects.all()
    serializer_class = AccountHistorySerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    ordering_fields = [
        'balance',
        'balance_with_shares',
        'date'
    ]
    filterset_fields = [
        'balance',
        'balance_with_shares'
    ]
    search_fields = [
        'balance',
        'balance_with_shares'
    ]
    permission_map = {
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
        accounts = user.accounts.all()
        if accounts:
            history = accounts[0].history.all()
            for account in accounts[1:]:
                history |= account.history.all()
            return history
