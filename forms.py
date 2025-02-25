from django import forms
from django.contrib.auth.hashers import make_password
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'password', 'address', 'email', 'phono']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
        }
        labels = {
            'username': 'Username',
            'password': 'Password',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password']) 
        if commit:
            instance.save() 
        return instance


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'password', 'address', 'email', 'phono']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'phono': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
