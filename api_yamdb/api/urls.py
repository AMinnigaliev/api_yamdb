from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet
    # TitleViewSet, CategoryViewSet, GenreViewSet

app_name = 'api'


router = DefaultRouter()
router.register('reviews', ReviewViewSet, basename='review')
router.register('comments', CommentViewSet, basename='comment')
# router.register('titles', TitleViewSet, basename='title')
# router.register('categories', CategoryViewSet, basename='category')
# router.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(router.urls)),
]