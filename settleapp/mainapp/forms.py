from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.conf import settings
#from accounts.validators import validate_password_digit, validate_password_uppercase,validate_pass


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

  