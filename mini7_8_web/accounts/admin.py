from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('user_id', 'name', 'email', 'is_admin', 'is_staff', 'is_active', 'date_joined', 'last_login')
    search_fields = ('user_id', 'name', 'email')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('user_id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
