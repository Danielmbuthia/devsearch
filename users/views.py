from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm, SkillForm, UpdateProfileForm
from users.models import Profile, Skill

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
         user.username = user.username.lower()
         user.save()
         login(request,user)
         messages.success(request,'User created successfully')
         return redirect(f'users:edit_account')
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
    
@login_required(login_url='users:login')   
def user_account(request):
   profile = request.user.profile
   skills = profile.skill_set.all()
   projects = profile.project_set.all()
   context ={
      'profile':profile,
      'skills':skills,
      'projects':projects
    }
   return render(request,'users/account.html',context)

@login_required(login_url='users:login') 
def update_account(request):
   profile = request.user.profile 
   form = UpdateProfileForm(instance=profile)
   if request.method == 'POST':
      form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
      if form.is_valid():
         form.save()
         messages.success(request,'Account updated successfully')
         return redirect('users:account')
   context = {
      'form':form
   }
   return render(request,'users/profile_form.html',context)

@login_required(login_url='users:login') 
def create_skill(request):
   form = SkillForm()
   profile = request.user.profile 
   if request.method == 'POST':
      form = SkillForm(request.POST)
      # name = request.POST['name']
      # skill_exist = Skill.objects.get(name__contains=name)
      # if skill_exist:
      #    messages.error(request,'Skill exists')
      #    return redirect('users:create_skill')
      if form.is_valid():
         skill = form.save(commit=False)
         skill.owner =profile
         skill.save()
         messages.success(request,'Skill added successfully')
         return redirect('users:account')
   context ={
      'form':form
   }
   return render(request,'users/skill_form.html',context)


@login_required(login_url='users:login') 
def update_skill(request,pk):
   profile = request.user.profile 
   skill = profile.skill_set.get(pk=pk)
   form = SkillForm(instance=skill)
   if request.method == 'POST':
      form = SkillForm(request.POST,instance=skill)
      if form.is_valid():
         form.save()
         messages.success(request,'Skill edited successfully')
         return redirect('users:account')
   context ={
      'form':form
   }
   return render(request,'users/skill_form.html',context)

@login_required(login_url='users:login') 
def delete_skill(request,pk):
   profile = request.user.profile 
   skill = profile.skill_set.get(pk=pk)
   if request.method == 'POST':
      skill.delete()
      messages.success(request,'skill deleted succesfully')
      return redirect('users:account')
   context ={
      'object':skill
   }
   return render(request,'projects/delete_template.html',context)