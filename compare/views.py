#-*- coding: utf-8 -*-
from compare.forms import ProfileForm
from compare.models import Profile
from django.shortcuts import render
# import file for copying from file to profile
from django.core.files import File

#my attempt at importing
from .modules import tom_evaluator

from django.db import models
from django.template import RequestContext, Template

def SaveProfile(request):
   saved = False
   
   if request.method == "POST":
      #Get the posted form
      MyProfileForm = ProfileForm(request.POST, request.FILES)
      
      if MyProfileForm.is_valid():

         profile = Profile()
         #profile.name = MyProfileForm.cleaned_data["name"]
         profile.picture = MyProfileForm.cleaned_data["picture"]
#         profile.save()
         profile.resize()
         # Whenever ImageField is saved, a new copy of the file is created from POSTed data
         profile.save()

         #profile.picture.url gets the url of the web server
         #profile.picture.url gets the absolute path
         is_tom = tom_evaluator.compare(profile.picture.path)
         profile.is_tom = is_tom
         #profile.save()
         # update fields breaks the abilty to use "profile.picture.url" in template (removes /media from url)
         profile.save(update_fields=['is_tom'])

         saved = True
   else:
      print(MyProfileForm.errors)
      MyProfileForm = Profileform()
		
   return render(request, 'saved.html', locals())
   #return render(request, 'saved.html', { "input_image": input })

def index(request):
    last_six = Profile.objects.order_by('-id')[:8]
    return render(request, 'index.html', locals())

def about(request):
    return render(request, 'about.html', locals())
    
