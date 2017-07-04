# _*_ coding: utf-8 _*_

from django.shortcuts import render, redirect
from django.template.context_processors import csrf
# from django.core.context_processors import csrf

from west.models import Character

from django import forms

from django.contrib.auth import *

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.forms import UserCreationForm

def diff_response(request):
    if request.user.is_authenticated():
        content = "<p>my dear user</p>"
    else:
        content = "<p>you wired stranger</p>"
    return HttpResponse(content)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
        return redirect("/")
    else:
        form = UserCreationForm()
        ctx = {'form':form}
        ctx.update(csrf(request))
        return render(request, "register.html",ctx)

def name_check(user):
    return user.get_username() == 'vamei'

@user_passes_test(name_check)
def specific_user(request):
    return HttpResponse("<p>for Vamei only</p>")

@login_required
def user_only(request):
    return HttpResponse("<p>This message is for logged in user only.</p>")

def diff_response(request):
    if request.user.is_authenticated():
        content = "<p>my dear user</p>"
    else:
        content = "<p>you wired stranger</p>"
    return HttpResponse(content)

def user_login(request):
    '''
    login
    '''
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
    ctx = {}
    ctx.update(csrf(request))
    return render(request, 'login.html',ctx)

def user_logout(request):
    '''
    logout
    URL: /users/logout
    '''
    logout(request)
    return redirect('/')

# class CharacterForm(forms.Form):
#    name = forms.CharField(max_length = 200)

def investigate(request):
    if request.POST:
        form = CharacterForm(request.POST)
        if form.is_valid():
            submitted = form.cleaned_data['name']
            new_record = Character(name = submitted)
            new_record.save()
    form = CharacterForm()
    ctx = {}
    ctx.update(csrf(request))
    all_records = Character.objects.all()
    ctx['staff'] = all_records
    ctx['form'] = form
    return render(request, "investigate.html", ctx)

