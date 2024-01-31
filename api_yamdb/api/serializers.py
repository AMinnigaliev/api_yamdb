from django.core.validators import validate_slug
from rest_framework import serializers

from api_yamdb.constants import (CODE_MAX_LENGTH,
                                 EMAIL_MAX_LENGTH,
                                 USERNAME_MAX_LENGTH)
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_year
from users.models import YamdbUser
from users.validators import validate_username


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH,
                                     required=True)

    def validate_username(self, value):
        validate_username(value)
        return value


class SignupSerializer(UsernameSerializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH,
                                   required=True)


class TokenSerializer(UsernameSerializer):
    confirmation_code = serializers.CharField(max_length=CODE_MAX_LENGTH,
                                              required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = YamdbUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate_username(self, value):
        validate_username(value)
        return value


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
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug',
        required=True,
        validators=[validate_slug]
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        validate_year(value)
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
                if instance.rating is None:
                    instance.rating = 0
                else:
                    instance.rating = round(instance.rating)
        except AttributeError:
            instance.rating = 0
        return super().to_representation(instance)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            try:
                title_id = self.context.get('view').kwargs.get('title_id')
                author = request.user.id
                Review.objects.get(
                    title=title_id,
                    author=author,
                )
                raise serializers.ValidationError(
                    'You can add only one review per title!')
            except Review.DoesNotExist:
                pass
        return data
