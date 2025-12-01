"""
Context processors para estudiantes
Inyecta datos del estudiante en todos los templates automáticamente
"""

def estudiante_data(request):
    """
    Añade el objeto estudiante al contexto de todos los templates
    Para mostrar foto de perfil y nombre en navbar/sidebar
    """
    context = {}

    if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
        context['estudiante_actual'] = request.user.estudiante

    return context

