from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Vacante, Empresa


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


class VacanteForm(forms.ModelForm):
    """
    Formulario para crear y editar vacantes de práctica
    """

    class Meta:
        model = Vacante
        fields = [
            'empresa',
            'titulo',
            'area_practica',
            'descripcion',
            'cantidad_cupos',
            'programa_academico',
            'semestre_minimo',
            'habilidades_requeridas',
            'horario',
            'duracion_meses',
            'estado',
        ]

        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Practicante de Desarrollo de Software',
                'required': True
            }),
            'area_practica': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Desarrollo de Software, Marketing Digital, etc.',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe las funciones y responsabilidades del practicante...',
                'required': True
            }),
            'cantidad_cupos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'value': '1',
                'required': True
            }),
            'programa_academico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ingeniería de Sistemas',
                'required': True
            }),
            'semestre_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'value': '6',
                'required': True
            }),
            'habilidades_requeridas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Trabajo en equipo, comunicación efectiva, conocimientos en Python...'
            }),
            'horario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lunes a Viernes 8:00am - 5:00pm',
                'required': True
            }),
            'duracion_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '3',
                'max': '12',
                'value': '6',
                'required': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }

        labels = {
            'empresa': 'Empresa Formadora',
            'titulo': 'Título de la Vacante',
            'area_practica': 'Área de Práctica',
            'descripcion': 'Descripción Detallada',
            'cantidad_cupos': 'Cantidad de Cupos',
            'programa_academico': 'Programa Académico',
            'semestre_minimo': 'Semestre Mínimo',
            'habilidades_requeridas': 'Habilidades Requeridas',
            'horario': 'Horario',
            'duracion_meses': 'Duración (meses)',
            'estado': 'Estado de la Vacante',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo empresas aprobadas
        self.fields['empresa'].queryset = Empresa.objects.filter(estado='APROBADA')

        # Si no hay empresas aprobadas, mostrar mensaje
        if not self.fields['empresa'].queryset.exists():
            self.fields['empresa'].empty_label = "No hay empresas aprobadas disponibles"

    def clean_cantidad_cupos(self):
        cantidad = self.cleaned_data.get('cantidad_cupos')
        if cantidad and cantidad < 1:
            raise forms.ValidationError('Debe haber al menos 1 cupo disponible')
        if cantidad and cantidad > 10:
            raise forms.ValidationError('No se pueden crear más de 10 cupos por vacante')
        return cantidad

    def clean_semestre_minimo(self):
        semestre = self.cleaned_data.get('semestre_minimo')
        if semestre and semestre < 1:
            raise forms.ValidationError('El semestre mínimo debe ser al menos 1')
        if semestre and semestre > 10:
            raise forms.ValidationError('El semestre mínimo no puede ser mayor a 10')
        return semestre

    def clean_duracion_meses(self):
        duracion = self.cleaned_data.get('duracion_meses')
        if duracion and duracion < 3:
            raise forms.ValidationError('La duración mínima debe ser 3 meses')
        if duracion and duracion > 12:
            raise forms.ValidationError('La duración máxima debe ser 12 meses')
        return duracion