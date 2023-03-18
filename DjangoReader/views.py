from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from pyexpat.errors import messages

from djangoProject2.users import RegisterForm
from .forms import ImageForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from .models import Language


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
    return render(request, 'account/login.html', {'form': form})


@login_required(login_url="auth")
def image_upload_view(request):
    """Process images uploaded by users"""
    query_results = Language.objects.all()
    # language = Language.objects.create(name="russian")
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        selected_option = request.POST.get('language', None)
        if form.is_valid():
            # a = request.data.get("language")
            # request.data.get("language")
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'account/index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'account/index.html', {'form': form, 'query_results': query_results})


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
        return render(request, 'account/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # LoginForm(request, user)
            return redirect('home')
        else:
            return render(request, 'account/register.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

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
        return render(request, 'account/login.html', {'form': form})


def about(request):
    return render(request, "account/index.html")
