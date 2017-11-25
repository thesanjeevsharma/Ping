from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import PostForm, CommentForm, UserForm
from .models import Post, Comment, User

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')

def dashboard(request):
    if not request.user.is_authenticated():
        return render(request, 'dashboard/index.html')
    else:
        posts = Post.objects.all().order_by('-time')
        user = request.user
        query = request.GET.get("data")
        if query:
            posts = posts.filter(
                Q(post_by__icontains=query)
            ).distinct()
            return render(request, 'dashboard/dashboard.html', {
                'posts': posts,
                'user': user,
            })
        else:
            return render(request, 'dashboard/dashboard.html', {'posts': posts, 'user': user})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.all().order_by('-time')
                comments = Comment.objects.all()
                user = request.user
                return render(request, 'dashboard/dashboard.html', {'posts': posts, 'comments': comments, 'user': user})
            else:
                return render(request, 'dashboard/index.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'dashboard/index.html', {'error_message': 'Invalid login'})
    return render(request, 'dashboard/index.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'dashboard/index.html', context)

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.all()
                return render(request, 'dashboard/dashboard.html', {'posts': posts})
    context = {
        "form": form,
    }
    return render(request, 'dashboard/register.html', context)

def post(request):
    if not request.user.is_authenticated():
        return render(request, 'dashboard/index.html')
    else:
        form = PostForm(request.POST or None, request.FILES or None)
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.post_by = request.user
            post.post_pic = request.FILES['post_pic']
            file_type = post.post_pic.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'user': user,
                    'post': post,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'dashboard/post.html', context)
            post.save()
            posts = Post.objects.all().reverse()
            return render(request, 'dashboard/dashboard.html', {'posts': posts})
        context = {
            "form": form,
        }
        return render(request, 'dashboard/post.html', context)

def profile_page(request):
    if not request.user.is_authenticated():
        return render(request, 'dashboard/index.html')
    else:
        user = request.user
        post_number = Post.objects.filter(post_by=request.user).count()
        posts = Post.objects.filter(post_by=request.user)
        if post_number == 0:
            post_message = 'You have no posts! Please add some.'
        else:
            post_message = 'You have total ' + str(post_number) + ' post(s).'
        context = {'user': user, 'post_message': post_message, 'posts': posts}
        return render(request, 'dashboard/profile_page.html', context)

def settings(request):
    if not request.user.is_authenticated():
        return render(request, 'dashboard/index.html')
    else:
        #yet to be added
        return render(request, 'dashboard/dashboard.html')

def saved(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.saved:
        post.saved = False
    else:
        post.saved = True
    post.save()
    posts = Post.objects.all()
    comments = Comment.objects.all()
    context = {
        'posts': posts,
        'comments': comments,
    }
    return render(request, 'dashboard/dashboard.html', context)

def comment(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'dashboard/index.html')
    else:
        post = get_object_or_404(Post, pk=post_id)
        comments = Comment.objects.filter(post=post)
        return render(request, 'dashboard/comment.html', {'post': post, 'comments': comments})





