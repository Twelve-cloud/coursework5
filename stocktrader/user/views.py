from user.permissions import (
    IsUserOwner, IsUserOwnerOrAdmin, IsNotAuthenticatedOrAdmin,
    IsNotUserOwner, IsNotUserBanned
)
from user.services import (
    set_blocking, cancel_all_users_orders, follow_user
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from user.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework import status
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_map = {
        'create': (
            IsNotAuthenticatedOrAdmin,
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
        'block': (
            IsAuthenticated,
            IsAdminUser,
            IsNotUserOwner,
        ),
        'follow': (
            IsAuthenticated,
            IsNotUserOwner,
            IsNotUserBanned,
        ),
        'followers': (
            IsAuthenticated,
            IsNotUserBanned,
        ),
        'follows': (
            IsAuthenticated,
            IsNotUserBanned,
        ),
        'remove_followers': (
            IsAuthenticated,
            IsUserOwner,
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['patch'])
    def block(self, request, pk=None):
        user = self.get_object()
        is_blocked = request.data.get('is_blocked', False)
        set_blocking(user, is_blocked)
        cancel_all_users_orders(user)
        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def follow(self, request, pk=None):
        target_user = self.get_object()
        follow_user(request.user, target_user)
        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        serializer = self.serializer_class(user.followers.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def follows(self, request, pk=None):
        user = self.get_object()
        serializer = self.serializer_class(user.follows.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
