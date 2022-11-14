from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not isinstance(request.user, AnonymousUser) and \
            obj == request.user


class IsUserOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAdminUser.has_permission(self, request, view) or \
            IsUserOwner.has_object_permission(self, request, view, obj)


class IsNotAuthentificatedOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return not IsAuthenticated.has_permission(self, request, view) or \
            IsAdminUser.has_permission(self, request, view)


class IsNotUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not IsUserOwner.has_object_permission(self, request, view, obj)


class IsNotUserBanned(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.is_blocked
