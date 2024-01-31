from django.contrib import admin

from api_yamdb.constants import CUT_LENGTH_TEXT


class CommentReviewAdminBaseModel(admin.ModelAdmin):
    search_fields = ('author__username',)

    def text_short(self, obj):
        return u"%s..." % (obj.text[:CUT_LENGTH_TEXT],)
