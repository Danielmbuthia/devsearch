from users.models import Profile, Skill
from django.db.models import Q

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def profiles_paginator(request,profiles,result):
    page = request.GET.get('page')
    paginator = Paginator(profiles,result)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    left_index = (int(page) - 4)
    if left_index < 1:
        left_index =1
        
    right_index = (int(page) + 5)
    if right_index > paginator.num_pages +1:
        right_index = paginator.num_pages
    
    custom_range = (left_index,right_index)
    
    
    return custom_range,profiles
 
def profiles_search(request):
    search_text =""
    if request.GET.get('search_text'):
      search_text = request.GET.get('search_text')
   
    skills = Skill.objects.filter(
       name__icontains = search_text
    )
    profiles = Profile.objects.distinct().filter(
       Q(name__icontains = search_text) |
       Q (short_intro__icontains =search_text) |
       Q (skill__in = skills)
    )  
    
    return search_text, profiles