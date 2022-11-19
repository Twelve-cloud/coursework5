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

    description = models.TextField(
        verbose_name='Description',
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

    def __str__(self):
        return f'{self.pk}. {self.name}'

    def get_absolute_url(self):
        return f'/brokers/{self.pk}/'


class Order(models.Model):
    class Types(models.TextChoices):
        BUY = 'buy', 'Buy'
        SELL = 'sel', 'Sell'
        __empty__ = 'Choose type'

    type = models.CharField(
        max_length=3,
        choices=Types.choices,
        verbose_name='Type'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
    )

    description = models.TextField(
        verbose_name='Description',
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Price'
    )

    company = models.CharField(
        max_length=256,
        verbose_name='Company',
    )

    broker = models.ForeignKey(
        'Broker',
        on_delete=models.CASCADE,
        verbose_name='Broker',
        related_name='orders'
    )

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='orders'
    )

    def __str__(self):
        return f'{self.pk}. {self.broker.name}[{self.get_type_display()}]'

    def get_absolute_url(self):
        return f'/orders/{self.pk}/'


class Account(models.Model):
    balance = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Balance'
    )

    balance_with_shares = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Balance with shares'
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

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated'
    )

    def __str__(self):
        return f'{self.pk}. {self.user.username}[{self.balance}]'

    def get_absolute_url(self):
        return f'/accounts/{self.pk}/'


class Stock(models.Model):
    company = models.CharField(
        max_digits=256,
        verbose_name='Company'
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    purchase_price = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Price'
    )

    account = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
        verbose_name='Account',
        related_name='shares'
    )

    def __str__(self):
        return f'{self.pk}. {self.company}[{self.amount}]'

    def get_absolute_url(self):
        return f'/stocks/{self.pk}/'


class AccountHistory(models.Model):
    account = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
        verbose_name='Account',
        related_name='history'
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date'
    )

    balance = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Balance'
    )

    balance_with_shares = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Balance with shares'
    )

    def __str__(self):
        return f'history of account #{self.account.pk}'

    def get_absolute_url(self):
        return f'/history/{self.pk}/'
