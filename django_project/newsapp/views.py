from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Category, UserProfile, Like, Bookmark, Comment
from django.db.models import Q
from .models import Advertisement
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AdvertisementForm
from functools import wraps 
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import PostForm

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)  
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.userprofile.role in roles:
                return view_func(request, *args, **kwargs)
            return redirect('login-user')
        return wrapper
    return decorator

def home_page(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')

    ads = Advertisement.objects.filter(is_approved=True, is_active=True)

    context = {
        'posts': posts,
        'ads_top': ads.filter(position='top'),
        'ads_sidebar': ads.filter(position='sidebar'),
        'ads_bottom': ads.filter(position='bottom'),
        'ads_front': ads.filter(position='front'),
    }

    return render(request, 'index.html', context)

    return render(request, 'index.html', {'posts': posts})

    categories = Category.objects.all()
    return render(request, 'index.html', {'posts': posts, 'categories': categories})


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
@role_required('editor', 'admin')
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.short_description = request.POST.get('short_description')
        post.content = request.POST.get('content')
        post.category_id = request.POST.get('category')
        post.banner_path = request.FILES.get('banner') or post.banner_path
        post.status = request.POST.get('status')
        post.save()
        return redirect('home-page')

    categories = Category.objects.all()
    return render(request, 'edit_post.html', {'post': post, 'categories': categories})



@login_required
def profile_page(request):
    return render(request, 'profile.html', {'user': request.user})

def search_posts(request):
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        category_id = request.GET.get('category', '')
        posts = Post.objects.filter(status='published')
        selected_category_name = None

        if category_id:
            posts = posts.filter(category__id=category_id)
            try:
                selected_category_name = Category.objects.get(id=category_id).name
            except Category.DoesNotExist:
                selected_category_name = None

        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(short_description__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()

        context = {
            'query': query,
            'categories': Category.objects.all(),
            'selected_category': category_id,
            'selected_category_name': selected_category_name,
            'posts': posts,
        }


        if not posts.exists():
            context['message'] = f"No results found for '{query}'." if query else "No results found."

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


def is_ads_manager(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'ads_manager'

@login_required
@user_passes_test(lambda u: u.userprofile.role == 'ads_manager')
def list_advertisements(request):
    position = request.GET.get('position')
    ads = Advertisement.objects.all()
    if position:
        ads = ads.filter(position=position)

    positions = ['top', 'sidebar', 'bottom', 'front']
    return render(request, 'ads/list_ads.html', {
        'ads': ads,
        'positions': positions,
        'selected_position': position
    })

@login_required
@user_passes_test(lambda u: u.userprofile.role == 'ads_manager')
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_ads')
    else:
        form = AdvertisementForm()
    return render(request, 'ads/create_ad.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(lambda u: u.userprofile.role == 'ads_manager')
def edit_advertisement(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('list_ads')
    else:
        form = AdvertisementForm(instance=ad)
    return render(request, 'ads/edit_ad.html', {'form': form, 'action': 'Edit'})

@login_required
@user_passes_test(lambda u: u.userprofile.role == 'ads_manager')
def delete_advertisement(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)
    if request.method == 'POST':
        ad.delete()
    return redirect('list_ads')


@login_required
@user_passes_test(lambda u: u.userprofile.role == 'admin')
def review_advertisements(request):
    pending_ads = Advertisement.objects.filter(is_approved=False)

    if request.method == 'POST':
        ad_id = request.POST.get('ad_id')
        action = request.POST.get('action')
        ad = get_object_or_404(Advertisement, id=ad_id)
        
        if action == 'approve':
            ad.is_approved = True
            ad.save()
        elif action == 'reject':
            ad.delete()
        return redirect('review_ads')

    return render(request, 'ads/review_ads.html', {'pending_ads': pending_ads})


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def terms(request):
    return render(request, 'terms.html')

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

