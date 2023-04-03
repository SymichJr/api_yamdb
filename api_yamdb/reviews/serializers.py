from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from reviews.models import User, Token


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')
    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError('имя пользователя не может быть "me"')
        return data

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            # "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()
        del self.fields["password"]

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs["username"])
        confirm_code = get_object_or_404(Token, user_id=user.id)
        if confirm_code.token != attrs["confirmation_code"]:
            raise serializers.ValidationError("Неверный код активации API")
        authenticate_kwargs = {
            'username': user,
            'confirmation_code': confirm_code,
        }
        self.user = authenticate(**authenticate_kwargs)
        jwt_token = str(self.get_token(self.user))
        return {"access": jwt_token}