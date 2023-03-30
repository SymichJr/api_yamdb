from rest_framework.response import Response

from rest_framework import viewsets, mixins, status

from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import User, Title, Category, Genre
from .serializers import (UserSerializer,
                          ReviewSerializer,
                          CategorySerializer,
                          GenreSerializer)
from .permissions import IsAdminOrReadOnlyPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(viewsets.ModelViewSet):
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
    permission_classes = (IsAdminOrReadOnlyPermission, IsAuthenticatedOrReadOnly, )
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)



#class TitleViewSet(viewsets.ModelViewSet):
#     queryset = ?
#     lookup_field = 'slug'
#     filter_backends =
#     permission_classes = (#IsAdminOrReadOnlyPermission,
#                           IsAuthenticatedOrReadOnly, )