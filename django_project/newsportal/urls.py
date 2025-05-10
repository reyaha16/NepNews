"""
URL configuration for newsportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# newsapp/urls.py
from django.urls import path
from newsapp import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name='login-user'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('category/<int:id>/', views.category_post, name='category-post'),
    path('post/<int:id>/', views.view_post, name='view-post'),
    path('new-post/', views.new_post, name='new-post'),
    path('post-approval/', views.post_approval, name='post-approval'),
    path('profile/', views.profile_page, name='profile'),  # ✅ simplified name
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('search/', views.search_posts, name='search-posts'),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),
    path('post/<int:post_id>/bookmark/', views.bookmark_post, name='bookmark-post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add-comment'),
    path('post/edit/<int:id>/', views.edit_post, name='edit-post'),
    path('post/<int:id>/delete/', views.delete_post, name='delete-post'),
    path('ads/create/', views.create_advertisement, name='create_ad'),
    path('ads/<int:ad_id>/edit/', views.edit_advertisement, name='edit_advertisement'),
    path('ads/<int:ad_id>/delete/', views.delete_advertisement, name='delete_advertisement'),
    path('ads/', views.list_advertisements, name='list_ads'),

    path('about/', views.about, name='about-page'),
    path('contact/', views.contact, name='contact-page'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy-page'),
    path('terms/', views.terms, name='terms-page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)