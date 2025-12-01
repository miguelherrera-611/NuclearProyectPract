from django.urls import path
from . import estudiante_views

app_name = 'estudiante'

urlpatterns = [
    # ============================================
    # AUTENTICACIÓN (Login redirige al unificado, registro disponible)
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
    # SEGUIMIENTOS SEMANALES
    # ============================================
    path('seguimientos/', estudiante_views.mis_seguimientos, name='mis_seguimientos'),
    path('seguimientos/crear/', estudiante_views.crear_seguimiento, name='crear_seguimiento'),
    path('seguimientos/<int:seguimiento_id>/', estudiante_views.detalle_seguimiento, name='detalle_seguimiento'),
    path('seguimientos/<int:seguimiento_id>/editar/', estudiante_views.editar_seguimiento, name='editar_seguimiento'),

    # ============================================
    # PÁGINA PARA ESTUDIANTES NO APTOS
    # ============================================
    path('no-apto/', estudiante_views.estudiante_no_apto, name='no_apto'),

    # ============================================
    # MI DOCENTE ASESOR Y CHAT
    # ============================================
    path('mi-docente/', estudiante_views.mi_docente_asesor, name='mi_docente_asesor'),
    path('chat/', estudiante_views.chat_con_docente, name='chat_con_docente'),
    path('chat/enviar/', estudiante_views.enviar_mensaje, name='enviar_mensaje'),
    path('chat/mensajes/', estudiante_views.obtener_mensajes, name='obtener_mensajes'),
]