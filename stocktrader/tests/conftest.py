from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from shares.models import Account
from model_bakery import baker
from user.models import User
import pytest


@pytest.fixture()
def api_factory():
    return APIRequestFactory()


@pytest.fixture()
def _request(mocker):
    return mocker.MagicMock()


@pytest.fixture()
def anon():
    return AnonymousUser()


@pytest.fixture()
def user():
    return baker.make(User, is_staff=False)


@pytest.fixture()
def admin():
    return baker.make(User, is_staff=True)


@pytest.fixture()
def account(user):
    return baker.make(Account, user=user, balance=5000)


@pytest.fixture()
def blocked_user():
    return baker.make(User, is_staff=False, is_blocked=True)
