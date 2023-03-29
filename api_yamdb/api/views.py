from reviews.models import User, Title
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404

from reviews.models import Category
from .serializers import UserSerializer, ReviewSerializer, CategorySerializer
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
    permission_classes = IsAdminOrReadOnlyPermission
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
