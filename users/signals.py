from .models import Profile
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.first_name,
            username = user.username,
            email= user.email
        )
        
def delete_user(sender,instance,**kwargs):
    profile = instance
    profile.user.delete()
    
#post_save.connect(create_profile,sender=User)
post_delete.connect(delete_user,sender=Profile)

