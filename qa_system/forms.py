from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'logininput', 'placeholder': '请输入姓名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'logininput', 'placeholder': '请输入密码'}))
    email = forms.EmailField(required=True)
    verification_code = forms.CharField(
        required=False,
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'logininput', 'placeholder': '请输入验证码'}),
        label='验证码'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['verification_code'].required = False



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']



class AvatarForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']

class NicknameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nickname']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'})
        }

class PhoneForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'})
        }

class EmailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

class SignatureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['signature']
        widgets = {
            'signature': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }