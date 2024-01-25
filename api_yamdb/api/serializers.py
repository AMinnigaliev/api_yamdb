from rest_framework import serializers

from reviews.models import Genre, Category
from users.validators import validate_username


class MixinValidateUsernameSerializer:

    def validate_username(self, value):
        validate_username(value)
        return value


class MixinUsernameSerializer(serializers.Serializer,
                              MixinValidateUsernameSerializer,):
    username = serializers.CharField(max_length=150, required=True)


class SignupSerializer(MixinUsernameSerializer):
    email = serializers.EmailField(max_length=254, required=True)


class TokenSerializer(MixinUsernameSerializer):
    confirmation_code = serializers.CharField(max_length=6, required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
