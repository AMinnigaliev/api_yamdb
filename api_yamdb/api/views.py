from django.db.models import Avg, F
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import SAFE_METHODS

from api.permissions import IsAdminUserOrReadOnly
from api.serializers import (TitleGetSerializer,
                             TitlePostPatchDelSerializer,
                             GenreSerializer,
                             CategorySerializer,
                             CommentSerializer,
                             ReviewSerializer,)
from reviews.models import Title, Genre, Category, Comment, Review


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet,):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly,)
    http_method_names = ['get', 'post', 'delete']


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly,)
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return super().get_queryset().annotate(rating=Avg(F('reviews__score')))

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleGetSerializer
        return TitlePostPatchDelSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.kwargs['review_id'],
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.kwargs['review_id'],
        )
