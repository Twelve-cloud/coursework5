from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return not isinstance(user, AnonymousUser) and obj == user


class IsNotAuthentificated(permissions.BasePermission):
    def has_permissions(self, request, view):
        return not IsAuthenticated(self, request, view)
