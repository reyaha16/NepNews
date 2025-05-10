from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'content', 'category', 'banner_path', 'status']
        widgets = {
            'status': forms.Select(choices=[('draft', 'Draft'), ('published', 'Published'), ('approved', 'Approved'), ('pending', 'Pending'), ('edited', 'Edited')]),
        }
