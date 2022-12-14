from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Message, Profile, Skill

class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','username','email','short_intro',
                  'bio','profile_image','social_github',
                  'social_linkedin','social_twitter','social_youtube',
                  'social_website'
                  ]
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs['class']='input'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','email','username','password1','password2')
        labels = {
            'first_name':'name'
        }
        
    def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            
            for name, field in self.fields.items():
                field.widget.attrs['class']='input'
                
                
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name','description']
    
    def __init__(self,*args, **kwargs):
        super(SkillForm,self).__init__(*args, **kwargs)
        
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'input'
            
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        
    
    