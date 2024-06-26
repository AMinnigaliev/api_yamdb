from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminUserOrReadOnly


class GenreCategoryViewMixin(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):

    lookup_field = 'slug'
    permission_classes = [IsAdminUserOrReadOnly]
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
