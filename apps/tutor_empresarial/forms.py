from django import forms
from apps.coordinacion.models import TutorEmpresarial


class TutorPerfilForm(forms.ModelForm):
    """Formulario para editar el perfil del tutor empresarial"""

    class Meta:
        model = TutorEmpresarial
        fields = ['nombre_completo', 'cargo', 'email', 'telefono', 'foto_perfil']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo en la empresa'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@empresa.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3001234567'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'nombre_completo': 'Nombre Completo',
            'cargo': 'Cargo',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'foto_perfil': 'Foto de Perfil',
        }

