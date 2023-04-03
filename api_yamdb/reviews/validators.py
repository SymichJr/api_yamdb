from django.core.validators import MaxValueValidator
from django.utils import timezone


def max_value_timezone_now(value):
    message = f"Год выпуска не может быть позже {timezone.now().year}"
    return MaxValueValidator(timezone.now().year)(value)
