from reviews.models import User, Review, Title
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "bio", "first_name", "last_name")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'pub_date', 'score', 'title')
    
    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Запрещенно добавлять больше одного отзыва'
                )
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'



