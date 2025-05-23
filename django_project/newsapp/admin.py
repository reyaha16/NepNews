from django.contrib import admin
from .models import Category, Post, UserProfile, Advertisement

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

@admin.action(description="Approve selected advertisements")
def approve_ads(modeladmin, request, queryset):
    queryset.update(is_approved=True)

@admin.action(description="Disapprove selected advertisements")
def disapprove_ads(modeladmin, request, queryset):
    queryset.update(is_approved=False)

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'is_active', 'is_approved', 'created_at')
    list_filter = ('position', 'is_active', 'is_approved')
    actions = [approve_ads, disapprove_ads]

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)