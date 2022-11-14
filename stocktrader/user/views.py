from user.permissions import (
    IsUserOwner, IsUserOwnerOrAdmin, IsNotAuthenticatedOrAdmin,
    IsNotUserOwner, IsNotUserBanned
)
from user.services import (
    set_blocking, cancel_all_users_orders, follow_user,
    remove_from_followers
)
from user.serializers import BasicUserSerializer, FullUserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'date_joined']
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

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullUserSerializer
        return BasicUserSerializer

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
        serializer = self.get_serializer_class()(user.followers.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def follows(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer_class()(user.follows.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def remove_followers(self, request, pk=None):
        user = self.get_object()
        followers_to_remove = request.data.get('followers', [])
        remove_from_followers(user, followers_to_remove)
        return Response('Success', status=status.HTTP_200_OK)
