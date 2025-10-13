from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ManejoUsuario

class FormularioRegistro(UserCreationForm):
    class Meta: 
        model = ManejoUsuario
        fields = [
            'username',
            'email', 
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico', 
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña'
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ej: maria.garcia'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ej: maria@cafeteria.co'}), 
            'first_name': forms.TextInput(attrs={'placeholder': 'Tus nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Tus apellidos'}), 
        }
