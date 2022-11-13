from django.db import models


class Broker(models.Model):
    class Types(models.TextChoices):
        SPREAD = 'sp', 'Sread'
        SWAP = 'sw', 'Swap'
        __empty__ = 'Choose type'

    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Name'
    )

    type = models.CharField(
        max_length=2,
        choices=Types.choices,
        verbose_name='Type'
    )

    rate = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Rate'
    )


class Order(models.Model):
    class Types(models.TextChoices):
        LIMIT = 'lt', 'Limit'
        MARKET = 'mt', 'Market'
        __empty__ = 'Choose type'

    class Status(models.TextChoices):
        PROCCESS = 'pc', 'Process'
        DONE = 'dn', 'Done'
        __empty__ = 'Choose status'

    type = models.CharField(
        max_length=2,
        choices=Types.choices,
        verbose_name='Type'
    )

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        verbose_name='Status'
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Price'
    )


class Deal(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
    )

    broker = models.ForeignKey(
        'Broker',
        on_delete=models.CASCADE,
        verbose_name='Broker',
        related_name='deals'
    )

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='deals'
    )

    order = models.OneToOneField(
        'Order',
        on_delete=models.PROTECT,
        verbose_name='Order',
        related_name='deal'
    )


class Account(models.Model):
    class Currency(models.TextChoices):
        USD = 'usd', 'Dollar'
        EUR = 'eur', 'Euro'
        RUB = 'rub', 'Ruble'
        __empty__ = 'Choose currency'

    balance = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Balance'
    )

    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        verbose_name='Currency'
    )

    broker = models.ForeignKey(
        'Broker',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Broker',
        related_name='accounts'
    )

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='accounts'
    )
