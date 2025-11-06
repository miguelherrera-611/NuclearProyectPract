from django.urls import path
from . import views

app_name = 'coordinacion'

urlpatterns = [
    # ============================================
    # AUTENTICACIÓN
    # ============================================
    path('', views.coordinador_login, name='login'),
    path('login/', views.coordinador_login, name='login'),
    path('logout/', views.coordinador_logout, name='logout'),

    # ============================================
    # DASHBOARD
    # ============================================
    path('dashboard/', views.coordinador_dashboard, name='dashboard'),

    # ============================================
    # GESTIÓN DE EMPRESAS (RF-01)
    # ============================================
    path('empresas/', views.empresas_lista, name='empresas_lista'),
    path('empresas/<int:empresa_id>/', views.empresa_detalle, name='empresa_detalle'),
    path('empresas/<int:empresa_id>/validar/', views.empresa_validar, name='empresa_validar'),

    # ============================================
    # GESTIÓN DE VACANTES (RF-02)
    # ============================================
    path('vacantes/', views.vacantes_lista, name='vacantes_lista'),
    path('vacantes/crear/', views.vacante_crear, name='vacante_crear'),
    path('vacantes/<int:vacante_id>/', views.vacante_detalle, name='vacante_detalle'),

    # ============================================
    # GESTIÓN DE ESTUDIANTES Y POSTULACIONES (RF-03)
    # ============================================
    path('estudiantes/', views.estudiantes_lista, name='estudiantes_lista'),
    path('postulaciones/', views.postulaciones_lista, name='postulaciones_lista'),
    path('postulaciones/crear/', views.postulacion_crear, name='postulacion_crear'),

    # ============================================
    # GESTIÓN DE TUTORES Y DOCENTES (RF-05)
    # ============================================
    path('tutores/', views.tutores_lista, name='tutores_lista'),
    path('docentes/', views.docentes_lista, name='docentes_lista'),
    path('postulaciones/<int:postulacion_id>/asignar/', views.practica_asignar, name='practica_asignar'),

    # ============================================
    # GESTIÓN DE PRÁCTICAS
    # ============================================
    path('practicas/', views.practicas_lista, name='practicas_lista'),
    path('practicas/<int:practica_id>/', views.practica_detalle, name='practica_detalle'),
    path('practicas/<int:practica_id>/cerrar/', views.practica_cerrar, name='practica_cerrar'),

    # ============================================
    # GESTIÓN DE SUSTENTACIONES (RF-09)
    # ============================================
    path('sustentaciones/', views.sustentaciones_lista, name='sustentaciones_lista'),
    path('practicas/<int:practica_id>/sustentacion/crear/', views.sustentacion_crear, name='sustentacion_crear'),

    # ============================================
    # REPORTES E INDICADORES (RF-12)
    # ============================================
    path('reportes/', views.reportes_dashboard, name='reportes_dashboard'),
]