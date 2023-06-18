from stocktrader.tasks import send_email_to_verify_account
from jauth.services import generate_token
from user.models import User


def set_blocking(user: User, is_blocked: bool) -> None:
    """
    set_blocking: set is_blocked parameter to is_blocked field of user.
    if is_blocked == False, user's not blocked, otherwise user's blocked.
    """
    user.is_blocked = is_blocked
    user.save()


def follow_user(user: User, target_user: User) -> None:
    """
    follow_user: add user to followers of target_user or remove it.
    Behaviour depends on whether user already in a followers list of
    target_user or not. If not it adds to followers if yes it removes from it.
    """
    if user in target_user.followers.all():
        target_user.followers.remove(user)
    else:
        target_user.followers.add(user)


def remove_from_followers(user: User, followers: list):
    """
    remove_from_followers: remove follower/followers from user's follower list.
    """
    followers = User.objects.filter(pk__in=followers)
    for follower in followers:
        if follower in user.followers.all():
            user.followers.remove(follower)


def send_verification_link(link: str, email: str) -> None:
    """
    send_verification_link: send verification link to user email.
    """
    verify_url = link + '?token=' + generate_token(type='access', user_id=email)
    send_email_to_verify_account.delay(email, verify_url)
