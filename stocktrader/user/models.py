from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email',
    )

    image = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Image',
    )

    is_blocked = models.BooleanField(
        default=False,
        verbose_name='Blocked?',
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name='Active?'
    )

    follows = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='followers',
        verbose_name='Follows'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'is_active']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-is_blocked', 'username']
        db_table = 'User'

    def __str__(self):
        return f'{self.id}. {self.username}'

    def get_absolute_url(self):
        return f'/users/{self.pk}/'
