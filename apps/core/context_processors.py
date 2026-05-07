def coordinador_data(request):
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'coordinador'):
        context['coordinador'] = request.user.coordinador
    return context


def estudiante_data(request):
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
        context['estudiante_actual'] = request.user.estudiante
    return context


def docente_data(request):
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'docente_asesor'):
        context['docente_actual'] = request.user.docente_asesor
    return context


def tutor_data(request):
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'tutor_empresarial'):
        tutor = request.user.tutor_empresarial
        context['tutor'] = tutor
        context['tutor_nombre'] = tutor.nombre_completo
        context['tutor_foto'] = tutor.foto_perfil.url if tutor.foto_perfil else None
        context['tutor_empresa'] = tutor.empresa.razon_social if tutor.empresa else None
    return context
