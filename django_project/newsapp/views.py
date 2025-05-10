from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Category, UserProfile, Like, Bookmark, Comment
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import PostForm
from .forms import UserForm, UserProfileForm


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
    categories = Category.objects.all()
    return render(request, 'index.html', {'posts': posts, 'categories': categories})

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Login successful.')
                return redirect('home-page')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid credentials.')
                return redirect('home-page')  # Redirect back with error message
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return redirect('home-page')  # Redirect back with error message
    
    # If GET request or something else
    return redirect('home-page')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('home-page')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('home-page')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('home-page')
        
        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            role='reader'  # Default role
        )
        
        # Log the user in
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, 'Account created successfully.')
        
        return redirect('home-page')  # Redirect to home page after signup
    
    # If GET request or something else
    return redirect('home-page')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home-page')  # Redirect to home page after logout
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse('reset-password', kwargs={'uidb64': uid, 'token': token})
            )
            subject = 'NepNews Password Reset Link'
            message = f'Click the link below to reset your password:\n\n{reset_link}\n\nThis link will expire in 1 hour.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, 'A password reset link has been sent to your email.')
            except Exception as e:
                messages.error(request, f'Failed to send email: {str(e)}')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
        return redirect('home-page')
    return render(request, 'index.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = PasswordResetTokenGenerator()
    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully. Please log in with your new password.')
            return redirect('home-page')
        return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('home-page')

def category_post(request, id):
    if not request.user.is_authenticated:
        return redirect('signup')
    category = get_object_or_404(Category, id=id)
    posts = Post.objects.filter(category=category, status='published')
    categories = Category.objects.all()
    return render(request, 'category_post.html', {'category': category, 'posts': posts, 'categories': categories})

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
    categories = Category.objects.all()
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        status = request.POST.get('status')
        post = get_object_or_404(Post, id=post_id)
        post.status = status
        post.save()
        return redirect('post-approval')
    return render(request, 'post_approval.html', {'drafts': drafts, 'categories': categories})

@login_required
def profile_page(request):
    categories = Category.objects.all()
    return render(request, 'profile.html', {'user': request.user, 'categories': categories})

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

def view_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.status != 'published':
        if not request.user.is_authenticated or (
            request.user != post.author and 
            request.user.userprofile.role not in ['editor', 'admin']
        ):
            return render(request, '404.html', status=404)

    post.views += 1
    post.save()
    comments = post.comments.all()
    return render(request, 'view-post.html', {
        'post': post,
        'comments': comments,
        'user': request.user,
    })

@login_required
def like_post(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

@login_required
def bookmark_post(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    post = get_object_or_404(Post, id=post_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
    if not created:
        bookmark.delete()
        bookmarked = False
    else:
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=request.user, post=post, content=content)
            return redirect('view-post', id=post_id)
    return redirect('view-post', id=post_id)

@login_required
@role_required('writer', 'editor', 'admin')
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.author and request.user.userprofile.role not in ['editor', 'admin']:
        return redirect('home-page')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if request.user.userprofile.role == 'writer':
            form.fields.pop('status', None)

        if form.is_valid():
            updated_post = form.save(commit=False)
            if post.status == 'approved' and request.user.userprofile.role == 'writer':
                updated_post.status = 'edited'
            updated_post.save()
            return redirect('view-post', id=updated_post.id)
    else:
        form = PostForm(instance=post)
        if request.user.userprofile.role == 'writer':
            form.fields.pop('status', None)

    return render(request, 'edit-post.html', {
        'form': form,
        'post': post,
    })

@login_required
@role_required('writer')
@require_POST
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('home-page')

    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('home-page')


@login_required
def edit_profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.userprofile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')  # ✅ matches the updated url name

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
