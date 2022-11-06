from ctypes import resize
from django.contrib.auth import get_user_model
from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm


class PostForm(forms.ModelForm):
    conteudo = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'No que está pensando...',
                'class': 'form-control margin-topo',
            }
        ),
        label='',
    )

    class Meta:
        model = Post
        exclude = ('autor', )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
        ]

    first_name = forms.CharField(
        label='Primeiro nome',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Digite o seu primeiro nome',
                'class': 'form-control'
            }
        )
    )

    last_name = forms.CharField(
        label='Sobrenome',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Digite seu sobrenome',
                'class': 'form-control'
            }
        )
        
    )

    username = forms.CharField(
        label='Usuário',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Digite seu nome de usuário',
                'class': 'form-control',
            }
        )
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Digite sua senha',
                'class': 'form-control',
            }
        )
    )



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class NovaSenhaForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

