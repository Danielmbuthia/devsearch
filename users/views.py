from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from users.forms import CustomUserCreationForm
from users.models import Profile

# Create your views here.
def login_user(request):
   page = 'login'
   if request.user.is_authenticated:
      return redirect('users:profiles')
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      try:
         user = User.objects.get(username=username)
      except:
         messages.error(request,'username does not exist')
         return redirect('users:login')
      user = authenticate(request,username=username,password=password)
      if user is not None:
         login(request,user)
         return redirect('users:profiles')
      else:
         messages.error(request,'Username or password is incorect')
         return redirect('users:login') 
   context = {
      'page':page
   }
         
   return render(request,'users/login_register.html',context)

def logout_user(request):
   logout(request)
   messages.info(request,'User loged out successfully')
   return redirect('users:login')

def register_user(request):
   page ='register'
   form = CustomUserCreationForm()
   if request.method == 'POST':
      form = CustomUserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         print(user.username)
         user.username = user.username.lower()
         user.save()
         login(request,user)
         messages.success(request,'User created successfully')
         return redirect(f'users:profiles')
      else:
         messages.error(request,'An error occurred when registering the user')
         return redirect('users:register')
      
   context = {
      'page':page,
      'form':form
   }
   return render(request,'users/login_register.html',context)

def profiles(request):
    profiles = Profile.objects.all()
    context ={
       'profiles':profiles 
    }
    return render(request,'users/profiles.html',context)

def user_profile(request,pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')
    context ={
       'profile':profile,
       'top_skills':top_skills,
       'other_skills':other_skills
    }
    return render(request,'users/user_profile.html',context)
    