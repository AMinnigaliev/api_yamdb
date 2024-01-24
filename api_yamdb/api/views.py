from rest_framework import filters, viewsets, mixins

from api.permissions import IsAdminUserOrReadOnly
from api.serializers import GenreSerializer, CategorySerializer
from reviews.models import Genre, Category


class GenreCategoryViewMixin:

    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly,)
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=slug',)


class GenreViewSet(GenreCategoryViewMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet,):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryViewMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
