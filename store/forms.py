# store/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomeUSer

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact = forms.CharField(max_length=15)
    address = forms.CharField(max_length=255)

    class Meta:
        model = CustomeUSer
        fields = ['username', 'email', 'contact', 'address', 'password1', 'password2']
