from django.contrib.auth import get_user_model
from django.db import models

from api_yamdb.constants import CUT_LENGTH_TEXT, NAME_MAX_LENGTH

User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Slug', unique=True)

    class Meta:
        abstract = True
        ordering = ('name', 'slug')

    def __str__(self):
        return self.slug


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
