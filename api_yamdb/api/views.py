from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
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

from api.serializers import (TitleGetSerializer,
                             TitlePostPatchDelSerializer,
                             GenreSerializer,
                             CategorySerializer,
                             CommentSerializer,
                             ReviewSerializer,
                             SignupSerializer,
                             TokenSerializer,
                             UserSerializer,
                             MeUserSerializer)
from api.permissions import (IsAdminUserOrReadOnly,
                             IsAdminUser,
                             IsAuthorAdminModeratorOrReadOnly,)
from api.filters import TitleFilter
from reviews.models import Title, Genre, Category, Review

User = get_user_model()


def get_title_obj(title_id):
    return get_object_or_404(Title, pk=title_id)


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
    """Выдача JWT-токена."""
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

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryViewMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):

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


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями."""
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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        title = get_title_obj(self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_title_obj(self.kwargs['title_id']),
        )
