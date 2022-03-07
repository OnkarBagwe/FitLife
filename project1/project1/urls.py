"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auth_module import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register, name="register"),
    path('home/', views.home, name="home"),
    path('', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),

    path('yoga_home/', views.yoga_home, name="yoga_home"),
    path('gym_home/', views.gym_home, name="gym_home"),

    path('plank/', views.plank_view, name="plank"),
    path('bird_dog/', views.bird_dog_view, name="bird_dog"),

    path('urdhavahastasana/', views.urdhavahastasana_view, name="urdhavahastasana"),
    path('veerbhadrasana/', views.veerbhadrasana_view, name="veerbhadrasana"),
    path('temp/', views.temp_view, name="temp")
    # path('video_feed/', views.video_feed, name='video_feed')
]
