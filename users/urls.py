
from django.urls import path
from users.views import (
    create_skill,
    create_message,
    delete_skill,
    inbox,
    profiles,
    update_account,
    update_skill,
    user_profile,
    login_user,
    logout_user,
    register_user,
    user_account,
    view_message
)


urlpatterns = [
    path('',profiles,name='profiles'),
    path('profile/<str:pk>/',user_profile,name='profile'),
    path('users/login/',login_user,name='login'),
    path('user/logout/',logout_user,name='logout'),
    path('user/register/',register_user,name='register'),
    path('user/account/',user_account,name='account'),
    path('user/edit_account',update_account,name='edit_account'),
    
    #skills crud
    path('skill/create/',create_skill,name='create_skill'),
    path('skill/edit/<str:pk>/',update_skill,name='edit_skill'),
    path('skill/delete/<str:pk>',delete_skill,name='delete_skill'),
    
    #messages
    path('inbox/', inbox, name="inbox"),
    path('message/<str:pk>/', view_message, name="message"),
    path('create_message/<str:pk>/', create_message, name="send_message"),
]
