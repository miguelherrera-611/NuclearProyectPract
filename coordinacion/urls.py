from django.urls import path
from . import views
from . import company_views

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
    path('empresas/crear/', company_views.empresa_crear, name='empresa_crear'),
    path('empresas/<int:empresa_id>/', views.empresa_detalle, name='empresa_detalle'),
    path('empresas/<int:empresa_id>/editar/', company_views.empresa_editar, name='empresa_editar'),
    path('empresas/<int:empresa_id>/eliminar/', company_views.empresa_eliminar, name='empresa_eliminar'),
    path('empresas/<int:empresa_id>/validar/', views.empresa_validar, name='empresa_validar'),

    # ============================================
    # GESTIÓN DE VACANTES (RF-02)
    # ============================================
    path('vacantes/', views.vacantes_lista, name='vacantes_lista'),
    path('vacantes/crear/', views.vacante_crear, name='vacante_crear'),
    path('vacantes/<int:vacante_id>/', views.vacante_detalle, name='vacante_detalle'),
    path('vacantes/<int:vacante_id>/editar/', views.vacante_editar, name='vacante_editar'),


    # ============================================
    # GESTIÓN DE ESTUDIANTES Y POSTULACIONES (RF-03)
    # ============================================
    path('estudiantes/', views.estudiantes_lista, name='estudiantes_lista'),
    path('estudiantes/<int:estudiante_id>/', views.estudiante_detalle, name='estudiante_detalle'),
    path('postulaciones/', views.postulaciones_lista, name='postulaciones_lista'),
    path('postulaciones/crear/', views.postulacion_crear, name='postulacion_crear'),
    path('postulaciones/<int:postulacion_id>/', views.postulacion_detalle, name='postulacion_detalle'),
    path('postulaciones/<int:postulacion_id>/aprobar/', views.postulacion_aprobar, name='postulacion_aprobar'),
    path('postulaciones/<int:postulacion_id>/crear-practica/', views.practica_crear_desde_postulacion, name='practica_crear_desde_postulacion'),
    path('postulaciones/<int:postulacion_id>/editar/', views.postulacion_editar, name='postulacion_editar'),
    path('postulaciones/<int:postulacion_id>/eliminar/', views.postulacion_eliminar, name='postulacion_eliminar'),
    path('postulaciones/<int:postulacion_id>/rechazar/', views.postulacion_rechazar, name='postulacion_rechazar'),

    # ============================================
    # GESTIÓN DE TUTORES Y DOCENTES (RF-05)
    # ============================================
    path('tutores/', views.tutores_lista, name='tutores_lista'),
    path('tutores/crear/', views.tutor_crear, name='tutor_crear'),
    path('tutores/<int:tutor_id>/', views.tutor_detalle, name='tutor_detalle'),
    path('tutores/<int:tutor_id>/editar/', views.tutor_editar, name='tutor_editar'),
    path('tutores/<int:tutor_id>/toggle/', views.tutor_toggle_activo, name='tutor_toggle_activo'),

    path('docentes/', views.docentes_lista, name='docentes_lista'),
    path('postulaciones/<int:postulacion_id>/asignar/', views.practica_asignar, name='practica_asignar'),

    # ============================================
    # GESTIÓN DE PRÁCTICAS
    # ============================================
    path('practicas/', views.practicas_lista, name='practicas_lista'),
    path('practicas/<int:practica_id>/', views.practica_detalle, name='practica_detalle'),
    path('practicas/<int:practica_id>/cerrar/', views.practica_cerrar, name='practica_cerrar'),
    path('practicas/<int:practica_id>/', views.practica_detalle, name='practica_detalle'),
    path('practicas/<int:practica_id>/cancelar/', views.practica_cancelar, name='practica_cancelar'),
    path('practicas/<int:practica_id>/finalizar/', views.practica_finalizar, name='practica_finalizar'),

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