"""
Context processors para coordinación
Inyecta datos del coordinador en todos los templates automáticamente
"""

def coordinador_data(request):
    """
    Añade el objeto coordinador al contexto de todos los templates
    Para mostrar foto de perfil y nombre en navbar/sidebar
    """
    context = {}

    if request.user.is_authenticated and hasattr(request.user, 'coordinador'):
        context['coordinador'] = request.user.coordinador

    return context

