from django.db import models
from django.contrib.auth.models import User
from django import forms
import datetime

from django.db import models
from django.utils import timezone

# Models
def get_default_user():
    return User.objects.first().id  # Assign the first user in DB

class StudentMarkForm(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    student_id = models.IntegerField( unique=True,primary_key=True)
    cohort = models.CharField(max_length=50)
    Computer_Arquitecture = models.FloatField(default=False)
    Networking = models.FloatField(default=False)
    R_Programming = models.FloatField(default=False)    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.name + ' ' + self.last_name

from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default='default_password') 
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    # Ensure there are no redundant fields like `username` or `password` here

  

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Placeholder for user profile extension


# Forms
class StudentForm(forms.ModelForm):  # Renamed from Student to StudentForm
    class Meta:
        model = StudentMarkForm
        fields = ['name', 'last_name', 'student_id', 'cohort', 'Networking', 'R_Programming', 'Computer_Arquitecture']
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    

    