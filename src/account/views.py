from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from asgiref.sync import sync_to_async

import django.contrib.auth as auth

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from common.django_utils import arender, alogout
from .models import CustomUser
from common.auth import aanonymous_required
from django.contrib.auth.decorators import login_required


@aanonymous_required
async def home(request:HttpRequest) -> HttpResponse:
   return render (request, 'account/home.html')

@aanonymous_required
async def register(request:HttpRequest) -> HttpResponse:
   if request.method == 'POST':
       form = CustomUserCreationForm(request.POST)
       if await form.ais_valid():
           await form.asave()
           return redirect ('login') 
   else:
       form = CustomUserCreationForm()
       
   context = {'register_form': form}
   return await arender (request, 'account/register.html', context)
    
@aanonymous_required
async def login(request:HttpRequest) -> HttpResponse:
   if request.method == 'POST':
      form = CustomAuthenticationForm(request.POST, data = request.POST)
      if await form.ais_valid():
         email = request.POST['username']
         passwd = request.POST['password']
         user: CustomUser | None = await sync_to_async(auth.authenticate)(
                                 request, 
                                 email=email, 
                                 password=passwd,
         )
         
         if user:
            await sync_to_async(auth.login)(request, user)
            return redirect(
               'writer-dashboard' if user.is_writer else 'client-dashboard'
            )
   else:
      form = CustomAuthenticationForm()
            
   context = {'login_form': form}
   return await arender (request, 'account/login.html', context)

@login_required(login_url='login')
async def logout(request: HttpRequest)-> HttpResponse:
   await alogout(request)
   return redirect('/')