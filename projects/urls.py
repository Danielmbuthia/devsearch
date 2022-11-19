
from django.urls import path

from .views import create_project, project, projects, update_project


urlpatterns = [
    path('',projects,name='projects'),
    path('project/<str:pk>/',project,name='project'),
    path('project/create',create_project,name="create_project"),
    path('project/update/<str:pk>',update_project,name="update_project"),
]