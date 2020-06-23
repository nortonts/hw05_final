from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10) 
    page_number = request.GET.get('page')  
    page = paginator.get_page(page_number) 
    return render(
                  request,
                  'index.html',
                  {'page': page, 'paginator': paginator}
                 )

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')  
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page, 
                                          'paginator': paginator})    

@login_required
def new_post(request): 
    is_edit = False
    form = PostForm(request.POST) 
    if request.method == 'POST' and form.is_valid(): 
        new = form.save(commit=False) 
        new.author_id = request.user.id 
        new.save() 
        return redirect('index') 
    return render(request, 'new.html', {'form': form, 'is_edit': is_edit}) 

def profile(request, username):
    user_name = get_object_or_404(User, username=username)
    user_posts = user_name.posts.all()
    posts_quan = user_posts.count()
    paginator = Paginator(user_posts, 10) 
    page_number = request.GET.get('page')  
    page = paginator.get_page(page_number) 
    return render(request, 'profile.html', {'page': page, 
                                            'paginator': paginator,
                                            'user_name': user_name, 
                                            'posts_quan': posts_quan})
 
 
def post_view(request, username, post_id):
        post = get_object_or_404(Post, id=post_id, author__username=username)
        user_name =  post.author
        posts_quan = post.author.posts.all().count()
        return render(request, 'post_view.html', {'post': post,
                                             'posts_quan': posts_quan,
                                             'user_name': user_name})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    if request.user != post.author:
        return redirect('post_view', username=username, post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_view', username=username, post_id=post_id)
    return render(request, 'new.html', {'form': form, 'post': post, 'is_edit': True})