from django.conf import settings

class AutoSetRoleMiddleware:
    """Middleware de desarrollo: si DEBUG=True y el usuario está autenticado y
    tiene relación `estudiante`, asegura que `request.session['active_role'] = 'estudiante'`.

    Esto evita que las vistas protegidas por el decorador `estudiante_required`
    redirijan a login u obtengan Forbidden por falta de rol activo cuando se está
    probando en local. No afecta producción porque solo actúa si settings.DEBUG es True.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if settings.DEBUG and request.user.is_authenticated:
                # Si el usuario tiene atributo 'estudiante' y no hay rol activo, asignarlo
                if hasattr(request.user, 'estudiante') and request.session.get('active_role') is None:
                    request.session['active_role'] = 'estudiante'
        except Exception:
            # No romper la petición por cualquier error aquí (es solo ayuda de desarrollo)
            pass

        response = self.get_response(request)
        return response
