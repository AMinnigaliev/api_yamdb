from django.urls import include, path
from rest_framework import routers

from api.views import UserViewSet, signup, token

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')

auth_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns))
]
