from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm, MessageForm, SkillForm, UpdateProfileForm
from users.models import Profile, Skill
from django.db.models import Q

from users.utils import profiles_paginator, profiles_search

# Create your views here.
def login_user(request):
   page = 'login'
   if request.user.is_authenticated:
      return redirect('users:profiles')
   if request.method == 'POST':
      username = request.POST['username'].lower()
      password = request.POST['password']
      try:
         user = User.objects.get(username=username)
      except:
         messages.error(request,'username does not exist')
         return redirect('users:login')
      user = authenticate(request,username=username,password=password)
      if user is not None:
         login(request,user)
         return redirect(request.GET['next'] if 'next' in request.GET else 'users:account')
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
   search_text, profiles = profiles_search(request) 
   custom_range,profiles = profiles_paginator(request,profiles,6)
   context ={
    'profiles':profiles,
    'search_text':search_text ,
    'custom_range':custom_range
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


@login_required(login_url='users:login')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {'message_requests': message_requests, 'unread_count': unread_count}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='users:login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('users:profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
