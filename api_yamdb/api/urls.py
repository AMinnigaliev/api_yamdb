from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       UserViewSet,
                       signup,
                       token,)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')

auth_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(router_v1.urls)),
]
