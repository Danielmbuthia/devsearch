from projects.models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def project_paginator(request,projects,result):
    page = request.GET.get('page')
    paginator = Paginator(projects,result)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    
    left_index = (int(page) - 4)
    if left_index < 1:
        left_index =1
        
    right_index = (int(page) + 5)
    if right_index > paginator.num_pages +1:
        right_index = paginator.num_pages
    
    custom_range = (left_index,right_index)
    
    
    return custom_range,projects
    
def project_search(request):
    search_text =''
    if request.GET.get('search_text'):
        search_text = request.GET.get('search_text')
    tags = Tag.objects.filter(
        name__icontains= search_text
    )
    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_text) |
        Q(description__icontains = search_text) |
        Q(owner__name__icontains = search_text) |
        Q(tags__in = tags)
    )
    
    return search_text, projects
