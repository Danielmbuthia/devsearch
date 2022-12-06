from django.contrib import admin
from django.utils.html import format_html

from users.models import Message, Profile,Skill
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    def thumb_nail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius:50px" />'.format(object.profile_image.url))
    
    thumb_nail.short_description = 'Photo'
    list_display = ('username','thumb_nail','name','email','user')
    list_display_links = ['username']
    search_fields= ['username','email']
    list_filter= ['username']
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject','name','email','receiver')
    
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Skill)
admin.site.register(Message,MessageAdmin)