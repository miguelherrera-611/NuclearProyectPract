from django.urls import path
from . import estudiante_views

app_name = 'estudiante'

urlpatterns = [
    # ============================================
    # AUTENTICACIÓN
    # ============================================
    path('', estudiante_views.estudiante_login, name='login'),
    path('login/', estudiante_views.estudiante_login, name='login'),
    path('registro/', estudiante_views.estudiante_registro, name='registro'),
    path('logout/', estudiante_views.estudiante_logout, name='logout'),

    # ============================================
    # DASHBOARD Y PERFIL
    # ============================================
    path('dashboard/', estudiante_views.estudiante_dashboard, name='dashboard'),
    path('perfil/', estudiante_views.estudiante_perfil, name='perfil'),
    path('perfil/subir-hoja-vida/', estudiante_views.estudiante_subir_hoja_vida, name='subir_hoja_vida'),

    # ============================================
    # VACANTES DISPONIBLES (SOLO LECTURA)
    # ============================================
    path('vacantes/', estudiante_views.vacantes_disponibles, name='vacantes_lista'),
    path('vacantes/<int:vacante_id>/', estudiante_views.vacante_detalle, name='vacante_detalle'),

    # ============================================
    # MIS POSTULACIONES
    # ============================================
    path('postulaciones/', estudiante_views.mis_postulaciones, name='postulaciones_lista'),
    path('postulaciones/<int:postulacion_id>/', estudiante_views.postulacion_detalle, name='postulacion_detalle'),

    # ============================================
    # MI PRÁCTICA ACTUAL
    # ============================================
    path('practica/', estudiante_views.mi_practica, name='mi_practica'),

    # ============================================
    # PÁGINA PARA ESTUDIANTES NO APTOS
    # ============================================
    path('no-apto/', estudiante_views.estudiante_no_apto, name='no_apto'),
]