from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.constants import (USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH,
    CODE_MAX_LENGTH, CHOICES, USER, ADMIN, MODERATOR)
from users.validators import validate_username


class YamdbUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[validate_username],
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    confirmation_code = models.CharField(
        'Проверочный код',
        max_length=CODE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Тип пользователя',
        max_length=max(map(lambda x: len(x[0]), CHOICES)),
        choices=CHOICES,
        default=USER,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR
