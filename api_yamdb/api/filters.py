from django_filters.rest_framework import CharFilter, FilterSet
from reviews.models import Title


class FilterTitle(FilterSet):
    category = CharFilter(field_name="category__slug")
    genre = CharFilter(field_name="genre__slug")
    name = CharFilter(field_name="name")
    year = CharFilter(field_name="year")
    rating = CharFilter(field_name="rating")

    class Meta:
        model = Title
        fields = ("name", "genre", "category", "year", "rating")
