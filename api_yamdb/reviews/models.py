from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

from .validators import max_value_timezone_now 

User = get_user_model()


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



class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='ID категории',
        max_length=50,
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='ID жанра',
        max_length=50,
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.IntegerField(
        validators=[max_value_timezone_now],
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titile_genre',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title_category',
        verbose_name='Категория',
    )

    class Meta():
        ordering = ('year',)
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name
