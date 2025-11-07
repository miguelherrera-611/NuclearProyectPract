from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Vacante, Empresa, Postulacion, Estudiante
from datetime import date, timedelta


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


class PostulacionForm(forms.ModelForm):
    """
    Formulario para postular estudiantes a vacantes de práctica (RF-03)
    """

    class Meta:
        model = Postulacion
        fields = [
            'vacante',
            'estudiante',
            'observaciones',
        ]

        widgets = {
            'vacante': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'id_vacante'
            }),
            'estudiante': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'id_estudiante'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones adicionales sobre el estudiante y su idoneidad para esta vacante...',
            }),
        }

        labels = {
            'vacante': 'Vacante de Práctica',
            'estudiante': 'Estudiante a Postular',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar solo vacantes disponibles con cupos libres
        self.fields['vacante'].queryset = Vacante.objects.filter(
            estado='DISPONIBLE'
        ).select_related('empresa')

        # Filtrar solo estudiantes aptos para postular
        self.fields['estudiante'].queryset = Estudiante.objects.filter(
            estado='APTO'
        ).order_by('nombre_completo')

        # Mensajes si no hay opciones disponibles
        if not self.fields['vacante'].queryset.exists():
            self.fields['vacante'].empty_label = "No hay vacantes disponibles"

        if not self.fields['estudiante'].queryset.exists():
            self.fields['estudiante'].empty_label = "No hay estudiantes aptos"

        # Personalizar la visualización de las opciones
        self.fields['vacante'].label_from_instance = self._vacante_label
        self.fields['estudiante'].label_from_instance = self._estudiante_label

    def _vacante_label(self, obj):
        """Personalizar cómo se muestra cada vacante en el select"""
        cupos_disponibles = obj.cantidad_cupos - obj.cupos_ocupados
        return f"{obj.titulo} - {obj.empresa.razon_social} ({cupos_disponibles} cupos disponibles)"

    def _estudiante_label(self, obj):
        """Personalizar cómo se muestra cada estudiante en el select"""
        return f"{obj.codigo} - {obj.nombre_completo} ({obj.programa_academico} - {obj.semestre}° sem)"

    def clean(self):
        cleaned_data = super().clean()
        vacante = cleaned_data.get('vacante')
        estudiante = cleaned_data.get('estudiante')

        if vacante and estudiante:
            # VALIDACIÓN 1: Verificar que el estudiante no esté ya postulado a esta vacante
            postulacion_existente = Postulacion.objects.filter(
                vacante=vacante,
                estudiante=estudiante
            ).exists()

            if postulacion_existente:
                raise forms.ValidationError(
                    f'El estudiante {estudiante.nombre_completo} ya está postulado a esta vacante.'
                )

            # VALIDACIÓN 2: Verificar que la vacante tenga cupos disponibles
            if vacante.cupos_ocupados >= vacante.cantidad_cupos:
                raise forms.ValidationError(
                    f'La vacante "{vacante.titulo}" no tiene cupos disponibles.'
                )

            # VALIDACIÓN 3: Verificar requisitos académicos del estudiante
            if estudiante.semestre < vacante.semestre_minimo:
                raise forms.ValidationError(
                    f'El estudiante no cumple el requisito de semestre mínimo ({vacante.semestre_minimo}°). '
                    f'El estudiante está en {estudiante.semestre}° semestre.'
                )

            # VALIDACIÓN 4: Verificar que el programa académico coincida (opcional, con advertencia)
            # Si quieres hacerlo estricto, descomenta esto:
            # if estudiante.programa_academico != vacante.programa_academico:
            #     raise forms.ValidationError(
            #         f'El programa académico del estudiante ({estudiante.programa_academico}) '
            #         f'no coincide con el requerido por la vacante ({vacante.programa_academico}).'
            #     )

            # VALIDACIÓN 5: Verificar que el estudiante no esté en demasiadas postulaciones activas
            postulaciones_activas = Postulacion.objects.filter(
                estudiante=estudiante,
                estado__in=['POSTULADO', 'SELECCIONADO']
            ).count()

            if postulaciones_activas >= 3:
                raise forms.ValidationError(
                    f'El estudiante {estudiante.nombre_completo} ya tiene {postulaciones_activas} '
                    f'postulaciones activas. Máximo permitido: 3.'
                )

        return cleaned_data

    def save(self, commit=True):
        postulacion = super().save(commit=False)
        postulacion.estado = 'POSTULADO'  # Estado inicial

        if commit:
            postulacion.save()

        return postulacion


class PostulacionForm(forms.ModelForm):
    """
    Formulario para postular estudiantes a vacantes de práctica (RF-03)
    """

    class Meta:
        model = Postulacion
        fields = [
            'vacante',
            'estudiante',
            'observaciones',
        ]

        widgets = {
            'vacante': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'id_vacante'
            }),
            'estudiante': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'id_estudiante'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones adicionales sobre el estudiante y su idoneidad para esta vacante...',
            }),
        }

        labels = {
            'vacante': 'Vacante de Práctica',
            'estudiante': 'Estudiante a Postular',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar solo vacantes disponibles con cupos libres
        self.fields['vacante'].queryset = Vacante.objects.filter(
            estado='DISPONIBLE'
        ).select_related('empresa')

        # Filtrar solo estudiantes aptos para postular
        self.fields['estudiante'].queryset = Estudiante.objects.filter(
            estado='APTO'
        ).order_by('nombre_completo')

        # Mensajes si no hay opciones disponibles
        if not self.fields['vacante'].queryset.exists():
            self.fields['vacante'].empty_label = "No hay vacantes disponibles"

        if not self.fields['estudiante'].queryset.exists():
            self.fields['estudiante'].empty_label = "No hay estudiantes aptos"

        # Personalizar la visualización de las opciones
        self.fields['vacante'].label_from_instance = self._vacante_label
        self.fields['estudiante'].label_from_instance = self._estudiante_label

    def _vacante_label(self, obj):
        """Personalizar cómo se muestra cada vacante en el select"""
        cupos_disponibles = obj.cantidad_cupos - obj.cupos_ocupados
        return f"{obj.titulo} - {obj.empresa.razon_social} ({cupos_disponibles} cupos disponibles)"

    def _estudiante_label(self, obj):
        """Personalizar cómo se muestra cada estudiante en el select"""
        return f"{obj.codigo} - {obj.nombre_completo} ({obj.programa_academico} - {obj.semestre}° sem)"

    def clean(self):
        cleaned_data = super().clean()
        vacante = cleaned_data.get('vacante')
        estudiante = cleaned_data.get('estudiante')

        if vacante and estudiante:
            # VALIDACIÓN 1: Verificar que el estudiante no esté ya postulado a esta vacante
            postulacion_existente = Postulacion.objects.filter(
                vacante=vacante,
                estudiante=estudiante
            ).exists()

            if postulacion_existente:
                raise forms.ValidationError(
                    f'El estudiante {estudiante.nombre_completo} ya está postulado a esta vacante.'
                )

            # VALIDACIÓN 2: Verificar que la vacante tenga cupos disponibles
            if vacante.cupos_ocupados >= vacante.cantidad_cupos:
                raise forms.ValidationError(
                    f'La vacante "{vacante.titulo}" no tiene cupos disponibles.'
                )

            # VALIDACIÓN 3: Verificar requisitos académicos del estudiante
            if estudiante.semestre < vacante.semestre_minimo:
                raise forms.ValidationError(
                    f'El estudiante no cumple el requisito de semestre mínimo ({vacante.semestre_minimo}°). '
                    f'El estudiante está en {estudiante.semestre}° semestre.'
                )

            # VALIDACIÓN 4: Verificar que el estudiante no esté en demasiadas postulaciones activas
            postulaciones_activas = Postulacion.objects.filter(
                estudiante=estudiante,
                estado__in=['POSTULADO', 'SELECCIONADO']
            ).count()

            if postulaciones_activas >= 3:
                raise forms.ValidationError(
                    f'El estudiante {estudiante.nombre_completo} ya tiene {postulaciones_activas} '
                    f'postulaciones activas. Máximo permitido: 3.'
                )

        return cleaned_data

    def save(self, commit=True):
        postulacion = super().save(commit=False)
        postulacion.estado = 'POSTULADO'  # Estado inicial

        if commit:
            postulacion.save()

        return postulacion
