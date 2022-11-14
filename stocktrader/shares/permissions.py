from rest_framework import permissions


class IsOrderCreator(permissions.BasePermissions):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsBalanceOwner(permissions.BasePermissions):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
