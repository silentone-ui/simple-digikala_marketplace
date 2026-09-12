from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    phone_number = forms.CharField(label="شماره موبایل", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل خود را وارد کنید'}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        password = cleaned_data.get("password")

        if phone_number and password:
            user = User.objects.filter(phone_number=phone_number).first()
            if user is not None and user.check_password(password):
                cleaned_data['user'] = user
            else:
                raise forms.ValidationError("شماره موبایل یا رمز عبور اشتباه است.")
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'phone_number')