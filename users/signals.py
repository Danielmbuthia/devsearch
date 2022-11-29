from .models import Profile
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            name=user.first_name,
            username = user.username,
            email= user.email
        )
        
def delete_user(sender,instance,**kwargs):
    profile = instance
    profile.user.delete()
 
@receiver(post_save,sender=Profile)   
def update_profile(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name=profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()     
    
#post_save.connect(create_profile,sender=User)
post_delete.connect(delete_user,sender=Profile)

