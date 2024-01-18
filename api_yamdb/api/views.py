from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializer import SignupSerializer, TokenSerializer


@api_view(['POST'])
def signup(request):
    """Регистрация нового пользователя."""
    serializer = SignupSerializer(data=request.data)


@api_view(['POST'])
def token(request):
    """Выдача JWT-токена пользователю."""
    serializer = TokenSerializer(data=request.data)
