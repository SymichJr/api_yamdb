from rest_framework.routers import DefaultRouter

from django.urls import path

from reviews.views import (
    SignupView,
    UserViewSet,
    MyTokenObtainPairView,
    UserMeView,
    UsersUsernameView,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("users/me/", UserMeView.as_view()),
    path("users/<str:username>/", UsersUsernameView.as_view()),
    path("auth/token/", MyTokenObtainPairView.as_view()),
    path("auth/signup/", SignupView.as_view()),
] + router.urls
