from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.constants import (CUT_LENGTH_TEXT,
                                 CATEGORYNAME_MAX_LENGTH,
                                 GENRENAME_MAX_LENGTH,
                                 GENRESLUG_MAX_LENGTH,
                                 TITLENAME_MAX_LENGTH)
from reviews.validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название категории',
                            max_length=CATEGORYNAME_MAX_LENGTH)
    slug = models.SlugField('Slug категории', unique=True)

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Название жанра',
                            max_length=GENRENAME_MAX_LENGTH)
    slug = models.SlugField('Slug жанра',
                            max_length=GENRESLUG_MAX_LENGTH,
                            unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('Название',
                            max_length=TITLENAME_MAX_LENGTH)
    year = models.SmallIntegerField('Год выпуска', validators=[validate_year])
    description = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class CommentReviewBaseModel(models.Model):

    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        verbose_name='username пользователя',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        default_related_name = u'%(model_name)ss'

    def __str__(self):
        return str(self.text[:CUT_LENGTH_TEXT])


class Review(CommentReviewBaseModel):

    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )

    class Meta(CommentReviewBaseModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('title', 'author')
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title',
            )
        ]


class Comment(CommentReviewBaseModel):

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )

    class Meta(CommentReviewBaseModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('review', 'author', '-pub_date')
