# Константы для приложения users и api
ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
CHOICES = (
    (ADMIN, 'Админ'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь'),
)
USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
CONFIRMATION_CODE_LENGTH = 6

# Константы для приложения reviews
NAME_MAX_LENGTH = 256

# Размер среза для строк отображаемых в админ зоне
CUT_LENGTH_TEXT = 30
