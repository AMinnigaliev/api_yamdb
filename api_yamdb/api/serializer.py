from rest_framework import serializers

from users.validators import validate_username


class MixinValidateUsernameSerializer:

    def validate_username(self, value):
        validate_username(value)
        return value


class MixinUsernameSerializer(serializers.Serializer,
                              MixinValidateUsernameSerializer):
    username = serializers.CharField(max_length=150, required=True)


class SignupSerializer(MixinUsernameSerializer):
    email = serializers.EmailField(max_length=254, required=True)


class TokenSerializer(MixinUsernameSerializer):
    confirmation_code = serializers.CharField(max_length=6, required=True)
