from django.http import HttpResponse
from django.shortcuts import redirect, render

from projects.forms import ProjectForm
from projects.models import Project

# Create your views here.

def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    context ={
        'projects':projects
    }
    return render(request,'projects/projects.html',context)

def project(request,pk):
    project = Project.objects.get(id=pk)
    context ={
        'projectObj':project
    }
    return render(request,'projects/project_view.html',context)

def create_project(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES) 
        if form.is_valid():
            form.save()
            return redirect("projects:projects")
    context ={
        "form":form
    }
    return render(request,'projects/projects_create.html',context)

def update_project(request,pk):
    project = Project.objects.get(id=pk)
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