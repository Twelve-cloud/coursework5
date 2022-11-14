from user.permissions import (
    IsUserOwner, IsUserOwnerOrAdmin, IsNotAuthentificatedOrAdmin,
    IsNotUserOwner, IsNotUserBanned
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from user.serializers import UserSerializer
from rest_framework import viewsets
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_map = {
        'create': (
            IsNotAuthentificatedOrAdmin,
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
            IsUserOwnerOrAdmin,
        ),
        'ban': (
            IsAuthenticated,
            IsAdminUser,
            IsNotUserBanned,
        ),
        'follow': (
            IsAuthenticated,
            IsNotUserOwner,
            IsNotUserBanned,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()
