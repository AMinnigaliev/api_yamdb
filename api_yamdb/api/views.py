from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import SignupSerializer, TokenSerializer


User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    """Регистрация нового пользователя."""
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    try:
        user, created = User.objects.get_or_create(
            email=email,
            username=username
        )
    except IntegrityError:
        return Response(
            {'error':
                (f'Пользователь с username = {username} '
                 f'или email = {email} уже существует! '
                 'Если это вы, проверьте правильность введённых данных.')
             },
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = get_random_string(length=6)
    user.save()
    send_mail(
        subject="Регистрация на YaMDb",
        message=f'Ваш проверочный код {user.confirmation_code}.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token(request):
    """Выдача JWT-токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if user.confirmation_code == confirmation_code:
        return Response(
            {'Токен': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )
