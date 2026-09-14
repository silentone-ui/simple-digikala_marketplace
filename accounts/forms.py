import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

PHONE_RE = re.compile(r'^09\d{9}$')


class LoginForm(forms.Form):
    phone_number = forms.CharField(label="شماره موبایل", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned = super().clean()
        phone = cleaned.get('phone_number')
        password = cleaned.get('password')
        if phone and password:
            user = User.objects.filter(phone_number=phone).first()
            if user and user.check_password(password) and user.is_active:
                cleaned['user'] = user
            else:
                raise forms.ValidationError("شماره موبایل یا رمز عبور اشتباه است.")
        return cleaned

    def get_user(self):
        return self.cleaned_data.get('user')


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'phone_number')

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not PHONE_RE.match(phone):
            raise forms.ValidationError("شماره موبایل معتبر نیست (مثال: 09123456789).")
        return phone