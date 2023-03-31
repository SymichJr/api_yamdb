
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from rest_framework.pagination import PageNumberPagination

from reviews.models import User, Title, Category, Genre, Review
from .serializers import (UserSerializer,
                          ReviewSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          TitleAdminSerializer,
                          CommentSerializer)
from .permissions import IsAdminOrReadOnlyPermission, IsAdminModeratorOwnerOrReadOnly
from .filters import FilterTitle


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission, )
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,  )
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating = Avg('reviews__score')
    ).all().order_by('year')
    permission_classes = (IsAdminOrReadOnlyPermission, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = FilterTitle


    def get_serializer_class(self):
        if self.request.method not in ('POST', 'PUT', 'PATCH'):
            return TitleSerializer
        return TitleAdminSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminModeratorOwnerOrReadOnly, )
    
    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
    
    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)