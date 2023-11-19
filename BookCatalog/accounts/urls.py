# urls.py
from django.urls import path
from accounts.views import CustomUserLoginView, CustomUserLogoutView, CustomUserRegisterView


urlpatterns = [
    path('register/', CustomUserRegisterView.as_view(), name='register'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('logout/', CustomUserLogoutView.as_view(), name='logout'),
]
