from datetime import date

from rest_framework import serializers

from reviews.models import Category, Genre, Title
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


class TitlePostPatchDelSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug')

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.')
        return value

    def to_representation(self, instance):
        return TitleGetSerializer(instance).data


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def to_representation(self, instance):
        try:
            if instance.rating:
                instance.rating = round(instance.rating)
        except AttributeError:
            instance.rating = None
        return super().to_representation(instance)
