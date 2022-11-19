from pyex.services import get_stock_latest_price
from django.dispatch import receiver
from shares.apps import update_price
from django.db import models


class Broker(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Name'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description',
    )

    rate = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Rate'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
    )

    class Meta:
        verbose_name = 'Broker'
        verbose_name_plural = 'Brokers'
        ordering = ('name', 'rate')
        db_table = 'Broker'
        get_latest_by = 'created_at'

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

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description',
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    company = models.CharField(
        max_length=256,
        verbose_name='Company',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
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

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('type', 'company', 'amount')
        db_table = 'Order'
        get_latest_by = 'created_at'

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
        verbose_name='Shares balance'
    )

    broker = models.ForeignKey(
        'Broker',
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

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ('balance', 'balance_with_shares')
        db_table = 'Account'

    def __str__(self):
        return f'{self.pk}. {self.user.username}[{self.balance}]'

    def get_absolute_url(self):
        return f'/accounts/{self.pk}/'


class Stock(models.Model):
    company = models.CharField(
        max_length=256,
        verbose_name='Company'
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    current_price = models.FloatField(
        verbose_name='Current price'
    )

    account = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
        verbose_name='Account',
        related_name='shares'
    )

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ('company', 'amount', 'current_price')
        db_table = 'Stock'
        unique_together = ('company', 'account')

    def __str__(self):
        return f'{self.pk}. {self.company}[{self.amount}]'

    def get_absolute_url(self):
        return f'/stocks/{self.pk}/'

    @receiver(update_price)
    def update_current_price(sender, **kwargs):
        stock = sender.objects.get(pk=kwargs['pk'])
        stock.update(current_price=get_stock_latest_price())


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
        verbose_name='Shares balance'
    )

    class Meta:
        verbose_name = 'AccountHistory'
        verbose_name_plural = 'AccountHistories'
        ordering = ('balance', 'balance_with_shares')
        db_table = 'AccountHistory'

    def __str__(self):
        return f'history of account #{self.account.pk}'

    def get_absolute_url(self):
        return f'/history/{self.pk}/'
