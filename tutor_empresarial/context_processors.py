"""
Context processor para el tutor empresarial
Proporciona datos del tutor en todos los templates
"""


def tutor_data(request):
    """Agrega información del tutor empresarial al contexto de los templates"""
    context = {}

    if request.user.is_authenticated and hasattr(request.user, 'tutor_empresarial'):
        tutor = request.user.tutor_empresarial
        context['tutor'] = tutor
        context['tutor_nombre'] = tutor.nombre_completo
        context['tutor_foto'] = tutor.foto_perfil.url if tutor.foto_perfil else None
        context['tutor_empresa'] = tutor.empresa.razon_social if tutor.empresa else None

    return context

