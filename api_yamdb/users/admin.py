from itertools import chain

from django.contrib import admin

from api_yamdb.constants import CUT_LENGTH_TEXT
from reviews.models import Category, Comment, Genre, Review, Title
from users.abstracts import CommentReviewAdminBaseModel
from users.models import YamdbUser


@admin.register(YamdbUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role',
                    'first_name', 'last_name', 'bio_short')
    list_editable = ('role',)
    list_display_links = ('username',)
    search_fields = ('username',)
    ordering = ('username', 'first_name', 'last_name', 'role')

    def bio_short(self, obj):
        return u"%s..." % (obj.bio[:CUT_LENGTH_TEXT],)


@admin.register(Category, Genre)
class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('name', 'slug')


@admin.register(Review)
class ReviewAdmin(CommentReviewAdminBaseModel):
    list_display = ('id', 'text_short', 'author', 'score', 'pub_date', 'title')
    ordering = ('author', '-pub_date', '-score', 'title')


@admin.register(Comment)
class CommentAdmin(CommentReviewAdminBaseModel):
    list_display = ('id', 'text_short', 'author', 'pub_date', 'review')
    ordering = ('author', '-pub_date')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'description_short', 'category', 'genres')
    list_display_links = ('name',)
    list_editable = ('category',)
    search_fields = ('name',)
    ordering = ('name', '-year', 'category')
    filter_horizontal = ('genre',)

    def genres(self, obj):
        return list(chain.from_iterable(obj.genre.values_list('name')))

    def description_short(self, obj):
        return u"%s..." % (obj.description[:CUT_LENGTH_TEXT],)


admin.site.empty_value_display = 'пусто'
