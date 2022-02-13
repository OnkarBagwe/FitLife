
from tkinter import Widget
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
# Create your models here.
class registered_user(models.Model):
    username = models.CharField(max_length=130)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=25)