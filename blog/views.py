from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Like
from .forms import PostForm


@login_required
def create(request):
    """
    Creates Post
    :param request:
    :return: render(request, 'blog/create.html', {'form': form})
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Successfully created')
            return redirect('show_post', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """
    Allows User to create post, if User is an Author
    :param request:
    :param post_id:
    :return: render(request, 'blog/edit_post.html', {'form': form, 'user': user})
    """
    user = request.user
    post = Post.objects.get(pk=post_id)
    if user != post.author:
        return HttpResponseForbidden
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_edited = True
            post.save()
            return redirect('show_post', post_id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'user': user})


def show_post(request, post_id):
    """
    Shows Post
    :param request:
    :param post_id:
    :return: render(request, 'blog/show_post.html', {'post': post})
    """
    post = Post.objects.get(pk=post_id)
    return render(request, 'blog/show_post.html', {'post': post})


def show_recent_posts(request):
    """
    Shows all post created, sorted by creation date
    :param request:
    :return: render(request, 'blog/show_recent_posts.html', {'posts': posts})
    """
    posts = Post.objects.get_queryset().order_by('-created_at')
    return render(request, 'blog/show_recent_posts.html', {'posts': posts})


@login_required
def like(request, post_id):
    """
    Allows User to like post if not liked. User must be logged in
    :param request:
    :param post_id:
    :return: redirect('show_post', post_id) or redirect('login')
    """
    user = request.user
    post = Post.objects.get(pk=post_id)
    if user.is_authenticated:
        new_like = Like(user=user, post=post)
        new_like.save()
        post.likes += 1
        post.save()

        return redirect('show_post', post_id)
    else:
        messages.error(request, 'You must be authenticated for liking!')
        return redirect('login')


@login_required
def unlike(request, post_id):
    """
    Allows User to unlike Post if liked by User. User must be logged in.
    :param request:
    :param post_id:
    :return: redirect('show_post', post_id) or redirect('login')
    """
    user = request.user
    post = Post.objects.get(pk=post_id)
    if user.is_authenticated:
        old_like = Like.objects.get(post=post_id, user=user)
        old_like.delete()
        post.likes -= 1
        post.save()
        return redirect('show_post', post_id)
    else:
        messages.error(request, 'You must be authenticated for liking!')
        return redirect('login')
