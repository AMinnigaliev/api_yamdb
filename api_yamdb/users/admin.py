from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


UserAdmin.fieldsets += (
    (None, {'fields': ('bio', 'role')}),
)
admin.site.register(MyUser, UserAdmin)
