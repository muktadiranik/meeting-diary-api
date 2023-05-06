from django.contrib import admin
from django.contrib.auth import get_user_model
from meetings.models import *
User = get_user_model()

# Register your models here.
admin.site.unregister(User)


class DepartmentInline(admin.StackedInline):
    model = Department
    list_display = ("name",)
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username',
         'password', 'first_name', 'last_name',)}),
    )
    inlines = (DepartmentInline,)
