from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# ============================================
# MODELO: COORDINADOR EMPRESARIAL
# ============================================
class Coordinador(models.Model):
    """Coordinador Empresarial - Gestiona todo el proceso de prácticas"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coordinador')
    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    # Foto de perfil
    foto_perfil = models.ImageField(
        upload_to='coordinadores/fotos_perfil/',
        blank=True,
        null=True,
        help_text="Foto de perfil del coordinador"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Coordinador Empresarial'
        verbose_name_plural = 'Coordinadores Empresariales'

    def __str__(self):
        return f"{self.nombre_completo}"


# ============================================
# MODELO: EMPRESA FORMADORA
# ============================================
class Empresa(models.Model):
    """Empresas que ofrecen cupos de práctica (RF-01)"""

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente de Aprobación'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
        ('INACTIVA', 'Inactiva'),
    ]

    # Información básica
    razon_social = models.CharField(max_length=300)
    nit = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=300)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    ciudad = models.CharField(max_length=100)

    # Representante legal
    representante_nombre = models.CharField(max_length=200)
    representante_cargo = models.CharField(max_length=100)
    representante_email = models.EmailField()
    representante_telefono = models.CharField(max_length=20)

    # Documentos
    camara_comercio = models.FileField(
        upload_to='empresas/documentos/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
        null=True
    )
    rut = models.FileField(
        upload_to='empresas/documentos/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
        null=True
    )

    # Estado y control
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(blank=True, null=True)
    aprobada_por = models.ForeignKey(
        Coordinador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='empresas_aprobadas'
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Empresa Formadora'
        verbose_name_plural = 'Empresas Formadoras'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.razon_social} - {self.nit}"


# ============================================
# MODELO: VACANTE DE PRÁCTICA
# ============================================
class Vacante(models.Model):
    """Vacantes oficiales creadas por Coordinación (RF-02)"""

    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
        ('CERRADA', 'Cerrada'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vacantes')
    titulo = models.CharField(max_length=300)
    area_practica = models.CharField(max_length=200, help_text='Área propuesta por la empresa')
    descripcion = models.TextField()
    cantidad_cupos = models.IntegerField(default=1)
    cupos_ocupados = models.IntegerField(default=0)

    # Requisitos
    programa_academico = models.CharField(max_length=200)
    semestre_minimo = models.IntegerField()
    habilidades_requeridas = models.TextField(blank=True, null=True)

    # Horario y duración
    horario = models.CharField(max_length=200)
    duracion_meses = models.IntegerField(default=6)

    # Control
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    creada_por = models.ForeignKey(Coordinador, on_delete=models.CASCADE, related_name='vacantes_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Vacante de Práctica'
        verbose_name_plural = 'Vacantes de Práctica'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.titulo} - {self.empresa.razon_social}"

    @property
    def cupos_disponibles(self):
        return self.cantidad_cupos - self.cupos_ocupados


# ============================================
# MODELO: ESTUDIANTE
# ============================================
class Estudiante(models.Model):
    """Estudiantes que realizan prácticas"""

    ESTADO_CHOICES = [
        ('APTO', 'Apto para Práctica'),
        ('EN_PRACTICA', 'En Práctica'),
        ('FINALIZADO', 'Práctica Finalizada'),
        ('NO_APTO', 'No Apto'),
    ]

    # Información personal
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estudiante')
    codigo = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    programa_academico = models.CharField(max_length=200)
    semestre = models.IntegerField()

    # Foto de perfil
    foto_perfil = models.ImageField(
        upload_to='estudiantes/fotos_perfil/',
        blank=True,
        null=True,
        help_text="Foto de perfil del estudiante"
    )

    # Documentos
    hoja_vida = models.FileField(
        upload_to='estudiantes/hojas_vida/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
        null=True
    )

    # Estado y control
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='APTO')
    promedio_academico = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['nombre_completo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre_completo}"


# ============================================
# MODELO: POSTULACIÓN
# ============================================
class Postulacion(models.Model):
    """Postulaciones de estudiantes a vacantes (RF-03)"""

    ESTADO_CHOICES = [
        ('POSTULADO', 'Postulado'),
        ('SELECCIONADO', 'Seleccionado por Empresa'),
        ('RECHAZADO', 'Rechazado'),
        ('VINCULADO', 'Vinculado'),
    ]

    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='postulaciones')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='postulaciones')
    postulado_por = models.ForeignKey(Coordinador, on_delete=models.CASCADE, related_name='postulaciones_realizadas')

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='POSTULADO')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Postulación'
        verbose_name_plural = 'Postulaciones'
        ordering = ['-fecha_postulacion']
        unique_together = ['vacante', 'estudiante']

    def __str__(self):
        return f"{self.estudiante.nombre_completo} -> {self.vacante.titulo}"


# ============================================
# MODELO: TUTOR EMPRESARIAL
# ============================================
class TutorEmpresarial(models.Model):
    """Tutores de las empresas que supervisan estudiantes"""

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tutores')
    nombre_completo = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tutor Empresarial'
        verbose_name_plural = 'Tutores Empresariales'

    def __str__(self):
        return f"{self.nombre_completo} - {self.empresa.razon_social}"


# ============================================
# MODELO: DOCENTE ASESOR
# ============================================
class DocenteAsesor(models.Model):
    """Docentes que asesoran estudiantes en práctica"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='docente_asesor')
    nombre_completo = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    especialidad = models.CharField(max_length=200)

    # Foto de perfil
    foto_perfil = models.ImageField(
        upload_to='docentes/fotos_perfil/',
        blank=True,
        null=True,
        help_text="Foto de perfil del docente asesor"
    )

    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Docente Asesor'
        verbose_name_plural = 'Docentes Asesores'

    def __str__(self):
        return self.nombre_completo


# ============================================
# MODELO: PRÁCTICA EMPRESARIAL
# ============================================
class PracticaEmpresarial(models.Model):
    """Registro completo de una práctica empresarial"""

    ESTADO_CHOICES = [
        ('EN_CURSO', 'En Curso'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    # Relaciones principales
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='practicas')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='practicas')
    vacante = models.ForeignKey(Vacante, on_delete=models.SET_NULL, null=True, related_name='practicas')
    tutor_empresarial = models.ForeignKey(TutorEmpresarial, on_delete=models.SET_NULL, null=True,
                                          related_name='practicas_supervisadas')
    docente_asesor = models.ForeignKey(DocenteAsesor, on_delete=models.SET_NULL, null=True,
                                       related_name='practicas_asesoradas')

    # Fechas
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    fecha_fin_real = models.DateField(blank=True, null=True)

    # Plan de práctica (RF-06)
    plan_practica = models.FileField(
        upload_to='practicas/planes/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
        null=True
    )
    plan_aprobado = models.BooleanField(default=False)

    # Control
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='EN_CURSO')
    asignada_por = models.ForeignKey(Coordinador, on_delete=models.CASCADE, related_name='practicas_asignadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Práctica Empresarial'
        verbose_name_plural = 'Prácticas Empresariales'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.estudiante.nombre_completo} - {self.empresa.razon_social}"


# ============================================
# MODELO: SUSTENTACIÓN
# ============================================
class Sustentacion(models.Model):
    """Registro de sustentaciones (RF-09)"""

    ESTADO_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('APROBADA', 'Aprobada'),
        ('CANCELADA', 'Cancelada'),
    ]

    practica = models.OneToOneField(PracticaEmpresarial, on_delete=models.CASCADE, related_name='sustentacion')
    fecha_programada = models.DateTimeField()
    lugar = models.CharField(max_length=200)

    # Jurados
    jurado_1 = models.ForeignKey(
        DocenteAsesor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sustentaciones_jurado1'
    )
    jurado_2 = models.ForeignKey(
        DocenteAsesor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sustentaciones_jurado2'
    )

    # Resultado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PROGRAMADA')
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    acta_sustentacion = models.FileField(
        upload_to='sustentaciones/actas/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
        null=True
    )

    # Control
    registrada_por = models.ForeignKey(Coordinador, on_delete=models.CASCADE, related_name='sustentaciones_registradas')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sustentación'
        verbose_name_plural = 'Sustentaciones'

    def __str__(self):
        return f"Sustentación - {self.practica.estudiante.nombre_completo}"


# ============================================
# MODELO: EVALUACIÓN
# ============================================
class Evaluacion(models.Model):
    """Evaluaciones del desempeño (RF-08)"""

    TIPO_CHOICES = [
        ('PARCIAL', 'Evaluación Parcial'),
        ('FINAL', 'Evaluación Final'),
    ]

    practica = models.ForeignKey(PracticaEmpresarial, on_delete=models.CASCADE, related_name='evaluaciones')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    evaluado_por = models.ForeignKey(DocenteAsesor, on_delete=models.CASCADE, related_name='evaluaciones_realizadas')

    # Criterios de evaluación
    desempeño_tecnico = models.DecimalField(max_digits=3, decimal_places=1)
    cumplimiento_objetivos = models.DecimalField(max_digits=3, decimal_places=1)
    trabajo_equipo = models.DecimalField(max_digits=3, decimal_places=1)
    iniciativa = models.DecimalField(max_digits=3, decimal_places=1)
    presentacion_informes = models.DecimalField(max_digits=3, decimal_places=1)

    calificacion_final = models.DecimalField(max_digits=3, decimal_places=1)
    observaciones = models.TextField(blank=True, null=True)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        ordering = ['-fecha_evaluacion']

    def __str__(self):
        return f"{self.tipo} - {self.practica.estudiante.nombre_completo}"


# ============================================
# MODELO: SEGUIMIENTO SEMANAL
# ============================================
class SeguimientoSemanal(models.Model):
    """Registro de seguimiento semanal (RF-07)"""

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente de Revisión'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Requiere Correcciones'),
    ]

    practica = models.ForeignKey(PracticaEmpresarial, on_delete=models.CASCADE, related_name='seguimientos')
    semana_numero = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    # Actividades
    actividades_realizadas = models.TextField()
    logros = models.TextField(blank=True, null=True)
    dificultades = models.TextField(blank=True, null=True)

    # Evidencias
    evidencia = models.FileField(
        upload_to='practicas/seguimientos/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'png', 'docx', 'zip'])],
        blank=True,
        null=True
    )

    # Validación
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    validado_tutor = models.BooleanField(default=False)
    validado_docente = models.BooleanField(default=False)
    calificacion = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        help_text="Calificación del docente asesor (0.0 - 5.0)"
    )
    observaciones_tutor = models.TextField(blank=True, null=True)
    observaciones_docente = models.TextField(blank=True, null=True)
    fecha_revision_docente = models.DateTimeField(blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Seguimiento Semanal'
        verbose_name_plural = 'Seguimientos Semanales'
        ordering = ['practica', 'semana_numero']
        unique_together = ['practica', 'semana_numero']

    def __str__(self):
        return f"Semana {self.semana_numero} - {self.practica.estudiante.nombre_completo}"


# ============================================
# MODELO: MENSAJE (CHAT)
# ============================================
class Mensaje(models.Model):
    """Mensajes entre estudiante y docente asesor"""

    # Relaciones
    practica = models.ForeignKey(
        PracticaEmpresarial,
        on_delete=models.CASCADE,
        related_name='mensajes',
        help_text="Práctica a la que pertenece el mensaje"
    )
    remitente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
        help_text="Usuario que envía el mensaje"
    )

    # Contenido
    contenido = models.TextField(help_text="Contenido del mensaje")
    archivo_adjunto = models.FileField(
        upload_to='mensajes/adjuntos/',
        blank=True,
        null=True,
        help_text="Archivo adjunto opcional"
    )

    # Control
    leido = models.BooleanField(default=False, help_text="Indica si el mensaje fue leído")
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['fecha_envio']

    def __str__(self):
        return f"Mensaje de {self.remitente.username} - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"

