from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CoordinadorLoginForm(AuthenticationForm):
    """
    Formulario personalizado de login para Coordinador Empresarial
    """
    username = forms.CharField(
        label='Usuario',
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autofocus': True
        })
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña'
        })
    )