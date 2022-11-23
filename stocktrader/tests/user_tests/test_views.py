from user.serializers import BasicUserSerializer, FullUserSerializer
from rest_framework.permissions import IsAuthenticated
from user.views import UserViewSet
from rest_framework import status
from user.models import User
import pytest


pytestmark = pytest.mark.django_db

create_view = UserViewSet.as_view({'post': 'create'})
block_view = UserViewSet.as_view({'patch': 'block'})
follow_view = UserViewSet.as_view({'patch': 'follow'})
followers_view = UserViewSet.as_view({'get': 'followers'})
follows_view = UserViewSet.as_view({'get': 'follows'})
remove_followers_view = UserViewSet.as_view({'patch': 'remove_followers'})


class TestUserViewSet:
    def test_get_serializer_class(self, _request, user, admin):
        user_viewset = UserViewSet()
        user_viewset.request = _request
        _request.user = user
        assert user_viewset.get_serializer_class() is BasicUserSerializer
        _request.user = admin
        assert user_viewset.get_serializer_class() is FullUserSerializer

    def test_get_permissions(self):
        user_viewset = UserViewSet()
        user_viewset.action = 'list'
        assert isinstance(user_viewset.get_permissions()[0], IsAuthenticated) is True

    def test_get_object(self, _request, user, userperm):
        user_viewset = UserViewSet()
        user_viewset.request = _request
        user_viewset.queryset = User.objects.all()
        user_viewset.kwargs = {'pk': user.pk}
        assert user_viewset.get_object() == user

    def test_create(self, api_factory, user_json, anon, admin, mocker, userperm):
        request = api_factory.post('', user_json, format='json')
        request.build_absolute_uri = mocker.MagicMock()
        send_verification = mocker.MagicMock()
        mocker.patch('user.views.send_verification_link', send_verification)
        request.user = anon
        response = create_view(request)
        request.build_absolute_uri.assert_called_once()
        send_verification.assert_called_once()
        assert response.status_code == status.HTTP_201_CREATED

    def test_block(self, api_factory, user, block_json, userperm):
        request = api_factory.patch('', block_json, format='json')
        response = block_view(request, pk=user.pk)
        user = User.objects.get(pk=user.pk)
        assert user.is_blocked is True
        assert response.status_code == status.HTTP_200_OK

    def test_follow(self, api_factory, user, admin, userperm):
        request = api_factory.patch('', '', format='json')
        user.is_active = True
        request.user = user
        response = follow_view(request, pk=admin.pk)
        assert (user in admin.followers.all()) is True
        assert response.status_code == status.HTTP_200_OK

    def test_followers(self, api_factory, user, userperm):
        request = api_factory.get('', {}, format='json')
        user.is_active = True
        request.user = user
        response = followers_view(request, pk=user.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_follows(self, api_factory, user, userperm):
        request = api_factory.get('', {}, format='json')
        user.is_active = True
        request.user = user
        response = follows_view(request, pk=user.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_remove_followers(self, api_factory, user, userperm):
        request = api_factory.patch('', {}, format='json')
        user.is_active = True
        request.user = user
        response = remove_followers_view(request, pk=user.pk)
        assert response.status_code == status.HTTP_200_OK
