from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from user.models import User


@shared_task
def send_notification_about_order(action: str, amount: int, email: str, company: str) -> None:
    """
    send_notification_about_order: sends notification when order has been
    finished with django send_main function.
    """
    send_mail(
        'Order was completed',
        f'Order was completed to {action} {amount} stocks of {company}.',
        settings.EMAIL_HOST_USER,
        [email]
    )


@shared_task
def send_email_to_verify_account(email: str, verify_url: str) -> None:
    """
    send_email_to_verify_account: sends notification to verify account with
    django send_main function.
    """
    send_mail(
        'Account Verification',
        f'Click the link to verify account {verify_url}',
        settings.EMAIL_HOST_USER,
        [email]
    )


@shared_task
def clear_database_from_waste_accounts() -> None:
    """
    clear_database_from_waste_accounts: clears database from accounts
    which haven't been activated every 3 hours.
    """
    User.objects.filter(is_active=False).delete()


@shared_task
def update_users_balance() -> None:
    """
    update_users_balance: updates user's balance each month.
    """
    for user in User.objects.all():
        for account in user.accounts.all():
            account.balance += 5000
            account.save()
            account.history.create(
                account=account,
                balance=account.balance,
                balance_with_shares=account.balance_with_shares
            )
