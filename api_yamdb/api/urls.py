from django.urls import include, path

from api.views import signup, token

app_name = 'api'


auth_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns))
]
