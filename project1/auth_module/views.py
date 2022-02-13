from cmath import log
from django.contrib import messages
from django.shortcuts import redirect
from distutils.log import Log
from django.shortcuts import render
from django.views.generic import UpdateView
from forms import register_user_form, login_user_form
#from auth_module.models import registered_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.http import *
from django.contrib.auth.models import User

# Create your views here.
class register_user_form_view(UpdateView):
    model = User
    form = register_user_form
    template_name = 'register.html'

# def register(request):
#     print("one")
#     # return render(request, 'register.html')
#     return render(request, 'register.html', {'form': register_user_form})

def register(request):
    if request.method == 'POST':
        form = register_user_form(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request,'Email already exists')
            else:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect('home')

    else:
        form = register_user_form()
    return render(request, 'register.html', {'form': form})


def home(request):
    if request.user.is_authenticated :
        return render(request,'home.html')

def login_user(request):
    #logout(request)
    username = password = ''
    if request.method == 'POST':
        form = login_user_form(request.POST)
        #print("First")
        username = request.POST['username']
        #print(username)
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        #print(user)
        if user is not None:
            print("Hello")
            if user.is_active:
                login(request, user)
                return redirect('home')
    else:
        #print("Arya")
        form = login_user_form()
    return render(request, 'login.html')