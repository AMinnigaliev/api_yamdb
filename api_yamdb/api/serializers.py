from rest_framework import serializers

from users.validators import validate_username


class MixinUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)

    def validate_username(self, value):
        validate_username(value)
        return value


class SignupSerializer(MixinUsernameSerializer, serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)


class TokenSerializer(MixinUsernameSerializer, serializers.Serializer):
    confirmation_code = serializers.CharField(max_length=6, required=True)
