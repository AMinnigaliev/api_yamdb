from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.abstracts import CategoryGenreBaseModel, CommentReviewBaseModel
from reviews.validators import validate_year

from api_yamdb.constants import (CATEGORY_NAME_LENGTH, GENRE_NAME_LENGTH,
                                 TITLE_NAME_LENGTH)

User = get_user_model()


class Category(CategoryGenreBaseModel):
    name = models.CharField(
        'Название категории',
        max_length=CATEGORY_NAME_LENGTH,
    )

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBaseModel):
    name = models.CharField(
        'Название жанра',
        max_length=GENRE_NAME_LENGTH,
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=TITLE_NAME_LENGTH,
    )
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
        ordering = ('name', 'year')

    def __str__(self):
        return self.name


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
