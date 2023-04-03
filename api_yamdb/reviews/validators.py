from django.core.validators import MaxValueValidator
from django.utils import timezone


def max_value_timezone_now(value):
    return MaxValueValidator(timezone.now().year)(value)
