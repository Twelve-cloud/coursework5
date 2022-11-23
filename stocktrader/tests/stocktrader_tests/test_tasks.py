from stocktrader.tasks import (
    send_notification_about_order, send_email_to_verify_account,
    clear_database_from_waste_accounts, update_users_balance
)
from shares.models import Account
from user.models import User
import pytest


pytestmark = pytest.mark.django_db


class TestStocktraderTasks:
    def test_send_notification_about_order(self, mocker):
        send_notif = mocker.MagicMock()
        mocker.patch('stocktrader.tasks.send_mail', send_notif)
        send_notification_about_order(..., ..., ..., ...)
        send_notif.assert_called_once()

    def test_send_email_to_verify_account(self, mocker):
        send_email = mocker.MagicMock()
        mocker.patch('stocktrader.tasks.send_mail', send_email)
        send_email_to_verify_account(..., ...)
        send_email.assert_called_once()

    def test_clear_database_from_waste_accounts(self, user):
        assert len(User.objects.all()) == 1
        clear_database_from_waste_accounts()
        assert len(User.objects.all()) == 0

    def test_update_users_balance(self, account):
        assert account.balance == 5000
        update_users_balance()
        assert Account.objects.get(pk=account.pk).balance == 10000
