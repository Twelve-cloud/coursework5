from shares.serializers import (
    BrokerSerializer, OrderSerializer, AccountSerializer
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from shares.permissions import IsOrderCreator, IsBalanceOwner
from shares.models import Broker, Order, Account
from rest_framework import viewsets, mixins


class BrokerViewSet(viewsets.ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
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
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_map = {
        'create': (
            IsAuthenticated,
        ),
        'list': (
            IsAuthenticated,
            IsOrderCreator,
            IsAdminUser,
        ),
        'retrieve': (
            IsAuthenticated,
            IsOrderCreator,
            IsAdminUser,
        ),
        'destroy': (
            IsAuthenticated,
            IsOrderCreator,
            IsAdminUser,
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()


class AccountViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_map = {
        'create': (
            IsAuthenticated,
        ),
        'list': (
            IsAuthenticated,
            IsBalanceOwner,
            IsAdminUser,
        ),
        'retrieve': (
            IsAuthenticated,
            IsBalanceOwner,
            IsAdminUser,
        ),
        'destroy': (
            IsAuthenticated,
            IsBalanceOwner,
            IsAdminUser,
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()
