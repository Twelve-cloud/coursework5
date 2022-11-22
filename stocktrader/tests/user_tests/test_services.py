from user.services import (
    set_blocking, follow_user, remove_from_followers, send_verification_link
)
from stocktrader.tasks import send_email_to_verify_account
import pytest


pytestmark = pytest.mark.django_db


class TestUserServices:
    def test_set_blocking(self, user):
        assert user.is_blocked is False
        set_blocking(user=user, is_blocked=True)
        assert user.is_blocked is True

    def test_follow_user(self, user, admin):
        assert user not in admin.followers.all()
        follow_user(user, admin)
        assert user in admin.followers.all()
        follow_user(user, admin)
        assert user not in admin.followers.all()

    def test_remove_from_followers(self, user, admin):
        admin.followers.add(user)
        assert user in admin.followers.all()
        remove_from_followers(admin, [user.pk])
        assert user not in admin.followers.all()

    def test_send_verification_link(self, mocker):
        gen_token = mocker.MagicMock(return_value='')
        send_email = mocker.MagicMock()

        mocker.patch('user.services.generate_token', gen_token)
        mocker.patch.object(send_email_to_verify_account, 'delay', send_email)
        send_verification_link('', '')

        gen_token.assert_called_once()
        send_email.assert_called_once()
