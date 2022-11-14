from shares.serializers import (
    BrokerSerializer, OrderSerializer, DealSerializer, AccountSerializer
)
from shares.models import Broker, Order, Deal, Account
from rest_framework import viewsets


class BrokerViewSet(viewsets.ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    permission_map = {
        'create': (
            IsNotAuthentificated,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'update': (
            IsAuthenticated,
            IsUserOwner,
        ),
        'partial_update': (
            IsAuthenticated,
            IsUserOwner,
        ),
        'destroy': (
            IsAuthenticated,
            IsUserOwner,
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_map = {
        'create': (
            IsNotAuthentificated,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'update': (
            IsAuthenticated,
            IsUserOwner,
        ),
        'partial_update': (
            IsAuthenticated,
            IsUserOwner,
        ),
        'destroy': (
            IsAuthenticated,
            IsUserOwner,
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_map = {
        'create': (
            IsNotAuthentificated,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'update': (
            IsAuthenticated,
            IsUserOwner,
        ),
        'partial_update': (
            IsAuthenticated,
            IsUserOwner,
        ),
        'destroy': (
            IsAuthenticated,
            IsUserOwner,
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_map = {
        'create': (
            IsNotAuthentificated,
        ),
        'list': (
            IsBalanceOwner,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'update': (
            IsAuthenticated,
            IsUserOwner,
        ),
        'partial_update': (
            IsAuthenticated,
            IsUserOwner,
        ),
        'destroy': (
            IsAuthenticated,
            IsUserOwner,
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()
