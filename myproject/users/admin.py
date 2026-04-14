# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'city', 'friends_count', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone', 'birth_date', 'avatar', 'bio', 'city', 'friends'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('email', 'phone', 'birth_date', 'bio', 'city'),
        }),
    )
    
    def friends_count(self, obj):
        return obj.friends.count()
    friends_count.short_description = 'Количество друзей'

admin.site.register(CustomUser, CustomUserAdmin)