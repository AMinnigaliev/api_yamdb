from rest_framework import viewsets, mixins

from api.permissions import IsAdminUserOrReadOnly
from api.serializers import GenreSerializer, CategorySerializer
from reviews.models import Genre, Category


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
