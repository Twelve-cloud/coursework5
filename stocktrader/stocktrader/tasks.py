from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from user.models import User


@shared_task
def send_notification_about_order(action: str, amount: int, email: str) -> None:
    send_mail(
        'Order was completed',
        (
            f'Order was completed to {action} {amount} stocks.'
        ),
        settings.EMAIL_HOST_USER,
        [email]
    )


@shared_task
def send_email_to_verify_account(email: str, verify_url: str) -> None:
    send_mail(
        'Account Verification',
        (
            f'Click the link below to verify account.<br>'
            f'<b><a href="{verify_url}">{verify_url}</a></b>'
        ),
        settings.EMAIL_HOST_USER,
        [email]
    )


@shared_task
def clear_database_from_waste_accounts() -> None:
    User.objects.filter(is_verified=False).delete()


@shared_task
def update_users_balance() -> None:
    for user in User.objects.all():
        for account in user.accounts.all():
            account.balance += 5000
            account.history.create(
                account=account,
                balance=account.balance,
                balance_with_shares=account.balance_with_shares
            )