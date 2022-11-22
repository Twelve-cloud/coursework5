from user.views import UserViewSet
from model_bakery import baker
from user.models import User
import pytest


@pytest.fixture()
def user_json():
    user = baker.prepare(User, is_staff=False)
    return {
        'email': user.email,
        'username': user.username,
        'password': user.password,
        'is_staff': user.is_staff
    }


@pytest.fixture()
def update_json():
    return {
        'password': '12341234',
        'first_name': 'James',
        'last_name': 'Bond'
    }


@pytest.fixture()
def block_json():
    return {
        'is_blocked': 'True'
    }


@pytest.fixture()
def userperm(mocker):
    mock = mocker.MagicMock(return_value=True)
    mocker.patch.object(UserViewSet, 'check_permissions', mock)
    mocker.patch.object(UserViewSet, 'check_object_permissions', mock)
