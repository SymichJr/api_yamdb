from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user = "user"
    admin = "admin"
    moderator = "moderator"
    users_role = [
        (user, 'пользователь'),
        (admin, 'администратор'),
        (moderator, 'модератор'),
    ]
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField("role",max_length=50, choices = users_role, default=user)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']