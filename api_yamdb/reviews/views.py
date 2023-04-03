from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from .wrappers import print_args
from .token import generate_token
from .serializers import (
    UserSerializer, MyTokenObtainPairSerializer, SignUpSerializer)
from .models import User, Token


def save_token(username, confirm_code):
    user = get_object_or_404(User, username=username)
    token = Token(user_id=user.id, token=confirm_code)
    token.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)


class SignupView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.data["username"]
            email = serializer.data["email"]
            subject = "Email verification for django"
            confirm_code = generate_token()
            message = f"Confirm_code - {confirm_code}"
            save_token(user, confirm_code)
            send_mail(subject, message, settings.EMAIL_BACKEND, [email])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersUsernameView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):# pk=None
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)
