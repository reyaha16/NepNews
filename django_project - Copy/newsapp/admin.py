from django.contrib import admin
from .models import Category, Post, UserProfile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    list_editable = ('status',)
    date_hierarchy = 'created_at'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)