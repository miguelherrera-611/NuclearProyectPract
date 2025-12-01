"""
Formularios para el módulo de Docente Asesor
"""
from django import forms
from coordinacion.models import DocenteAsesor


class DocenteAsesorPerfilForm(forms.ModelForm):
    """Formulario para editar el perfil del docente asesor"""

    class Meta:
        model = DocenteAsesor
        fields = ['nombre_completo', 'email', 'telefono', 'especialidad', 'foto_perfil']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3001234567'
            }),
            'especialidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ingeniería de Software, Gestión Empresarial'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'nombre_completo': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'especialidad': 'Especialidad',
            'foto_perfil': 'Foto de Perfil',
        }

