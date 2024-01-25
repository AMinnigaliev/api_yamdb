from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, signup, token

app_name = 'api'


auth_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token'),
]

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(router_v1.urls)),
]
