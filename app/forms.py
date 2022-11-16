from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactModel



class SignUpForm(UserCreationForm):
    password2=forms.CharField(widget=forms.PasswordInput,label='confirm password(again)')

    class Meta:
        model=User
        fields=['username','first_name','last_name','email']


class Contact(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields= '__all__'
