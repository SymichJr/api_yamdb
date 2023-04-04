import re

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, data):
        pattern = re.compile("^[\\w]{3,}")
        if re.match(pattern=pattern, string=data) is None:
            raise serializers.ValidationError("Имя запрещено!")
        if data == "me":
            raise serializers.ValidationError(
                'имя пользователя не может быть "me"'
            )
        return data

    def validate(self, data):
        username = data.get("username", None)
        email = data.get("email", None)

        if User.objects.filter(email=email, username=username).exists():
            return data

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("email занят.")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username занят.")
        return data

    class Meta:
        model = User
        fields = ("username", "email")


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            "bio",
            "first_name",
            "last_name",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre
        lookup_field = "slug"


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "rating",
            "category",
            "genre",
        )
        model = Title


class TitleAdminSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "category", "genre")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Review
        fields = ("id", "author", "text", "pub_date", "score", "title")
        read_only_fields = ("title",)
        unique_together = ("author", "title")

    def validate(self, data):
        request = self.context.get("request")
        title_id = self.context.get("view").kwargs.get("title_id")
        if (
            request.method == "POST"
            and Review.objects.filter(
                author=request.user, title=title_id
            ).exists()
        ):
            raise serializers.ValidationError(
                "Запрещенно добавлять больше одного отзыва!"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ("id", "author", "review", "text", "pub_date")
        read_only_fields = ("review",)
