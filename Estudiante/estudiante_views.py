from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from functools import wraps
from django.http import HttpResponseForbidden

# ✅ Importar modelos desde coordinacion
from coordinacion.models import (
    Estudiante, Vacante, Postulacion, PracticaEmpresarial,
    TutorEmpresarial, DocenteAsesor, Sustentacion,
    Evaluacion, SeguimientoSemanal, Empresa
)

# ✅ Importar formularios desde esta carpeta
from .estudiante_forms import (
    EstudianteRegistroForm, EstudianteLoginForm,
    EstudiantePerfilForm, HojaVidaUploadForm
)

# ✅ Importar serializadores de coordinacion para React
from coordinacion import serializers


# ============================================
# DECORADOR: SOLO ESTUDIANTES
# ============================================

def estudiante_required(view_func):
    """
    Decorador que exige que el usuario sea un estudiante autenticado
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión como estudiante')
            return redirect('login_unificado')

        # Verificar que tenga el objeto estudiante asociado
        if not hasattr(request.user, 'estudiante'):
            messages.error(request, 'Tu cuenta no está registrada como estudiante')
            return HttpResponseForbidden('Acceso denegado: solo estudiantes')

        # Verificar que esté activo
        if not request.user.is_active:
            messages.error(request, 'Tu cuenta está desactivada')
            return HttpResponseForbidden('Cuenta inactiva')

        # Verificar rol activo en sesión
        active = request.session.get('active_role')
        if active and active != 'estudiante':
            messages.error(request, 'Acceso denegado con el rol activo actual')
            return HttpResponseForbidden('Acceso denegado')

        return view_func(request, *args, **kwargs)

    return _wrapped_view


# ============================================
# AUTENTICACIÓN
# ============================================

def estudiante_login(request):
    """
    Vista de login para estudiantes
    Redirige al login unificado si el usuario no es estudiante
    """
    # Si ya está autenticado, verificar su rol
    if request.user.is_authenticated:
        if hasattr(request.user, 'estudiante'):
            # Es estudiante, redirigir a su dashboard
            return redirect('estudiante:dashboard')
        else:
            # No es estudiante, redirigir al login unificado
            messages.warning(
                request,
                'Esta cuenta no pertenece a un estudiante. Por favor, usa el login principal.'
            )
            return redirect('login_unificado')

    if request.method == 'POST':
        form = EstudianteLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Verificar que el usuario sea un estudiante
            if not hasattr(user, 'estudiante'):
                messages.error(
                    request,
                    '❌ Esta cuenta no está registrada como estudiante. '
                    'Si eres coordinador, usa el login de coordinación.'
                )
                return render(request, 'estudiante/login.html', {'form': form})

            # Login exitoso
            login(request, user)
            # Establecer rol activo en sesión
            request.session['active_role'] = 'estudiante'
            # Limpiar available_roles por si venía de login unificado
            request.session.pop('available_roles', None)
            messages.success(request, f'¡Bienvenido/a {user.estudiante.nombre_completo}! 👋')
            return redirect('estudiante:dashboard')
        else:
            messages.error(request, '❌ Usuario o contraseña incorrectos')
    else:
        form = EstudianteLoginForm()

    context = {
        'form': form,
    }

    return render(request, 'estudiante/login.html', context)


def estudiante_registro(request):
    """
    Vista de registro para nuevos estudiantes
    ✅ Asigna automáticamente estado según semestre
    """
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
        return redirect('estudiante:dashboard')

    if request.method == 'POST':
        form = EstudianteRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            estudiante = user.estudiante

            # Mensaje personalizado según estado
            if estudiante.estado == 'NO_APTO':
                messages.warning(
                    request,
                    f'✅ Registro exitoso. Sin embargo, como estás en {estudiante.semestre}° semestre, '
                    f'aún no puedes realizar prácticas empresariales. '
                    f'Podrás hacerlo a partir de 4to semestre.'
                )
            else:
                messages.success(
                    request,
                    f'✅ ¡Registro exitoso! Bienvenido/a {estudiante.nombre_completo}. '
                    f'Tu cuenta está lista y estás APTO para ser postulado a prácticas.'
                )

            # Login automático después del registro
            login(request, user)
            # Establecer rol activo en sesión
            request.session['active_role'] = 'estudiante'
            return redirect('estudiante:dashboard')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = EstudianteRegistroForm()

    context = {
        'form': form,
    }

    return render(request, 'estudiante/registro.html', context)


@estudiante_required
def estudiante_logout(request):
    """
    Cerrar sesión del estudiante
    """
    nombre = request.user.estudiante.nombre_completo
    logout(request)
    # Limpiar sesión relacionada a roles
    request.session.pop('active_role', None)
    request.session.pop('available_roles', None)
    messages.info(request, f'Hasta pronto, {nombre}. Has cerrado sesión correctamente 👋')
    return redirect('estudiante:login')


# ============================================
# DASHBOARD PRINCIPAL
# ============================================

@estudiante_required
def estudiante_dashboard(request):
    """
    Dashboard principal del estudiante
    Muestra información según su estado actual
    """
    estudiante = request.user.estudiante

    # Obtener práctica actual (si tiene)
    practica_actual = None
    if estudiante.estado == 'EN_PRACTICA':
        practica_actual = PracticaEmpresarial.objects.filter(
            estudiante=estudiante,
            estado='EN_CURSO'
        ).select_related('empresa', 'tutor_empresarial', 'docente_asesor').first()

    # Obtener postulaciones recientes
    postulaciones_recientes = Postulacion.objects.filter(
        estudiante=estudiante
    ).select_related('vacante', 'vacante__empresa').order_by('-fecha_postulacion')[:3]

    # Obtener vacantes disponibles según su programa
    vacantes_disponibles = Vacante.objects.filter(
        estado='DISPONIBLE',
        programa_academico__icontains=estudiante.programa_academico
    ).select_related('empresa').order_by('-fecha_publicacion')[:5]

    # Estadísticas
    stats = {
        'estado': estudiante.estado,
        'postulaciones_total': Postulacion.objects.filter(estudiante=estudiante).count(),
        'postulaciones_activas': Postulacion.objects.filter(
            estudiante=estudiante,
            estado__in=['POSTULADO', 'SELECCIONADO']
        ).count(),
        'vacantes_disponibles': vacantes_disponibles.count(),
        'tiene_hoja_vida': bool(estudiante.hoja_vida),
    }

    # Si tiene práctica, agregar estadísticas de práctica
    if practica_actual:
        stats['seguimientos_realizados'] = SeguimientoSemanal.objects.filter(
            practica=practica_actual
        ).count()
        stats['plan_aprobado'] = practica_actual.plan_aprobado

        # Verificar si tiene sustentación programada
        try:
            sustentacion = practica_actual.sustentacion
            stats['sustentacion_programada'] = True
            stats['fecha_sustentacion'] = sustentacion.fecha_programada
        except Sustentacion.DoesNotExist:
            stats['sustentacion_programada'] = False

    # Convertir a JSON para React
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    stats_json = json.dumps(stats, cls=DjangoJSONEncoder)

    # Serializar datos para React
    postulaciones_json = serializers.to_json([
        serializers.serialize_postulacion(p) for p in postulaciones_recientes
    ])

    vacantes_json = serializers.to_json([
        serializers.serialize_vacante(v) for v in vacantes_disponibles
    ])

    practica_json = None
    if practica_actual:
        practica_json = serializers.to_json(serializers.serialize_practica(practica_actual))

    # Serializar estudiante a JSON para uso en el cliente (React)
    estudiante_json = serializers.to_json(serializers.serialize_estudiante(estudiante))

    context = {
        'estudiante': estudiante,
        'estudiante_json': estudiante_json,
        'stats': stats_json,
        'postulaciones': postulaciones_json,
        'vacantes': vacantes_json,
        'practica_actual': practica_json,
    }

    return render(request, 'estudiante/dashboard.html', context)


# ============================================
# PERFIL Y DATOS PERSONALES
# ============================================

@estudiante_required
def estudiante_perfil(request):
    """
    Ver y editar perfil del estudiante
    ✅ Recalcula estado si cambia semestre
    """
    estudiante = request.user.estudiante
    estado_anterior = estudiante.estado

    if request.method == 'POST':
        form = EstudiantePerfilForm(request.POST, request.FILES, instance=estudiante)
        if form.is_valid():
            estudiante = form.save()

            # Verificar si cambió el estado
            if estado_anterior != estudiante.estado:
                if estudiante.estado == 'NO_APTO':
                    messages.warning(
                        request,
                        f'⚠️ Perfil actualizado. Debido a tu semestre actual ({estudiante.semestre}°), '
                        f'tu estado cambió a NO APTO. Podrás realizar prácticas a partir de 4to semestre.'
                    )
                elif estudiante.estado == 'APTO':
                    messages.success(
                        request,
                        f'✅ ¡Excelente! Perfil actualizado. Ahora estás APTO para ser postulado a prácticas.'
                    )
            else:
                messages.success(request, '✅ Perfil actualizado exitosamente')

            return redirect('estudiante:perfil')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = EstudiantePerfilForm(instance=estudiante)

    context = {
        'form': form,
        'estudiante': estudiante,
    }

    return render(request, 'estudiante/perfil.html', context)


@estudiante_required
def estudiante_subir_hoja_vida(request):
    """
    Vista rápida para subir/actualizar solo la hoja de vida
    """
    estudiante = request.user.estudiante

    if request.method == 'POST':
        form = HojaVidaUploadForm(request.POST, request.FILES, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Hoja de vida actualizada exitosamente')
            return redirect('estudiante:perfil')
        else:
            messages.error(request, '❌ Error al subir la hoja de vida')
    else:
        form = HojaVidaUploadForm(instance=estudiante)

    context = {
        'form': form,
        'estudiante': estudiante,
    }

    return render(request, 'estudiante/subir_hoja_vida.html', context)


# ============================================
# VACANTES DISPONIBLES (SOLO LECTURA)
# ============================================

@estudiante_required
def vacantes_disponibles(request):
    """
    Ver vacantes disponibles
    ✅ El estudiante NO puede postularse directamente (lo hace Coordinación)
    """
    estudiante = request.user.estudiante

    # Filtros
    programa_filtro = request.GET.get('programa', '')
    buscar = request.GET.get('buscar', '')

    # Obtener vacantes disponibles
    vacantes = Vacante.objects.filter(
        estado='DISPONIBLE'
    ).select_related('empresa', 'creada_por')

    # Filtrar por programa académico del estudiante (opcional)
    if programa_filtro == 'mi_programa':
        vacantes = vacantes.filter(programa_academico__icontains=estudiante.programa_academico)

    # Búsqueda
    if buscar:
        vacantes = vacantes.filter(
            Q(titulo__icontains=buscar) |
            Q(area_practica__icontains=buscar) |
            Q(empresa__razon_social__icontains=buscar)
        )

    # Verificar si el estudiante cumple requisitos para cada vacante
    vacantes_con_info = []
    for vacante in vacantes:
        cumple_semestre = estudiante.semestre >= vacante.semestre_minimo
        cumple_programa = vacante.programa_academico.lower() in estudiante.programa_academico.lower()

        # Verificar si ya está postulado a esta vacante
        ya_postulado = Postulacion.objects.filter(
            estudiante=estudiante,
            vacante=vacante
        ).exists()

        vacantes_con_info.append({
            'vacante': vacante,
            'cumple_requisitos': cumple_semestre and cumple_programa,
            'cumple_semestre': cumple_semestre,
            'cumple_programa': cumple_programa,
            'ya_postulado': ya_postulado,
        })

    # Serializar para React
    vacantes_json = serializers.to_json([
        {
            **serializers.serialize_vacante(item['vacante']),
            'cumple_requisitos': item['cumple_requisitos'],
            'ya_postulado': item['ya_postulado'],
        }
        for item in vacantes_con_info
    ])

    context = {
        'vacantes': vacantes_json,
        'programa_filtro': programa_filtro,
        'buscar': buscar,
        'estudiante_programa': estudiante.programa_academico,
    }

    return render(request, 'estudiante/vacantes/lista.html', context)


@estudiante_required
def vacante_detalle(request, vacante_id):
    """
    Ver detalle de una vacante específica
    """
    estudiante = request.user.estudiante
    vacante = get_object_or_404(Vacante, id=vacante_id)

    # Verificar si cumple requisitos
    cumple_semestre = estudiante.semestre >= vacante.semestre_minimo
    cumple_programa = vacante.programa_academico.lower() in estudiante.programa_academico.lower()

    # Verificar si ya está postulado
    postulacion = Postulacion.objects.filter(
        estudiante=estudiante,
        vacante=vacante
    ).first()

    context = {
        'vacante': vacante,
        'cumple_semestre': cumple_semestre,
        'cumple_programa': cumple_programa,
        'postulacion': postulacion,
    }

    return render(request, 'estudiante/vacantes/detalle.html', context)


# ============================================
# MIS POSTULACIONES
# ============================================

@estudiante_required
def mis_postulaciones(request):
    """
    Ver todas las postulaciones del estudiante
    """
    estudiante = request.user.estudiante

    # Filtro por estado
    estado_filtro = request.GET.get('estado', '')

    postulaciones = Postulacion.objects.filter(
        estudiante=estudiante
    ).select_related('vacante', 'vacante__empresa', 'postulado_por')

    if estado_filtro:
        postulaciones = postulaciones.filter(estado=estado_filtro)

    postulaciones = postulaciones.order_by('-fecha_postulacion')

    # Serializar para React
    postulaciones_json = serializers.to_json([
        serializers.serialize_postulacion(p) for p in postulaciones
    ])

    context = {
        'postulaciones': postulaciones_json,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'estudiante/postulaciones/lista.html', context)


@estudiante_required
def postulacion_detalle(request, postulacion_id):
    """
    Ver detalle de una postulación específica
    """
    estudiante = request.user.estudiante
    postulacion = get_object_or_404(
        Postulacion.objects.select_related('vacante', 'vacante__empresa', 'postulado_por'),
        id=postulacion_id,
        estudiante=estudiante  # Solo puede ver sus propias postulaciones
    )

    context = {
        'postulacion': postulacion,
    }

    return render(request, 'estudiante/postulaciones/detalle.html', context)


# ============================================
# MI PRÁCTICA ACTUAL
# ============================================

@estudiante_required
def mi_practica(request):
    """
    Ver información completa de la práctica actual
    Solo accesible si el estudiante está EN_PRACTICA
    """
    estudiante = request.user.estudiante

    # Verificar que esté en práctica
    if estudiante.estado != 'EN_PRACTICA':
        messages.warning(
            request,
            'No tienes una práctica activa en este momento'
        )
        return redirect('estudiante:dashboard')

    # Obtener práctica actual
    practica = PracticaEmpresarial.objects.filter(
        estudiante=estudiante,
        estado='EN_CURSO'
    ).select_related(
        'empresa', 'tutor_empresarial', 'docente_asesor', 'asignada_por'
    ).first()

    if not practica:
        messages.error(request, 'No se encontró tu práctica activa')
        return redirect('estudiante:dashboard')

    # Obtener seguimientos
    seguimientos = SeguimientoSemanal.objects.filter(
        practica=practica
    ).order_by('-semana_numero')

    # Obtener evaluaciones
    evaluaciones = Evaluacion.objects.filter(
        practica=practica
    ).select_related('evaluado_por').order_by('-fecha_evaluacion')

    # Verificar sustentación
    sustentacion = None
    try:
        sustentacion = practica.sustentacion
    except Sustentacion.DoesNotExist:
        pass

    # Serializar para React
    practica_json = serializers.to_json(serializers.serialize_practica(practica))

    context = {
        'practica': practica,
        'practica_json': practica_json,
        'seguimientos': seguimientos,
        'evaluaciones': evaluaciones,
        'sustentacion': sustentacion,
    }

    return render(request, 'estudiante/practica/mi_practica.html', context)


# ============================================
# PÁGINA DE ESTUDIANTES NO APTOS
# ============================================

@estudiante_required
def estudiante_no_apto(request):
    """
    Página informativa para estudiantes no aptos (semestre 1, 2 o 3)
    """
    estudiante = request.user.estudiante

    # Calcular en cuántos semestres podrá hacer prácticas
    semestres_faltantes = max(0, 4 - estudiante.semestre)

    context = {
        'estudiante': estudiante,
        'semestres_faltantes': semestres_faltantes,
    }

    return render(request, 'estudiante/no_apto.html', context)
