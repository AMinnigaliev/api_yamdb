import copy
from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Genre, Category, Comment, Review


User = get_user_model() # НЕОБХОДИМО УБРАТЬ!!!!!!!!!!!!!!!++++===----!!!!!!


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


class TitleSerializerMixin:

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class TitlePostPatchDelSerializer(TitleSerializerMixin,
                                  serializers.ModelSerializer,):

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug')
    rating = serializers.FloatField(read_only=True)

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.')
        return value

    def to_representation(self, instance):
        return TitleGetSerializer(instance).data


class TitleGetSerializer(TitleSerializerMixin,
                         serializers.ModelSerializer,):

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField(read_only=True)


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
        default=serializers.CurrentUserDefault(),
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
        