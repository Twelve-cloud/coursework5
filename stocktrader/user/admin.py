from django.contrib import admin
from user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_display_links = ('email', 'username')
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    ordering = ('email', 'username')


admin.site.register(User, UserAdmin)
