from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_recent_posts, name='show_recent_posts'),
    path('create/', views.create, name='create_post'),
    path('show/<int:post_id>/', views.show_post, name='show_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('unlike/<int:post_id>/', views.unlike, name='unlike')
]
