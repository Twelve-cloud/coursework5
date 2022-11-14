from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            not isinstance(request.user, AnonymousUser) and
            obj == request.user
        )


class IsNotAuthentificatedOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            not IsAuthenticated.has_permission(self, request, view) or
            IsAdminUser.has_permission(self, request, view)
        )
