from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(
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
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(
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
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title
