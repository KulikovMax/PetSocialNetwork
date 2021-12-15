from django.contrib import messages
from django.shortcuts import render, redirect
from account.views import update_profile_lr
from account.models import UserFollowing, User
from blog.models import Post
from .forms import SearchForm


def index(request):
    """
    Shows main page of the site. If User is logged in, template will render his/her followers/posts
    :param request:
    :return: return render(request, 'network/index.html', {'user': request.user, 'posts': posts}) or return redirect('login')
    """
    update_profile_lr(request)
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by('-created_at')
        return render(request, 'network/index.html', {'user': request.user, 'posts': posts})
    else:
        return redirect('login')


def search(request):
    """
    Renders template with SearchForm.
    Allows User to search for other Users.
    :param request:
    :return: render(request, 'network/search_form.html', {'form': form}) or render(request, 'network/search_results.html', {'users': users})
    """
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            users = User.objects.all().filter(username__icontains=username, first_name__icontains=first_name,
                                              last_name__icontains=last_name)
            return render(request, 'network/search_results.html', {'users': users})

    else:
        form = SearchForm()
    return render(request, 'network/search_form.html', {'form': form})


def user_page(request, user_id):
    """
    Renders template with other User (founded by search) info.
    :param request:
    :param user_id:
    :return:
    """
    target_user = User.objects.get(pk=user_id)
    request_user = request.user
    posts = Post.objects.all().filter(author=target_user)
    target_followers = [x.return_user() for x in UserFollowing.objects.all().filter(following_user=target_user)]
    target_followings = [x.return_user() for x in UserFollowing.objects.all().filter(user=target_user)]
    return render(request, 'network/user_page.html',
                  {'target_user': target_user, 'requset_user': request_user, 'posts': posts,
                   't_followers': target_followers,
                   't_followings': target_followings})


def follow(request, user_id):
    """
    Allows User to follow other User if not followed.
    :param request:
    :param user_id:
    :return: return redirect('user_page', user_id)
    """
    if request.user.is_authenticated:
        new_follow = UserFollowing(user=request.user, following_user=User.objects.get(pk=user_id))
        new_follow.save()
    else:
        messages.error(request, 'You should be logged in!')
    return redirect('user_page', user_id)


def unfollow(request, user_id):
    """
    Allows User to follow other User if followed.
    :param request:
    :param user_id:
    :return: return redirect('user_page', user_id)
    """
    if request.user.is_authenticated:
        old_follow = UserFollowing.objects.get(user=request.user, following_user=User.objects.get(pk=user_id))
        old_follow.delete()
    else:
        messages.error(request, 'You should be logged in!')
    return redirect('user_page', user_id)


def show_followings(request):
    """
    Shows User subscriptions.
    :param request:
    :return: render(request, 'network/followings.html')
    """
    return render(request, 'network/followings.html')


def show_followers(request):
    """
    Shows User followers
    :param request:
    :return: render(request, 'network/followers.html')
    """
    return render(request, 'network/followers.html')
