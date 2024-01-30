from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    year = date.today().year
    if value > year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего.')
    return value
