from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg, F
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (IsAdminUser, IsAdminUserOrReadOnly,
                             IsAuthorAdminModeratorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, MeUserSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleGetSerializer, TitlePostPatchDelSerializer,
                             TokenSerializer, UserSerializer)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    """
    Регистрация нового пользователя.
    """
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    try:
        user, created = User.objects.get_or_create(
            email=email,
            username=username,
        )
    except IntegrityError:
        return Response(
            {'error':
                (f'Пользователь с username = {username} '
                 f'или email = {email} уже существует! '
                 'Если это вы, проверьте правильность введённых данных.')},
            status=status.HTTP_400_BAD_REQUEST,
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
    """
    Выдача JWT-токена.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username'),
    )
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if user.confirmation_code == confirmation_code:
        return Response(
            {'token': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_200_OK,
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST,
    )


class UserViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        url_name='users_detail',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=MeUserSerializer,
    )
    def users_detail(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreCategoryViewMixin:

    lookup_field = 'slug'
    permission_classes = [IsAdminUserOrReadOnly]
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(GenreCategoryViewMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet,):
    """
    Ресурс жанров произведений.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryViewMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,):
    """
    Ресурс категорий произведений.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Ресурс произведений.
    """
    queryset = Title.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return super().get_queryset().annotate(rating=Avg(F('reviews__score')))

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleGetSerializer
        return TitlePostPatchDelSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Ресурс комментариев к отзывам.
    """
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorAdminModeratorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        review = self.get_review_object()
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review_object(),
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Ресурс отзывов на произведения.
    """
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorAdminModeratorOrReadOnly]

    def get_title_object(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title_object()
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title_object(),
        )
