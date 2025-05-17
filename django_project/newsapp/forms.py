from django import forms
from django.contrib.auth.models import User
from .models import Post, UserProfile, Advertisement

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'content', 'category', 'banner_path', 'status']
        widgets = {
            'status': forms.Select(choices=[('draft', 'Draft'), ('published', 'Published'), ('unpublished', 'Unpublished'), ('edited', 'Edited After Approval')]),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'banner_path': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio', 'role']  # Added 'role' to allow editing
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'image', 'url', 'position', 'is_active', 'is_approved']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }