from user.permissions import (
    IsUserOwner, IsUserOwnerOrAdmin, IsNotAuthenticatedOrAdmin,
    IsNotUserOwner, IsNotUserBanned
)
import pytest


pytestmark = pytest.mark.django_db


class TestUserPermissions:
    def test_is_user_owner(self, _request, user, admin, anon):
        _request.user = user
        assert IsUserOwner.has_object_permission(..., _request, ..., user) is True
        assert IsUserOwner.has_object_permission(..., _request, ..., admin) is False
        assert IsUserOwner.has_object_permission(..., _request, ..., anon) is False

    def test_is_user_owner_or_admin(self, _request, user, admin, anon):
        _request.user = user
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., user) is True
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., admin) is False
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., anon) is False
        _request.user = admin
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., user) is True
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., admin) is True
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., anon) is True

    def test_is_not_authenticated_or_admin(self, _request, user, admin, anon):
        _request.user = user
        assert IsNotAuthenticatedOrAdmin.has_permission(..., _request, ...) is False
        _request.user = admin
        assert IsNotAuthenticatedOrAdmin.has_permission(..., _request, ...) is True
        _request.user = anon
        assert IsNotAuthenticatedOrAdmin.has_permission(..., _request, ...) is True

    def test_is_not_user_owner(self, _request, user, admin, anon):
        _request.user = user
        assert IsNotUserOwner.has_object_permission(..., _request, ..., user) is False
        assert IsNotUserOwner.has_object_permission(..., _request, ..., admin) is True
        assert IsNotUserOwner.has_object_permission(..., _request, ..., anon) is True

    def test_is_not_user_banned(self, _request, user, blocked_user):
        assert IsNotUserBanned.has_object_permission(..., ..., ..., user) is True
        assert IsNotUserBanned.has_object_permission(..., ..., ..., blocked_user) is False
