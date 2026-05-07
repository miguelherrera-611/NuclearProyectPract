from django.urls import path
from .views import tutor_views as views

app_name = 'tutor'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_tutor, name='dashboard'),

    # Estudiantes
    path('mis-estudiantes/', views.mis_estudiantes, name='mis_estudiantes'),
    path('estudiante/<int:practica_id>/', views.detalle_estudiante, name='detalle_estudiante'),

    # Encuestas
    path('encuestas/', views.encuestas_disponibles, name='encuestas_disponibles'),
    path('encuesta/<int:encuesta_id>/responder/<int:practica_id>/', views.responder_encuesta, name='responder_encuesta'),

    # Perfil
    path('perfil/', views.perfil_tutor, name='perfil'),

    # Logout
    path('logout/', views.logout_tutor, name='logout'),
]

