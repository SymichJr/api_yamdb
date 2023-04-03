from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UsersUsernameView,
                    UserViewSet, create_user, get_token)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)


urlpatterns = [
    path("", include(router.urls)),
    path("auth/signup/", create_user),
    path("auth/token/", get_token),
    path("users/<username>/", UsersUsernameView.as_view()),
]
