from shares.permissions import IsOrderCreatorOrAdmin, IsBalanceOwnerOrAdmin
import pytest


pytestmark = pytest.mark.django_db


class TestSharesPermissions:
    def test_is_order_creator_or_admin(self, _request, order, admin, anon):
        _request.user = order.user
        assert IsOrderCreatorOrAdmin.has_object_permission(..., _request, ..., order) is True
        _request.user = admin
        assert IsOrderCreatorOrAdmin.has_object_permission(..., _request, ..., order) is True
        _request.user = anon
        assert IsOrderCreatorOrAdmin.has_object_permission(..., _request, ..., order) is False

    def test_is_balance_owner_or_admin(self, _request, account, admin, anon):
        _request.user = account.user
        assert IsBalanceOwnerOrAdmin.has_object_permission(..., _request, ..., account) is True
        _request.user = admin
        assert IsBalanceOwnerOrAdmin.has_object_permission(..., _request, ..., account) is True
        _request.user = anon
        assert IsBalanceOwnerOrAdmin.has_object_permission(..., _request, ..., account) is False
