from user.models import User


def set_blocking(user: User, is_blocked: bool) -> None:
    """
    set_blocking: set is_blocked parameter to is_blocked field of user.
    if is_blocked == False, user's not blocked, otherwise user's blocked.
    """
    user.is_blocked = is_blocked
    user.save()


def cancel_all_users_orders(user: User) -> None:
    """
    cancel_all_users_orders: set status "Done" to all users orders which have
    status "Process"
    """
    for order in user.orders.all():
        if order.status == 'pc':
            order.status = 'dn'


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
