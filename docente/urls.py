"""
URLs para el Docente Asesor
"""
from django.urls import path
from . import docente_views

app_name = 'docente'

urlpatterns = [
    # Dashboard
    path('dashboard/', docente_views.dashboard_docente, name='dashboard'),

    # Estudiantes
    path('mis-estudiantes/', docente_views.mis_estudiantes, name='mis_estudiantes'),
    path('estudiante/<int:practica_id>/', docente_views.detalle_estudiante, name='detalle_estudiante'),

    # Seguimientos
    path('seguimientos-pendientes/', docente_views.seguimientos_pendientes, name='seguimientos_pendientes'),
    path('seguimiento/<int:seguimiento_id>/revisar/', docente_views.revisar_seguimiento, name='revisar_seguimiento'),

    # Perfil
    path('perfil/', docente_views.perfil_docente, name='perfil'),

    # Chat con Estudiantes (con parámetros query)
    path('chat/enviar/', docente_views.enviar_mensaje_docente, name='enviar_mensaje'),
    path('chat/mensajes/', docente_views.obtener_mensajes_docente, name='obtener_mensajes'),
]

