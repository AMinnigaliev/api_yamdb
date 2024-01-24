from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    TitleViewSet, CategoryViewSet, GenreViewSet, CommentViewSet, ReviewViewSet)

app_name = 'api'


router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet,
    basename='comment',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(router.urls)),
]
