"""
Context processors para docentes
Inyecta datos del docente en todos los templates automáticamente
"""

def docente_data(request):
    """
    Añade el objeto docente al contexto de todos los templates
    Para mostrar foto de perfil y nombre en navbar/sidebar
    """
    context = {}

    if request.user.is_authenticated and hasattr(request.user, 'docente_asesor'):
        context['docente_actual'] = request.user.docente_asesor

    return context

