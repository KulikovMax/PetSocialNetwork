from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('user/', views.UserRetrieveUpdateAPIView.as_view()),
    path('analitycs/<date_from_s>&<date_to_s>/', views.likes_detail)
]