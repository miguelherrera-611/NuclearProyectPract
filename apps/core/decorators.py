from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden


def coordinator_required(view_func):
    """Decorador que exige que el usuario esté autenticado y tenga un objeto `coordinador` asociado."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión')
            return redirect('login_unificado')
        if not request.user.is_active:
            messages.error(request, 'Tu cuenta está desactivada')
            return HttpResponseForbidden('Cuenta inactiva')
        if not hasattr(request.user, 'coordinador'):
            messages.error(request, 'Acceso denegado: se requiere rol Coordinador')
            return HttpResponseForbidden('Acceso denegado')
        active = request.session.get('active_role')
        if active and active != 'coordinador':
            messages.error(request, 'Acceso denegado con el rol activo actual')
            return HttpResponseForbidden('Acceso denegado')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def estudiante_required(view_func):
    """Decorador que exige que el usuario sea un estudiante autenticado."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión como estudiante')
            return redirect('login_unificado')
        if not hasattr(request.user, 'estudiante'):
            messages.error(request, 'Tu cuenta no está registrada como estudiante')
            return HttpResponseForbidden('Acceso denegado: solo estudiantes')
        if not request.user.is_active:
            messages.error(request, 'Tu cuenta está desactivada')
            return HttpResponseForbidden('Cuenta inactiva')
        active = request.session.get('active_role')
        if active and active != 'estudiante':
            messages.error(request, 'Acceso denegado con el rol activo actual')
            return HttpResponseForbidden('Acceso denegado')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def tutor_required(view_func):
    """Decorador para verificar que el usuario sea un tutor empresarial."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'tutor_empresarial'):
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('login_unificado')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
