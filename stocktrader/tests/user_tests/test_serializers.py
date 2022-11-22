from user.serializers import BasicUserSerializer, FullUserSerializer
from django.contrib.auth.hashers import check_password
from django.db.utils import IntegrityError
import pytest


pytestmark = pytest.mark.django_db


class TestBasicUserSerializer:
    def test_create(self, user_json):
        serializer = BasicUserSerializer()
        user = serializer.create(user_json)
        assert user.email == user_json.get('email')
        assert user.is_staff == user_json.get('is_staff')
        assert user.is_active is False

        with pytest.raises(IntegrityError):
            serializer.create(user_json)

    def test_update(self, user, update_json):
        serializer = BasicUserSerializer()
        user_password = update_json.get('password')
        user = serializer.update(user, update_json)
        assert user.first_name == update_json.get('first_name')
        assert user.last_name == update_json.get('last_name')
        assert check_password(user_password, user.password) is True


class TestFullUserSerializer:
    def test_create(self, user_json):
        serializer = FullUserSerializer()
        user = serializer.create(user_json)
        assert user.email == user_json.get('email')
        assert user.is_staff == user_json.get('is_staff')
        assert user.is_active is False

        with pytest.raises(IntegrityError):
            serializer.create(user_json)

    def test_update(self, user, update_json):
        serializer = FullUserSerializer()
        user_password = update_json.get('password')
        user = serializer.update(user, update_json)
        assert user.first_name == update_json.get('first_name')
        assert user.last_name == update_json.get('last_name')
        assert check_password(user_password, user.password) is True
