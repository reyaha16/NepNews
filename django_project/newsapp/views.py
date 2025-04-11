from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Category, UserProfile
from django.db.models import Q

def role_required(*roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.userprofile.role in roles:
                return view_func(request, *args, **kwargs)
            return redirect('login-user')
        return wrapper
    return decorator

def home_page(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Find the user by email
            user = User.objects.get(email=email)
            # Authenticate using the user's actual username
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-page')
            else:
                messages.error(request, 'Invalid password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email.')
    return render(request, 'index.html')
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('home-page')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('home-page')

        user = User.objects.create_user(
            username=email, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('home-page')
    return render(request, 'index.html')

def logout_user(request):
    logout(request)
    return redirect('home-page')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.success(request, 'A password reset link has been sent to your email.')
        else:
            messages.error(request, 'Email not found.')
        return redirect('home-page')
    return render(request, 'index.html')

def category_post(request, id):
    if not request.user.is_authenticated:
        return redirect('signup')
    category = get_object_or_404(Category, id=id)
    posts = Post.objects.filter(category=category, status='published')
    return render(request, 'category_post.html', {'category': category, 'posts': posts})

def view_post(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    post.views += 1
    post.save()
    return render(request, 'view-post.html', {'post': post})

@login_required
@role_required('writer', 'editor', 'admin')
def new_post(request):
    if request.method == 'POST':
        form_data = request.POST
        post = Post(
            title=form_data['title'],
            short_description=form_data['short_description'],
            content=form_data['content'],
            category_id=form_data['category'],
            author=request.user,
            banner_path=request.FILES.get('banner'),
            status='draft'
        )
        if request.user.userprofile.role in ['editor', 'admin']:
            post.status = form_data.get('status', 'draft')
        post.save()
        return redirect('home-page')
    categories = Category.objects.all()
    return render(request, 'new-post.html', {'categories': categories})

@login_required
@role_required('editor', 'admin')
def post_approval(request):
    drafts = Post.objects.filter(status='draft')
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        status = request.POST.get('status')
        post = get_object_or_404(Post, id=post_id)
        post.status = status
        post.save()
        return redirect('post-approval')
    return render(request, 'post_approval.html', {'drafts': drafts})

@login_required
def profile_page(request):
    return render(request, 'profile.html', {'user': request.user})

def search_posts(request):
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        context = {
            'query': query,
            'categories': Category.objects.all(),
        }
        
        if not query:
            context['message'] = "Please enter a search term."
            return render(request, 'search-post.html', context)
        
        # Search across title, content, short_description, and category name
        posts = Post.objects.filter(status='published').filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
        
        context['posts'] = posts
        if not posts.exists():
            context['message'] = f"No results found for '{query}'."
        
        return render(request, 'search-post.html', context)
    return redirect('home-page')