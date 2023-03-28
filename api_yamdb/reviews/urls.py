from reviews.views import UserViewSet
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r"users", UserViewSet)



urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", TokenObtainPairView.as_view(), name='token_obtain_pair')
]