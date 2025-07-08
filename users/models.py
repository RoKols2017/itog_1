from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name='Telegram ID')
    telegram_link_token = models.CharField(max_length=64, null=True, blank=True, unique=True, verbose_name='Токен для привязки Telegram')

    def __str__(self):
        return self.username
