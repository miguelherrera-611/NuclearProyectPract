from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from coordinacion.models import Estudiante


class EstudianteRegistroForm(UserCreationForm):
    """
    Formulario de registro para nuevos estudiantes
    ✅ Valida semestre para determinar si es APTO o NO_APTO
    """

    # Campos del User de Django
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: juan.perez',
            'required': True
        }),
        help_text='Este será tu nombre de usuario para iniciar sesión'
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres',
            'required': True
        })
    )

    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña',
            'required': True
        })
    )

    # Campos específicos del Estudiante
    codigo = forms.CharField(
        label='Número de documento',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 2021001',
            'required': True
        })
    )

    nombre_completo = forms.CharField(
        label='Nombre Completo',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Juan Pérez García',
            'required': True
        })
    )

    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'estudiante@example.com',
            'required': True
        })
    )

    telefono = forms.CharField(
        label='Teléfono',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 3101234567',
            'required': True
        })
    )

    programa_academico = forms.CharField(
        label='Programa Académico',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Ingeniería de Sistemas',
            'required': True
        })
    )

    semestre = forms.IntegerField(
        label='Semestre Actual',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '10',
            'placeholder': 'Ej: 6',
            'required': True
        }),
        help_text='⚠️ Administración: desde 2° semestre | Software e Industrial: desde 4° semestre'
    )

    promedio_academico = forms.DecimalField(
        label='Promedio Académico (Opcional)',
        max_digits=3,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0.00',
            'max': '5.00',
            'step': '0.01',
            'placeholder': 'Ej: 4.2'
        })
    )

    hoja_vida = forms.FileField(
        label='Hoja de Vida (PDF - Opcional)',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf'
        }),
        help_text='Puedes subirla después desde tu perfil'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_codigo(self):
        """Validar que el código no esté duplicado"""
        codigo = self.cleaned_data.get('codigo')
        if Estudiante.objects.filter(codigo=codigo).exists():
            raise ValidationError(f'Ya existe un estudiante con el código {codigo}')
        return codigo

    def clean_email(self):
        """Validar que el email no esté duplicado"""
        email = self.cleaned_data.get('email')
        if Estudiante.objects.filter(email=email).exists():
            raise ValidationError(f'Ya existe un estudiante con el email {email}')
        if User.objects.filter(email=email).exists():
            raise ValidationError(f'Este email ya está registrado')
        return email

    def clean_semestre(self):
        """Validar rango de semestre"""
        semestre = self.cleaned_data.get('semestre')
        if semestre and (semestre < 1 or semestre > 10):
            raise ValidationError('El semestre debe estar entre 1 y 10')
        return semestre

    def clean_promedio_academico(self):
        """Validar promedio académico"""
        promedio = self.cleaned_data.get('promedio_academico')
        if promedio and (promedio < 0 or promedio > 5):
            raise ValidationError('El promedio debe estar entre 0.0 y 5.0')
        return promedio

    def clean(self):
        """
        Validación personalizada: verificar que el semestre sea válido según el programa
        """
        cleaned_data = super().clean()
        programa = cleaned_data.get('programa_academico')
        semestre = cleaned_data.get('semestre')

        if programa and semestre:
            # Definir semestres mínimos por programa
            requisitos = {
                'Administración de Empresas': 2,
                'Ingeniería de Software': 4,
                'Ingeniería Industrial': 4,
            }

            semestre_minimo = requisitos.get(programa)

            if semestre_minimo and semestre < semestre_minimo:
                raise ValidationError(
                    f'Para {programa} debes estar en {semestre_minimo}° semestre o superior para realizar prácticas. '
                    f'Actualmente estás en {semestre}° semestre.'
                )

        return cleaned_data

    def clean_hoja_vida(self):
        """Validar archivo de hoja de vida"""
        archivo = self.cleaned_data.get('hoja_vida')
        if archivo:
            # Validar tamaño (máximo 5MB)
            if archivo.size > 5242880:
                raise ValidationError('El archivo no debe superar los 5MB')
            # Validar extensión
            if not archivo.name.endswith('.pdf'):
                raise ValidationError('Solo se permiten archivos PDF')
        return archivo

    def save(self, commit=True):
        """
        Guardar usuario y estudiante
        ✅ LÓGICA: Determinar estado según programa académico y semestre
        """
        # Crear el User de Django
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # ✅ DETERMINAR ESTADO SEGÚN PROGRAMA Y SEMESTRE
            programa = self.cleaned_data['programa_academico']
            semestre = self.cleaned_data['semestre']

            # Definir semestres mínimos por programa
            requisitos = {
                'Administración de Empresas': 2,
                'Ingeniería de Software': 4,
                'Ingeniería Industrial': 4,
            }

            semestre_minimo = requisitos.get(programa, 4)  # Por defecto 4

            if semestre >= semestre_minimo:
                estado_inicial = 'APTO'
            else:
                estado_inicial = 'NO_APTO'

            # Crear el registro de Estudiante
            estudiante = Estudiante.objects.create(
                user=user,
                codigo=self.cleaned_data['codigo'],
                nombre_completo=self.cleaned_data['nombre_completo'],
                email=self.cleaned_data['email'],
                telefono=self.cleaned_data['telefono'],
                programa_academico=programa,
                semestre=semestre,
                promedio_academico=self.cleaned_data.get('promedio_academico'),
                hoja_vida=self.cleaned_data.get('hoja_vida'),
                estado=estado_inicial  # ✅ ASIGNACIÓN AUTOMÁTICA SEGÚN PROGRAMA
            )

            return user

        return user


class EstudianteLoginForm(AuthenticationForm):
    """
    Formulario de login para estudiantes
    """
    username = forms.CharField(
        label='Usuario',
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario',
            'autofocus': True
        })
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )


class EstudiantePerfilForm(forms.ModelForm):
    """
    Formulario para que el estudiante edite su perfil
    ✅ Puede actualizar semestre y esto cambia su estado automáticamente
    """

    class Meta:
        model = Estudiante
        fields = [
            'nombre_completo',
            'email',
            'telefono',
            'programa_academico',
            'semestre',
            'promedio_academico',
            'foto_perfil',
            'hoja_vida',
        ]

        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@example.com',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono',
                'required': True
            }),
            'programa_academico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Programa académico',
                'required': True
            }),
            'semestre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'required': True
            }),
            'promedio_academico': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.00',
                'max': '5.00',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'hoja_vida': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
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
            'programa_academico': 'Programa Académico',
            'semestre': 'Semestre Actual',
            'promedio_academico': 'Promedio Académico',
            'hoja_vida': 'Hoja de Vida (PDF)',
            'foto_perfil': 'Foto de Perfil',
        }

    def clean_email(self):
        """Validar que el email no esté duplicado (excluyendo el actual)"""
        email = self.cleaned_data.get('email')
        if email:
            qs = Estudiante.objects.filter(email=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('Ya existe otro estudiante con este email')
        return email

    def clean_semestre(self):
        """Validar rango de semestre"""
        semestre = self.cleaned_data.get('semestre')
        if semestre and (semestre < 1 or semestre > 10):
            raise ValidationError('El semestre debe estar entre 1 y 10')
        return semestre

    def clean_hoja_vida(self):
        """Validar archivo de hoja de vida"""
        archivo = self.cleaned_data.get('hoja_vida')
        if archivo:
            if archivo.size > 5242880:
                raise ValidationError('El archivo no debe superar los 5MB')
            if not archivo.name.endswith('.pdf'):
                raise ValidationError('Solo se permiten archivos PDF')
        return archivo

    def save(self, commit=True):
        """
        Guardar cambios y actualizar estado según semestre
        ✅ LÓGICA NUEVA: Recalcular estado si cambia semestre
        """
        estudiante = super().save(commit=False)

        # ✅ RECALCULAR ESTADO SEGÚN SEMESTRE
        if estudiante.semestre <= 3:
            # Si está en 1, 2 o 3 semestre: NO_APTO
            if estudiante.estado not in ['EN_PRACTICA', 'FINALIZADO']:
                estudiante.estado = 'NO_APTO'
        else:
            # Si está en 4to semestre o más: APTO (si no está en práctica)
            if estudiante.estado == 'NO_APTO':
                estudiante.estado = 'APTO'

        if commit:
            estudiante.save()

        return estudiante


class HojaVidaUploadForm(forms.ModelForm):
    """
    Formulario simple para subir/actualizar solo la hoja de vida
    """

    class Meta:
        model = Estudiante
        fields = ['hoja_vida']

        widgets = {
            'hoja_vida': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            })
        }

        labels = {
            'hoja_vida': 'Hoja de Vida (PDF)'
        }

    def clean_hoja_vida(self):
        """Validar archivo"""
        archivo = self.cleaned_data.get('hoja_vida')
        if archivo:
            if archivo.size > 5242880:
                raise ValidationError('El archivo no debe superar los 5MB')
            if not archivo.name.endswith('.pdf'):
                raise ValidationError('Solo se permiten archivos PDF')
        return archivo