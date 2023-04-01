from reviews.models import User, Token
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "bio",
            "first_name",
            "last_name",
        )

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError('имя пользователя не может быть "me"')
        return data
    
    # def validate_first_name(self, data):
    #     if len(data) >= 150:
    #         raise serializers.ValidationError("длинна first_name  не превышать 150 символов")
    #     return data
    # def validete_last_name(self, data):
    #     if len(data) >= 150:
    #         raise serializers.ValidationError("last_name не превышать 150 символов")
    #     return data


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = AccessToken


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirm_code"] = serializers.CharField()
        del self.fields["password"]

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs["username"])
        except User.DoesNotExist:
            raise serializers.ValidationError("нет такого пользователя")
        confirm_code = get_object_or_404(Token, user_id=user.id)
        if confirm_code.token != attrs["confirm_code"]:
            raise serializers.ValidationError("Неверный код активации API")
        jwt_token = str(self.get_token(user))
        return {"access": jwt_token}
