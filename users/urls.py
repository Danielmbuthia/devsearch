
from django.urls import path
from users.views import (
    profiles,
    user_profile,
    login_user,
    logout_user,
    register_user
)


urlpatterns = [
    path('',profiles,name='profiles'),
    path('profile/<str:pk>',user_profile,name='profile'),
    path('users/login',login_user,name='login'),
    path('user/logout',logout_user,name='logout'),
    path('user/register',register_user,name='register')
]
