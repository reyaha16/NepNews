# newsapp/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('writer', 'Writer'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
        ('ads_manager', 'Ads Manager'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('unpublished', 'Unpublished'),
<<<<<<< HEAD
        ('edited', 'Edited After Approval'),  # new status
=======

        ('edit', 'Edit'),

        ('edited', 'Edited After Approval'),  # new status

>>>>>>> b3e7c98be4789099278f1efadb84d36447b33da8
    )
    
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    banner_path = models.ImageField(upload_to='banners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
<<<<<<< HEAD
=======
    

class Advertisement(models.Model):
    POSITION_CHOICES = [
        ('top', 'Top'),
        ('sidebar', 'Sidebar'),
        ('bottom', 'Bottom'),
        ('front', 'Front Page'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ads/')
    link = models.URLField(blank=True, null=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='top')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False) 

    def __str__(self):
        return self.title
>>>>>>> b3e7c98be4789099278f1efadb84d36447b33da8

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
<<<<<<< HEAD
        return f"Comment by {self.user.username} on {self.post.title}"
=======
        return f"Comment by {self.user.username} on {self.post.title}"

>>>>>>> b3e7c98be4789099278f1efadb84d36447b33da8
