from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Vacante, Empresa, Postulacion, Estudiante, TutorEmpresarial, PracticaEmpresarial, DocenteAsesor
from datetime import date, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Sustentacion


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


# ==============================
# EmpresaForm (CRUD para Empresa)
# ==============================
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'razon_social',
            'nit',
            'direccion',
            'telefono',
            'email',
            'ciudad',
            'representante_nombre',
            'representante_cargo',
            'representante_email',
            'representante_telefono',
            'camara_comercio',
            'rut',
            'estado',
            'observaciones',
        ]

        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'representante_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'representante_cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'representante_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'representante_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            # ✅ ACTUALIZAR WIDGETS PARA ARCHIVOS
            'camara_comercio': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'onchange': 'validateFile(this, "camara")'
            }),
            'rut': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'onchange': 'validateFile(this, "rut")'
            }),
        }

        labels = {
            'razon_social': 'Razón Social',
            'nit': 'NIT',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Email',
            'ciudad': 'Ciudad',
            'representante_nombre': 'Nombre del Representante',
            'representante_cargo': 'Cargo del Representante',
            'representante_email': 'Email del Representante',
            'representante_telefono': 'Teléfono del Representante',
            'camara_comercio': 'Cámara de Comercio (PDF)',
            'rut': 'RUT (PDF)',
            'observaciones': 'Observaciones',
            'estado': 'Estado',
        }

    # ✅ AÑADIR VALIDACIÓN DE ARCHIVOS PDF
    def clean_camara_comercio(self):
        archivo = self.cleaned_data.get('camara_comercio')
        if archivo:
            # Validar tamaño (máximo 5MB)
            if archivo.size > 5242880:
                raise ValidationError('El archivo no debe superar los 5MB')
            # Validar extensión
            if not archivo.name.endswith('.pdf'):
                raise ValidationError('Solo se permiten archivos PDF')
        return archivo

    def clean_rut(self):
        archivo = self.cleaned_data.get('rut')
        if archivo:
            # Validar tamaño (máximo 5MB)
            if archivo.size > 5242880:
                raise ValidationError('El archivo no debe superar los 5MB')
            # Validar extensión
            if not archivo.name.endswith('.pdf'):
                raise ValidationError('Solo se permiten archivos PDF')
        return archivo

    def clean_nit(self):
        nit = self.cleaned_data.get('nit')
        if nit:
            qs = Empresa.objects.filter(nit=nit)
            # En edición, permitimos el mismo registro
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('Ya existe una empresa con este NIT')
        return nit

# ==============================
# TutorEmpresarialForm (CRUD para Tutores)
# ==============================
class TutorEmpresarialForm(forms.ModelForm):
    class Meta:
        model = TutorEmpresarial
        fields = [
            'empresa',
            'nombre_completo',
            'cargo',
            'email',
            'telefono',
            'activo',
        ]

        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Jorge Martínez López',
                'required': True
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Líder de Desarrollo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@empresa.com',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3101234567',
                'required': True
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'empresa': 'Empresa',
            'nombre_completo': 'Nombre Completo',
            'cargo': 'Cargo',
            'email': 'Email',
            'telefono': 'Teléfono',
            'activo': 'Activo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo empresas aprobadas
        self.fields['empresa'].queryset = Empresa.objects.filter(estado='APROBADA')

        if not self.fields['empresa'].queryset.exists():
            self.fields['empresa'].empty_label = "No hay empresas aprobadas disponibles"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Validar que el email no esté duplicado (excluyendo la instancia actual si es edición)
            qs = TutorEmpresarial.objects.filter(email=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('Ya existe un tutor con este email')
        return email


# ==============================
# SustentacionForm (CRUD para Sustentaciones)
# ==============================
class SustentacionForm(forms.ModelForm):
    class Meta:
        model = Sustentacion
        fields = [
            'practica',
            'fecha_programada',
            'lugar',
            'jurado_1',
            'jurado_2',
            'calificacion',
            'observaciones',
        ]

        widgets = {
            'practica': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_programada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Sala de Conferencias A',
                'required': True
            }),
            'jurado_1': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'jurado_2': forms.Select(attrs={
                'class': 'form-select'
            }),
            'calificacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.0',
                'max': '5.0',
                'step': '0.1',
                'placeholder': 'Ej: 4.5'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones adicionales sobre la sustentación...'
            }),
        }

        labels = {
            'practica': 'Práctica Empresarial',
            'fecha_programada': 'Fecha y Hora Programada',
            'lugar': 'Lugar de Sustentación',
            'jurado_1': 'Jurado Principal',
            'jurado_2': 'Jurado Secundario (Opcional)',
            'calificacion': 'Calificación Final (0.0 - 5.0)',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar solo prácticas finalizadas sin sustentación
        if not self.instance.pk:  # Solo al crear
            self.fields['practica'].queryset = PracticaEmpresarial.objects.filter(
                estado='FINALIZADA',
                sustentacion__isnull=True
            ).select_related('estudiante', 'empresa')
        else:  # Al editar, mostrar la práctica actual
            self.fields['practica'].queryset = PracticaEmpresarial.objects.filter(
                id=self.instance.practica.id
            )
            self.fields['practica'].disabled = True

        # Filtrar solo docentes activos
        self.fields['jurado_1'].queryset = DocenteAsesor.objects.filter(activo=True)
        self.fields['jurado_2'].queryset = DocenteAsesor.objects.filter(activo=True)

        # Mensajes si no hay opciones
        if not self.fields['practica'].queryset.exists():
            self.fields['practica'].empty_label = "No hay prácticas finalizadas sin sustentación"

        if not self.fields['jurado_1'].queryset.exists():
            self.fields['jurado_1'].empty_label = "No hay docentes activos disponibles"

    def clean(self):
        cleaned_data = super().clean()
        jurado_1 = cleaned_data.get('jurado_1')
        jurado_2 = cleaned_data.get('jurado_2')
        calificacion = cleaned_data.get('calificacion')
        fecha_programada = cleaned_data.get('fecha_programada')

        # Validar que los jurados sean diferentes
        if jurado_1 and jurado_2 and jurado_1.id == jurado_2.id:
            raise ValidationError('Los jurados deben ser docentes diferentes')

        # Validar que la fecha sea futura (solo al crear)
        if not self.instance.pk and fecha_programada:
            if fecha_programada < timezone.now():
                raise ValidationError('La fecha de sustentación debe ser futura')

        # Validar calificación si existe
        if calificacion is not None:
            if calificacion < 0 or calificacion > 5:
                raise ValidationError('La calificación debe estar entre 0.0 y 5.0')

        # Validación defensiva: verificar que la práctica aún no tenga sustentación
        practica = cleaned_data.get('practica')
        if not self.instance.pk and practica:
            # Si la práctica ya tiene una sustentación registrada, rechazar
            if PracticaEmpresarial.objects.filter(id=practica.id, sustentacion__isnull=False).exists():
                raise ValidationError('La práctica seleccionada ya tiene una sustentación registrada')

        return cleaned_data