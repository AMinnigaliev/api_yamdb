import re

from django.core.exceptions import ValidationError


def validate_username(value):
    pattern = re.compile(r'^[\w.@+-]+\Z')
    if value.lower() == 'me':
        raise ValidationError(message='Значение "me" не валидно.')
    if not pattern.match(value):
        raise ValidationError(message='Поле содержит некорректные символы.')
    return value
