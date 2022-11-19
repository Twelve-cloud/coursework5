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
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import status


class BrokerViewSet(viewsets.ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'type']
    search_fields = ['name', 'type']
    ordering_fields = ['name', 'type', 'rate']
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'company', 'amount']
    search_fields = ['type', 'company', 'amount']
    ordering_fields = ['type', 'company', 'created_at', 'amount']
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


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['balance', 'balance_with_shares']
    search_fields = ['balance', 'balance_with_shares']
    ordering_fields = ['balance', 'balance_with_shares', 'updated_at']
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

        broker, user = request.data['broker'], request.data['user']

        if Account.objects.filter(broker=broker, user=user).exists():
            return Response(
                data='Error: Number of accounts in one broker must be single',
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().create(request, *args, **kwargs)

        AccountHistory.objects.create(
            account=Account.objects.get(broker=broker, user=user),
            balance=request.data['balance'],
            balance_with_shares=request.data['balance_with_shares']
        )

        return response

    def update(self, request, *args, **kwargs):
        account = Account.objects.get(pk=kwargs.get('pk'))

        AccountHistory.objects.create(
            account=account,
            balance=request.data.get('balance', account.balance),
            balance_with_shares=request.data.get(
                'balance_with_shares',
                account.balance_with_shares
            )
        )

        return super().update(request, *args, **kwargs)


class StockViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'amount', 'purchase_price']
    search_fields = ['company', 'amount', 'purchase_price']
    ordering_fields = ['company', 'amount', 'purchase_price']
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
            for account in accounts:
                shares |= account.shares.all()
            return shares


class AccountHistoryViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = AccountHistory.objects.all()
    serializer_class = AccountHistorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['balance', 'balance_with_shares']
    search_fields = ['balance', 'balance_with_shares']
    ordering_fields = ['balance', 'balance_with_shares', 'date']
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
            for account in accounts:
                history |= account.history.all()
            return history
