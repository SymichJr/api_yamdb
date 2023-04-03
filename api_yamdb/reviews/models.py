from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email', unique=True)
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
    role = models.CharField("role", max_length=50, choices=users_role, default='user')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    UNIQUE_FIELDS = ['username']
    unique_together = ('username', 'email') 
    # class Meta:

        
        # = [
        #     (fields=["username", "email"], name="user_email")
        # ]

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
