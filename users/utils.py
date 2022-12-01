from users.models import Profile, Skill
from django.db.models import Q


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