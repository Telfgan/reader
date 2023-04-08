import base64
import os
import uuid
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from pyexpat.errors import messages

from djangoProject2.users import RegisterForm
from .forms import ImageForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from .models import Language
from .services.extractor import extract
from .services.helper import fromBase64, toBase64
from .services.translator import translator, translate


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('upload')
                else:
                    return redirect('Disabled account')
            else:
                return HttpResponseNotFound()
    else:
        form = LoginForm()
    return render(request, 'DjangoReader/login.html', {'form': form})


@login_required(login_url="auth")
def image_upload_view(request):
    """Process images uploaded by users"""
    query_results = Language.objects.all()
    form = ImageForm()
    if request.method == 'GET':
        form = ImageForm(request.POST, request.FILES)
        return render(request, 'DjangoReader/index.html',{'form': form, 'query_results': query_results})
    # language = Language.objects.create(name="russian")
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        selected_option = request.POST.get('language', None)
        origin_language_name = request.POST.get('origin_language_name', None)
        translating_language_name = request.POST.get('translating_language_name', None)
        trancate_language = origin_language_name[:3]
        if form.is_valid():
            dir2 = os.path.abspath(__file__)
            dir3 = f'{Path(dir2).parent}/image'
            dir4 = f'{dir3}/{Path(request.FILES["image"].name)}'
            with open(dir4, 'wb') as f:
                f.write(request.FILES['image'].file.read())

            form.save()

            ext = extract(dir4, trancate_language)
            trans = translate(ext, origin_language_name, translating_language_name)


            img_obj = form.instance
            return render(request, 'DjangoReader/read.html', {'form': form, 'img_obj': img_obj, 'translated': fromBase64(trans)})

    return render(request, 'DjangoReader/index.html', {'form': form, 'query_results': query_results})


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("upload")
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'DjangoReader/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # LoginForm(request, user)
            return redirect('home')
        else:
            return render(request, 'DjangoReader/register.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'DjangoReader/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(
                    request, f'Hi {username.title()}, welcome back!')
                return redirect('home')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'DjangoReader/login.html', {'form': form})


def about(request):
    return render(request, "DjangoReader/index.html")
