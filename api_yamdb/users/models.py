from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
)


class MyUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[validate_username],
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    confirmation_code = models.CharField(
        'Проверочный код',
        max_length=6,
        blank=True,
    )
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=9, choices=CHOICES, default='user')
