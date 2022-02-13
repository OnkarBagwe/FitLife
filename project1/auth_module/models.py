
from tkinter import Widget
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.
"""class registered_user(models.Model):
    username = models.CharField(max_length=130)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=25)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []"""


"""class registered_user(AbstractBaseUser):
    username = CharField(max_length=130)
    email = EmailField(blank=True)
    password = CharField(max_length=25)
    #USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []"""

