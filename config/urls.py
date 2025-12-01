from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ LOGIN UNIFICADO (Página principal)
    path('', views.login_unificado, name='login_unificado'),
    path('login/', views.login_unificado, name='login_unificado'),
    path('seleccionar-rol/', views.seleccionar_rol, name='seleccionar_rol'),
    path('logout/', views.logout_view, name='logout'),

    # Rutas de Coordinación
    path('coordinacion/', include('coordinacion.urls')),

    # Rutas de Estudiantes
    path('estudiante/', include('Estudiante.urls')),

    # Rutas de Docente Asesor
    path('docente/', include('docente.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)