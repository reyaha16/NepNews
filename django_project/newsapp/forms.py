from django import forms
<<<<<<< HEAD
from django.contrib.auth.models import User
from .models import Post, UserProfile
=======
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'image', 'link', 'is_active']

from .models import Post
>>>>>>> b3e7c98be4789099278f1efadb84d36447b33da8

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'content', 'category', 'banner_path', 'status']
        widgets = {
<<<<<<< HEAD
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
        fields = ['profile_pic', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }
=======
            'status': forms.Select(choices=[('draft', 'Draft'), ('published', 'Published'), ('approved', 'Approved'), ('pending', 'Pending'), ('edited', 'Edited')]),
        }

>>>>>>> b3e7c98be4789099278f1efadb84d36447b33da8
