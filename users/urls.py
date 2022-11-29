
from django.urls import path
from users.views import (
    profiles,
    update_account,
    user_profile,
    login_user,
    logout_user,
    register_user,
    user_account
)


urlpatterns = [
    path('',profiles,name='profiles'),
    path('profile/<str:pk>/',user_profile,name='profile'),
    path('users/login/',login_user,name='login'),
    path('user/logout/',logout_user,name='logout'),
    path('user/register/',register_user,name='register'),
    path('user/account/',user_account,name='account'),
    path('user/edit_account',update_account,name='edit_account'),
]
