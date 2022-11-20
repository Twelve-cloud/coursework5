from celery import shared_task
from user.models import User


@shared_task
def send_notification_about_order() -> None:
    pass


@shared_task
def send_email_to_verify_account(email: str, verify_url: str) -> None:
    pass


@shared_task
def clear_database_from_waste_accounts() -> None:
    User.objects.filter(is_verified=False).delete()
