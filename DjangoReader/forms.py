from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Image, Language


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

        #fields = ['username', 'password1', 'password2']
        fields = [username, password1, password2]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')
