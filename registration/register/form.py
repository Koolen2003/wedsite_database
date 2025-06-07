# forms.py
from django import forms
from django.utils import timezone
import datetime
from django.forms import ModelForm
from .models import StudentMarkForm, Teacher, UserProfile
class MyForm(forms.Form):
  
    name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    student_id = forms.IntegerField( required=False)
    cohort = forms.CharField(max_length=100, required=False)
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

class TeacherRegistrationForm(ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Teacher
        fields = ['username', 'password']

from django.contrib.auth.models import User
from django.db import models

class StudentMake(ModelForm):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    student_id = models.IntegerField(max_length=50, unique=True)
    cohort = models.CharField(max_length=50)
    # Add subject fields directly instead of concatenated strings
    computer_architecture = models.FloatField(default=0.0)
    networking = models.FloatField(default=0.0)
    r_programming = models.FloatField(default=0.0)
    class Meta:
        model = StudentMarkForm
        fields = '__all__'
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.name + ' ' + self.last_name





class EditStudentForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    student_id = forms.IntegerField(label='Student ID', disabled=True)  # Make ID uneditable
    cohort = forms.CharField(label='Cohort', max_length=100)
    Computer_Arquitecture = forms.DecimalField(label='Computer Architecture', max_digits=5, decimal_places=2)
    Networking = forms.DecimalField(label='Networking', max_digits=5, decimal_places=2)
    R_Programming = forms.DecimalField(label='R Programming', max_digits=5, decimal_places=2)

    class Meta:
        model = StudentMarkForm
        fields = ['name', 'last_name', 'student_id', 'cohort', 'Computer_Arquitecture', 'Networking', 'R_Programming']

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class TeacherLoginForm(AuthenticationForm):
    user_type = forms.CharField(widget=forms.HiddenInput(), initial='teacher')

