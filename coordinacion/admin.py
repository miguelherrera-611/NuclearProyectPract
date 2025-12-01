from django.contrib import admin
from .models import (
    Coordinador, Empresa, Vacante, Estudiante, Postulacion,
    TutorEmpresarial, DocenteAsesor, PracticaEmpresarial,
    Sustentacion, Evaluacion, SeguimientoSemanal
)


@admin.register(Coordinador)
class CoordinadorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'telefono', 'activo', 'fecha_creacion']
    search_fields = ['nombre_completo', 'email']
    list_filter = ['activo', 'fecha_creacion']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['razon_social', 'nit', 'ciudad', 'estado', 'fecha_registro']
    search_fields = ['razon_social', 'nit']
    list_filter = ['estado', 'ciudad', 'fecha_registro']


@admin.register(Vacante)
class VacanteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'empresa', 'programa_academico', 'cantidad_cupos', 'cupos_ocupados', 'estado']
    search_fields = ['titulo', 'empresa__razon_social']
    list_filter = ['estado', 'programa_academico']


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre_completo', 'programa_academico', 'semestre', 'estado']
    search_fields = ['codigo', 'nombre_completo', 'email']
    list_filter = ['estado', 'programa_academico', 'semestre']


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'vacante', 'estado', 'fecha_postulacion']
    search_fields = ['estudiante__nombre_completo', 'vacante__titulo']
    list_filter = ['estado', 'fecha_postulacion']


@admin.register(TutorEmpresarial)
class TutorEmpresarialAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'empresa', 'cargo', 'email', 'activo']
    search_fields = ['nombre_completo', 'email', 'empresa__razon_social']
    list_filter = ['activo', 'empresa']


@admin.register(DocenteAsesor)
class DocenteAsesorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'telefono', 'especialidad', 'activo']
    search_fields = ['nombre_completo', 'email', 'especialidad']
    list_filter = ['activo', 'fecha_registro']


@admin.register(PracticaEmpresarial)
class PracticaEmpresarialAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'empresa', 'docente_asesor', 'estado', 'fecha_inicio', 'fecha_fin_estimada']
    search_fields = ['estudiante__nombre_completo', 'empresa__razon_social']
    list_filter = ['estado', 'fecha_inicio']
    raw_id_fields = ['estudiante', 'empresa', 'vacante', 'tutor_empresarial', 'docente_asesor', 'asignada_por']


@admin.register(Sustentacion)
class SustentacionAdmin(admin.ModelAdmin):
    list_display = ['practica', 'fecha_programada', 'estado', 'calificacion']
    search_fields = ['practica__estudiante__nombre_completo']
    list_filter = ['estado', 'fecha_programada']


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['practica', 'tipo', 'calificacion_final', 'evaluado_por', 'fecha_evaluacion']
    search_fields = ['practica__estudiante__nombre_completo']
    list_filter = ['tipo', 'fecha_evaluacion']


@admin.register(SeguimientoSemanal)
class SeguimientoSemanalAdmin(admin.ModelAdmin):
    list_display = ['practica', 'semana_numero', 'fecha_inicio', 'fecha_fin', 'estado', 'validado_docente']
    search_fields = ['practica__estudiante__nombre_completo']
    list_filter = ['estado', 'validado_docente', 'validado_tutor', 'fecha_registro']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
