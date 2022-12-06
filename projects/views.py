from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from projects.forms import ProjectForm
from projects.models import Project

from django.contrib import messages

from projects.utils import project_paginator, project_search

# Create your views here.

def projects(request):
    search_text, projects = project_search(request)
    custom_range,projects = project_paginator(request,projects,6)
  
    context ={
        'projects':projects,
        'search_text':search_text,
        'custom_range':custom_range
    }
    return render(request,'projects/projects.html',context)

def project(request,pk):
    project = Project.objects.get(id=pk)
    context ={
        'projectObj':project
    }
    return render(request,'projects/project_view.html',context)

@login_required(login_url='users:login')
def create_project(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES) 
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile # logged in user
            project.save()
            return redirect("projects:projects")
    context ={
        "form":form
    }
    return render(request,'projects/projects_create.html',context)

@login_required(login_url='users:login')
def update_project(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES,instance=project) 
        if form.is_valid():
            form.save()
            return redirect("projects:projects")
    context ={
        "form":form
    }
    return render(request,'projects/projects_create.html',context)


@login_required(login_url='users:login')
def delete_project(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request,'project deleted succesfully')
        return redirect('projects:projects')
    context ={
        'object':project
    }
    return render(request,'projects/delete_template.html',context)
        