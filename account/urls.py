import django.contrib.auth
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('logout-then-login/', auth_views.logout_then_login, name='logout'),
    path('', views.edit, name='dashboard'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-password-done/', views.change_password_done, name='change_password_done'),
    path('sign_up/', views.sign_up, name='sign_up'),
    # path('edit/', views.edit, name='edit'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html',
                                                                 email_template_name='account/password_reset_email.html',
                                                                 success_url=reverse_lazy('password_reset_done')
                                                                 ),
         name='password_reset'),
    path('reset-password/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html',
                                                     success_url=reverse_lazy('password_reset_complete')),
         name='password_reset_confirm',
         ),
    path('reset-password/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
]
