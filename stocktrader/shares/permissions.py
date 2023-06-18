from rest_framework.permissions import IsAdminUser
from rest_framework import permissions


class IsOrderCreatorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAdminUser.has_permission(self, request, view) or \
            request.user == obj.user


class IsBalanceOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAdminUser.has_permission(self, request, view) or \
            request.user == obj.user
