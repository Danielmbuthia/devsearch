
from django.urls import path
from users.views import profiles,user_profile


urlpatterns = [
    path('',profiles,name='profiles'),
    path('profile/<str:pk>',user_profile,name='profile')
]
