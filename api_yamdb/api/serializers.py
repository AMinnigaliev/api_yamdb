import copy
from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Title, Review
from users.validators import validate_username

User = get_user_model() # НЕОБХОДИМО УБРАТЬ!!!!!!!!!!!!!!!++++===----!!!!!!


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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        # lookup_field = 'comment'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=User.objects.get(pk=1),
        # default=serializers.CurrentUserDefault(),
    )
    title = serializers.HiddenField(default=None)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        lookup_field = 'review'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
            )
        ]

    def get_fields(self):
        print(f'\ndeepcopy = {copy.deepcopy(self._declared_fields)}\n')
        print(f'\n_declared_fields = {self._declared_fields}\n')
        return super().get_fields()

    # def create(self, validated_data):
    #     print(f'\nvalidated_data = {validated_data}\n')
    #     print(f'\nCurrentUserDefault = '
    #           f'{self.data}\n')
    #     return super().create(validated_data)
