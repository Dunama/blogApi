import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


logger = logging.getLogger(__name__)


@login_required(login_url='/signin/')
def index(request):
    # Renders the existing landing page template.
    from accounts.models import Follow, Profile
    from posts.models import Post

    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    posts = (
        Post.objects.select_related('author')
        .prefetch_related('likes', 'comments', 'comments__author')
        .order_by('-created_at')
    )
    liked_post_ids = set(
        Post.objects.filter(likes=request.user).values_list('id', flat=True)
    )

    following_user_ids = set(
        Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    )
    suggestions_username_profile_list = (
        Profile.objects.select_related('user')
        .exclude(user=request.user)
        .order_by('user__username')[:8]
    )
    return render(
        request,
        'index.html',
        {
            'posts': posts,
            'liked_post_ids': liked_post_ids,
            'user_profile': user_profile,
            'suggestions_username_profile_list': suggestions_username_profile_list,
            'following_user_ids': following_user_ids,
        },
    )


def signin(request):
    # Handles the HTML login form on GET/POST.
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')

            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, 'Invalid username or password')
                return redirect('/signin/')

            login(request, user)
            return redirect('/')
        except Exception:
            logger.exception('Web signin failed')
            messages.error(request, 'Login failed due to a server error. Please try again.')
            return redirect('/signin/')

    return render(request, 'signin.html')


def signup(request):
    # Handles the HTML signup form on GET/POST.
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')

            if not username:
                messages.error(request, 'Username is required')
                return redirect('/signup/')

            if password != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('/signup/')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('/signup/')

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/')
        except Exception:
            logger.exception('Web signup failed')
            messages.error(request, 'Signup failed due to a server error. Please try again.')
            return redirect('/signup/')

    return render(request, 'signup.html')


@login_required(login_url='/signin/')
def settings_view(request):
    from accounts.models import Profile

    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        bio = (request.POST.get('bio') or '').strip()
        location = (request.POST.get('location') or '').strip()
        image = request.FILES.get('image')

        user_profile.bio = bio
        user_profile.location = location
        if image is not None:
            user_profile.profileimg = image
        user_profile.save()

        messages.success(request, 'Profile updated')
        return redirect('/settings/')

    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='/signin/')
def search(request):
    from accounts.models import Profile

    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    username = ''
    username_profile_list = Profile.objects.none()

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        if username:
            username_profile_list = (
                Profile.objects.select_related('user')
                .filter(user__username__icontains=username)
                .exclude(user=request.user)
            )

    return render(
        request,
        'search.html',
        {
            'user_profile': user_profile,
            'username': username,
            'username_profile_list': username_profile_list,
        },
    )


@login_required(login_url='/signin/')
def profile(request, username: str | None = None):
    from accounts.models import Follow, Profile
    from posts.models import Post

    if not username:
        return redirect(f"/profile/{request.user.username}/")

    try:
        user_object = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('/')

    user_profile, _ = Profile.objects.get_or_create(user=user_object)
    user_posts = Post.objects.filter(author=user_object).order_by('-created_at')
    user_post_length = user_posts.count()

    user_followers = Follow.objects.filter(following=user_object).count()
    user_following = Follow.objects.filter(follower=user_object).count()

    is_following = Follow.objects.filter(follower=request.user, following=user_object).exists()
    button_text = 'Unfollow' if is_following else 'Follow'

    return render(
        request,
        'profile.html',
        {
            'user_object': user_object,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'user_followers': user_followers,
            'user_following': user_following,
            'button_text': button_text,
        },
    )


def logout_view(request):
    logout(request)
    return redirect('/signin/')


@login_required(login_url='/signin/')
def like_post(request):
    """Compatibility endpoint for templates linking to /like-post?post_id=..."""
    from posts.models import Post
    post_id = request.POST.get('post_id') or request.GET.get('post_id')
    if post_id:
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return redirect('home')
        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('home')


@login_required(login_url='/signin/')
@require_http_methods(["POST"])
def follow(request):
    """Toggle follow/unfollow for a target user.

    Templates submit `user` (target username). We always use request.user as follower.
    """
    from accounts.models import Follow

    target_username = (request.POST.get('user') or '').strip()
    if not target_username:
        return redirect('/')

    try:
        target_user = User.objects.get(username=target_username)
    except User.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('/')

    if target_user == request.user:
        return redirect(f"/profile/{request.user.username}/")

    existing = Follow.objects.filter(follower=request.user, following=target_user)
    if existing.exists():
        existing.delete()
    else:
        Follow.objects.create(follower=request.user, following=target_user)

    return redirect(f"/profile/{target_user.username}/")


@login_required(login_url='/signin/')
@require_http_methods(["POST"])
def delete_post(request):
    from posts.models import Post

    post_id = (request.POST.get('post_id') or '').strip()
    if not post_id:
        return redirect('home')

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return redirect('home')

    if post.author_id != request.user.id:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('home')

    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('home')


@login_required(login_url='/signin/')
@require_http_methods(["POST"])
def upload(request):
    """Handle the home feed upload form (template posts to /upload).

    The bundled templates use fields named `image_upload` and `caption`.
    We map those onto the API-backed Post model's `cover_photo` and `body`.
    """
    from posts.models import Post

    # Support both legacy template names and API-ish names.
    image_file = request.FILES.get('cover_photo') or request.FILES.get('image_upload')
    title = (request.POST.get('title') or '').strip()
    body = (request.POST.get('body') or request.POST.get('caption') or '').strip()

    # Keep it permissive: allow text-only posts, but require at least one.
    if not image_file and not body:
        messages.error(request, 'Please add an image or a caption before uploading.')
        return redirect('home')

    # Basic file validation so silent failures are easier to understand.
    if image_file and not (image_file.content_type or '').startswith('image/'):
        messages.error(request, 'Uploaded file must be an image.')
        return redirect('home')

    Post.objects.create(
        author=request.user,
        title=title[:255] or body[:255] or 'Post',
        body=body,
        cover_photo=image_file,
    )
    return redirect('home')


@login_required(login_url='/signin/')
@require_http_methods(["POST"])
def comment_post(request):
    from comments.models import Comment
    from posts.models import Post

    post_id = (request.POST.get('post_id') or '').strip()
    body = (request.POST.get('body') or '').strip()

    if not post_id:
        messages.error(request, 'Missing post id.')
        return redirect('home')

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        messages.error(request, 'Post not found.')
        return redirect('home')

    if not body:
        messages.error(request, 'Comment cannot be empty.')
        return redirect('home')

    Comment.objects.create(post=post, author=request.user, body=body)
    return redirect('home')
