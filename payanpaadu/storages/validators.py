from django.core.exceptions import ValidationError


def picture_size_validator(value):
    fifty_kb = 50 * 1000

    if value.size > fifty_kb:
        raise ValidationError('The maximum picture size that can be uploaded is 50 KB')

    return value
