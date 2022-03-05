from cmath import log
import time
import bird_dog
import plank
import Urdhvahastasana
import Veerbhadrasana
import sys 
import threading
from django.contrib import messages
from django.shortcuts import redirect
from distutils.log import Log
from django.shortcuts import render
from django.views.generic import UpdateView
from forms import register_user_form, login_user_form
#from auth_module.models import registered_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.http import *
from django.contrib.auth.models import User
import cv2
from django.http.response import StreamingHttpResponse
from auth_module.camera import VideoCamera

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

def logout_user(request):
    if request.user.is_authenticated :
        django_logout(request)
        return redirect('login_user')
    else:
        return redirect('home')


def gym_home(request):
    if request.user.is_authenticated:
        return render(request, 'gym_home.html')
    else:
        return redirect('login_user')

def yoga_home(request):
    if request.user.is_authenticated:
        return render(request, 'yoga_home.html')
    else:
        return redirect('login_user')

# gym exercises

def plank_view(request):
    if request.user.is_authenticated:
        plank.execute()
        return render(request, 'plank.html')
    else:
        return redirect('login_user')

def bird_dog_view(request):
    if request.user.is_authenticated:
        bird_dog.execute()
        """if(bird_dog.close == True):
            sys.exit(bird_dog.execute())"""
        #cv2.imshow("Bird_Dog",bird_dog_test.image1)
        return render(request, 'bird_dog.html')
    else:
        return redirect('login_user')

def urdhavahastasana_view(request):
    if request.user.is_authenticated:
        Urdhvahastasana.execute()
        #cv2.imshow("Bird_Dog",bird_dog_test.image1)
        return render(request, 'urdhavahastasana.html')
    else:
        return redirect('login_user')



def veerbhadrasana_view(request):
    if request.user.is_authenticated:
        Veerbhadrasana.execute()
        #cv2.imshow("Bird_Dog",bird_dog_test.image1)
        return render(request, 'veerbhadrasana.html')
    else:
        return redirect('login_user')

"""def gen(camera):
	# while True:
	# 	frame = camera.get_frame()
	# 	yield (b'--frame\r\n'
	# 			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # tq= threading.Thread(target=VideoCamera.quadrupule)
    # tgf=threading.Thread(target=VideoCamera.get_frame)
    # te=threading.Thread(target=VideoCamera.extend)
  
    for i in range(1,500):
        frame= camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

    for i in range(1,500):
        frame= VideoCamera.quadrupule()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
       

    # # for i in range (1,20):
    # #     print(i)
    # #     if i==1:
    # #         tgf.start()

    # #     if i==15: 
    # #         tq.start()
    # #     time.sleep(1)

    # # frame = camera.execute()
    # # yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')"""
