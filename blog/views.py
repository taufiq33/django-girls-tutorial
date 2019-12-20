from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm
from django.utils import timezone

# Create your views here.


def post_list(request):
    context = {
        'post_list': Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    context = {
        'post': get_object_or_404(Post, id=pk),
    }
    if request.user.is_authenticated:
        context['comment_form'] = CommentForm(
            initial={
                "author": "{} [admin]".format(request.user)
            }
        )
    else:
        if context['post'].published_date == None :
            return redirect('login')
        context['comment_form'] = CommentForm()
    
    return render(request, 'blog/post_detail.html', context)


def post_add_comment(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, id=pk)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
        return redirect('post_detail', pk=post.pk)
        


@login_required
def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        context = {
            'form': PostForm,
        }
    return render(request, 'blog/post_add.html', context)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        context = {
            'form': PostForm(instance=post),
        }

    return render(request, 'blog/post_edit.html', context)


@login_required
def post_draft(request):
    draft_posts = Post.objects.filter(published_date__isnull=True)
    context = {
        "draft_posts": draft_posts
    }

    return render(request, 'blog/post_draft.html', context)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.published_date = timezone.now()
    post.author = request.user
    post.save()
    return redirect('post_list')


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('post_list')
