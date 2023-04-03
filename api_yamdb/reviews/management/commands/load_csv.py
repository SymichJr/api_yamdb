from csv import DictReader

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)

from django.core.management import BaseCommand



class Command(BaseCommand):
    """
    Перед запуском удалите файл db.sqlite3 в директории api_yamdb
    Запустите команду python manage.py migrate --run-syncdb
    Запустите импорт команду python manage.py load_csv
    """

    help = "Импорт .csv в Django Database"

    def handle(self, *args, **kwargs):
        for row in DictReader(
                open("static/data/users.csv", encoding="utf-8")
            ):
                users = User(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    role=row["role"],
                    bio=row["bio"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                )
                users.save()

        for row in DictReader(
                open("static/data/category.csv", encoding="utf-8")
            ):
                category = Category(
                    id=row["id"], name=row["name"], slug=row["slug"]
                )
                category.save()

        for row in DictReader(
                open("static/data/genre.csv", encoding="utf-8")
            ):
                genre = Genre(id=row["id"], name=row["name"], slug=row["slug"])
                genre.save()

        for row in DictReader(
                open("static/data/titles.csv", encoding="utf-8")
            ):
                titles = Title(
                    id=row["id"],
                    name=row["name"],
                    year=row["year"],
                    category=Category.objects.get(id=row["category"]),
                )
                titles.save()

        for row in DictReader(
                open("static/data/genre_title.csv", encoding="utf-8")
            ):
                genre_title = GenreTitle(
                    id=row["id"],
                    title=Title.objects.get(id=row["title_id"]),
                    genre=Genre.objects.get(id=row["genre_id"]),
                )
                genre_title.save()

        for row in DictReader(
                open("static/data/review.csv", encoding="utf-8")
            ):
                review = Review(
                    id=row["id"],
                    title=Title.objects.get(id=row["title_id"]),
                    text=row["text"],
                    author=User.objects.get(id=row["author"]),
                    score=row["score"],
                    pub_date=row["pub_date"],
                )
                review.save()

        for row in DictReader(
                open("static/data/comments.csv", encoding="utf-8")
            ):
                comments = Comment(
                    id=row["id"],
                    review=Review.objects.get(id=row["review_id"]),
                    text=row["text"],
                    author=User.objects.get(id=row["author"]),
                    pub_date=row["pub_date"],
                )
                comments.save()
