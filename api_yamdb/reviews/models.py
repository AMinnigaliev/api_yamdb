from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Slug категории', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Gener(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Slug жанра', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.DateField('Год выпуска', auto_now_add=True)
    description = models.TextField('Описание')
    genres = models.ManyToManyField(
        Gener,
        through='GenerTitle',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True, blank=False,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class GenerTitle(models.Model):
    genre = models.ForeignKey(Gener, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        verbose_name='username пользователя',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        'Рейтинг',
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True)
    title_id = models.ForeignKey(
        Title,
        verbose_name='ID произведения',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    def __str__(self):
        return self.score


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='username автора комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True)
    review_id = models.ForeignKey(
        Review,
        verbose_name='ID отзыва',
        on_delete=models.CASCADE,
        related_name='comments',
    )
