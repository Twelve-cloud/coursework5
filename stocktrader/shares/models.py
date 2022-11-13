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
        LIMIT = 'lt', 'Limit'
        MARKET = 'mt', 'Market'
        __empty__ = 'Choose type'

    class Status(models.TextChoices):
        PROCCESS = 'pc', 'Process'
        DONE = 'dn', 'Done'
        __empty__ = 'Choose status'

    class Currency(models.TextChoices):
        USD = 'usd', 'Dollar'
        EUR = 'eur', 'Euro'
        RUB = 'rub', 'Ruble'
        __empty__ = 'Choose currency'

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

    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        verbose_name='Currency'
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name='Price'
    )

    broker = models.ForeignKey(
        'Broker',
        on_delete=models.CASCADE,
        verbose_name='Broker',
        related_name='orders'
    )

    def __str__(self):
        return f'{self.pk}. {self.broker.name}[{self.type}]'

    def get_absolute_url(self):
        return f'/orders/{self.pk}/'


class Deal(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
    )

    description = models.TextField(
        verbose_name='Description',
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

    def __str__(self):
        return f'{self.pk}. {self.user.username}[{self.created_at}]'

    def get_absolute_url(self):
        return f'/deals/{self.pk}/'


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

    def __str__(self):
        return f'{self.pk}. {self.user.username}[{self.balance}]'

    def get_absolute_url(self):
        return f'/accounts/{self.pk}/'
