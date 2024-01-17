from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
)


class MyUser(AbstractUser):
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=9, choices=CHOICES, default='user')
