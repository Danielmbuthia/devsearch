
from django.urls import path

from .views import create_project, project, projects, update_project,delete_project


urlpatterns = [
    path('',projects,name='projects'),
    path('create/',create_project,name="project_create"),
    path('<str:pk>/',project,name='project'),
    path('update/<str:pk>/',update_project,name="update_project"),
    path('delete/<str:pk>',delete_project,name='delete_project')
]