from account.models import UserFollowing


def add_variable_to_context(request):
    if request.user.is_authenticated:
        followers = UserFollowing.objects.all().filter(following_user=request.user)
        followings = UserFollowing.objects.all().filter(user=request.user)
        return {'user': request.user, 'followers': followers, 'followings': followings}
    else:
        return {}
