from datetime import date

from rest_framework import serializers

from reviews.models import Comment, Review
    # Title, Genre, Category


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        lookup_field = 'comment_id'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        lookup_field = 'review_id'

# class CategorySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Category
#         fields = ('name', 'slug')
#         lookup_field = 'slug'
#
#
# class GenreSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Genre
#         fields = ('name', 'slug')
#         lookup_field = 'slug'
#
#
# class TitlePostPatchDelSerializer(serializers.ModelSerializer):
#
#     category = serializers.SlugRelatedField(
#         queryset=Category.objects.all(), slug_field='slug')
#     genre = serializers.SlugRelatedField(
#         queryset=Genre.objects.all(), many=True, slug_field='slug')
#     rating = serializers.FloatField(read_only=True)
#
#     class Meta:
#         model = Title
#         fields = (
#             'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
#
#     def validate_year(self, value):
#         year = date.today().year
#         if value > year:
#             raise serializers.ValidationError(
#                 'Год выпуска не может быть больше текущего.')
#         return value
#
#
# class TitleGetSerializer(TitlePostPatchDelSerializer):
#
#     category = CategorySerializer()
#     genre = GenreSerializer(many=True)
