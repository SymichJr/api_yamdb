from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import max_value_timezone_now


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    USERS_ROLE = (
        (USER, "пользователь"),
        (ADMIN, "администратор"),
        (MODERATOR, "модератор"),
    )
    first_name = models.TextField("Имя", blank=True, max_length=150)
    last_name = models.TextField("Фамилия", blank=True, max_length=150)
    email = models.EmailField(
        "Электронная почта", unique=True, blank=False, max_length=254
    )
    role = models.CharField(
        "Роль ", max_length=50, choices=USERS_ROLE, default=USER
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    UNIQUE_FIELDS = ["username"]
    unique_together = ("username", "email")

    @property
    def is_user(self):
        return self.role == "user"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_admin(self):
        return self.role == "admin"

    class Meta:
        ordering = ["id"]


class Genre(models.Model):
    name = models.CharField(
        verbose_name="Название жанра",
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name="ID жанра",
        max_length=50,
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name="Название категории",
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name="ID категории",
        max_length=50,
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    year = models.IntegerField(
        validators=[max_value_timezone_now],
        verbose_name="Год выпуска",
        db_index=True,
        blank=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="titile_genre",
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="title_category",
        verbose_name="Категория",
    )

    class Meta:
        ordering = ["year"]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name="Жанр"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "genre"], name="GenreTitle"
            ),
        ]
        verbose_name = "Жанр произведения"
        verbose_name_plural = "Жанры произведений"

    def __str__(self):
        return f"Произведение:{self.title} жанр:{self.genre}"


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField(
        max_length=2500,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    score = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name="Оценка",
        validators=[
            MinValueValidator(1, "От 1 до 10"),
            MaxValueValidator(10, "От 1 до 10"),
        ],
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_review"
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(
        verbose_name="Дата комментария", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["pub_date"]
