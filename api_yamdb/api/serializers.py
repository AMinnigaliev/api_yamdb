from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Title, Review
from users.validators import validate_username

User = get_user_model


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)

    def validate_username(self, value):
        validate_username(value)
        return value


class SignupSerializer(UsernameSerializer):
    email = serializers.EmailField(max_length=254, required=True)


class TokenSerializer(UsernameSerializer):
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


class UserSerializer(UsernameSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class MeUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         read_only=True, slug_field='username')
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'text', 'author', 'pub_date')
#         # lookup_field = 'comment'


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
