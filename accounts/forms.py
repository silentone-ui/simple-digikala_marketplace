from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import User 


class LoginForm(AuthenticationForm):
   
    username = forms.CharField(label="شماره موبایل", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('first_name','last_name','email')