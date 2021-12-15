from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('user/<int:user_id>', views.user_page, name='user_page'),
    path('follow/<int:user_id>', views.follow, name='follow'),
    path('unfollow/<int:user_id>', views.unfollow, name='unfollow'),
    path('followings/', views.show_followings, name='followings'),
    path('followers/', views.show_followers, name='followers'),
]
