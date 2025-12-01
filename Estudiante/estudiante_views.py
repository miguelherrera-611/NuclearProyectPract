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
    Redirección al login unificado
    Esta vista se mantiene solo para compatibilidad con URLs antiguas
    """
    messages.info(request, 'Por favor, inicia sesión seleccionando tu rol')
    return redirect('login_unificado')



def estudiante_registro(request):
    """
    Vista de registro para nuevos estudiantes
    ✅ Asigna automáticamente estado según programa y semestre
    """
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
        return redirect('estudiante:dashboard')

    if request.method == 'POST':
        form = EstudianteRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            estudiante = user.estudiante

            # Requisitos por programa
            requisitos = {
                'Administración de Empresas': 2,
                'Ingeniería de Software': 4,
                'Ingeniería Industrial': 4,
            }

            semestre_minimo = requisitos.get(estudiante.programa_academico, 4)

            # Mensaje personalizado según estado y programa
            if estudiante.estado == 'NO_APTO':
                messages.warning(
                    request,
                    f'✅ Registro exitoso. Sin embargo, como estudiante de {estudiante.programa_academico} '
                    f'en {estudiante.semestre}° semestre, aún no puedes realizar prácticas empresariales. '
                    f'Podrás hacerlo a partir del {semestre_minimo}° semestre.'
                )
            else:
                messages.success(
                    request,
                    f'✅ ¡Registro exitoso! Bienvenido/a {estudiante.nombre_completo}. '
                    f'Como estudiante de {estudiante.programa_academico} en {estudiante.semestre}° semestre, '
                    f'estás APTO para ser postulado a prácticas empresariales.'
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


def estudiante_logout(request):
    """
    Cerrar sesión del estudiante
    """
    if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
        nombre = request.user.estudiante.nombre_completo
        messages.info(request, f'Hasta pronto, {nombre}. Has cerrado sesión correctamente 👋')

    logout(request)
    # Limpiar sesión relacionada a roles
    request.session.pop('active_role', None)
    request.session.pop('available_roles', None)
    return redirect('login_unificado')


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


# ============================================
# SEGUIMIENTOS SEMANALES
# ============================================

@estudiante_required
def mis_seguimientos(request):
    """
    Vista para que el estudiante vea todos sus seguimientos semanales
    """
    estudiante = request.user.estudiante

    # Verificar que esté en práctica
    practica = PracticaEmpresarial.objects.filter(
        estudiante=estudiante,
        estado='EN_CURSO'
    ).select_related('empresa', 'docente_asesor', 'tutor_empresarial').first()

    if not practica:
        messages.warning(request, 'No tienes una práctica activa en este momento.')
        return redirect('estudiante:dashboard')

    # Obtener todos los seguimientos
    seguimientos = SeguimientoSemanal.objects.filter(
        practica=practica
    ).order_by('-semana_numero')

    context = {
        'estudiante': estudiante,
        'practica': practica,
        'seguimientos': seguimientos,
    }

    return render(request, 'estudiante/seguimientos/lista.html', context)


@estudiante_required
def crear_seguimiento(request):
    """
    Vista para que el estudiante cree un nuevo seguimiento semanal
    """
    estudiante = request.user.estudiante

    # Obtener práctica activa
    practica = PracticaEmpresarial.objects.filter(
        estudiante=estudiante,
        estado='EN_CURSO'
    ).select_related('empresa', 'docente_asesor', 'tutor_empresarial').first()

    if not practica:
        messages.warning(request, 'No tienes una práctica activa.')
        return redirect('estudiante:dashboard')

    if request.method == 'POST':
        semana_numero = request.POST.get('semana_numero')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        actividades_realizadas = request.POST.get('actividades_realizadas')
        logros = request.POST.get('logros', '')
        dificultades = request.POST.get('dificultades', '')
        evidencia = request.FILES.get('evidencia')

        # Validar que la semana no exista
        if SeguimientoSemanal.objects.filter(practica=practica, semana_numero=semana_numero).exists():
            messages.error(request, f'Ya existe un seguimiento para la semana {semana_numero}.')
            return redirect('estudiante:crear_seguimiento')

        # Crear seguimiento
        seguimiento = SeguimientoSemanal.objects.create(
            practica=practica,
            semana_numero=semana_numero,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            actividades_realizadas=actividades_realizadas,
            logros=logros,
            dificultades=dificultades,
            evidencia=evidencia,
            estado='PENDIENTE'
        )

        messages.success(request, f'Seguimiento de la semana {semana_numero} creado correctamente.')
        return redirect('estudiante:mis_seguimientos')

    # Calcular siguiente número de semana
    ultimo_seguimiento = SeguimientoSemanal.objects.filter(practica=practica).order_by('-semana_numero').first()
    siguiente_semana = (ultimo_seguimiento.semana_numero + 1) if ultimo_seguimiento else 1

    context = {
        'estudiante': estudiante,
        'practica': practica,
        'siguiente_semana': siguiente_semana,
    }

    return render(request, 'estudiante/seguimientos/crear.html', context)


@estudiante_required
def detalle_seguimiento(request, seguimiento_id):
    """
    Vista para ver el detalle de un seguimiento específico
    """
    estudiante = request.user.estudiante

    seguimiento = get_object_or_404(
        SeguimientoSemanal,
        id=seguimiento_id,
        practica__estudiante=estudiante
    )

    context = {
        'estudiante': estudiante,
        'seguimiento': seguimiento,
    }

    return render(request, 'estudiante/seguimientos/detalle.html', context)


@estudiante_required
def editar_seguimiento(request, seguimiento_id):
    """
    Vista para editar un seguimiento (solo si está en estado RECHAZADO o PENDIENTE)
    """
    estudiante = request.user.estudiante

    seguimiento = get_object_or_404(
        SeguimientoSemanal,
        id=seguimiento_id,
        practica__estudiante=estudiante
    )

    # Solo se puede editar si está pendiente o rechazado
    if seguimiento.estado == 'APROBADO':
        messages.warning(request, 'No puedes editar un seguimiento que ya fue aprobado.')
        return redirect('estudiante:detalle_seguimiento', seguimiento_id=seguimiento.id)

    if request.method == 'POST':
        seguimiento.actividades_realizadas = request.POST.get('actividades_realizadas')
        seguimiento.logros = request.POST.get('logros', '')
        seguimiento.dificultades = request.POST.get('dificultades', '')

        # Si se sube nueva evidencia, reemplazar
        if request.FILES.get('evidencia'):
            seguimiento.evidencia = request.FILES.get('evidencia')

        # Si estaba rechazado, volver a pendiente
        if seguimiento.estado == 'RECHAZADO':
            seguimiento.estado = 'PENDIENTE'
            seguimiento.observaciones_docente = ''

        seguimiento.save()

        messages.success(request, f'Seguimiento de la semana {seguimiento.semana_numero} actualizado correctamente.')
        return redirect('estudiante:mis_seguimientos')

    context = {
        'estudiante': estudiante,
        'seguimiento': seguimiento,
    }

    return render(request, 'estudiante/seguimientos/editar.html', context)


# ============================================
# VISTAS: MI DOCENTE ASESOR Y CHAT
# ============================================

@estudiante_required
def mi_docente_asesor(request):
    """Vista de información del docente asesor asignado"""
    estudiante = request.user.estudiante

    # Obtener la práctica activa del estudiante
    practica = PracticaEmpresarial.objects.filter(
        estudiante=estudiante,
        estado='EN_CURSO'
    ).select_related('docente_asesor').first()

    if not practica or not practica.docente_asesor:
        messages.info(request, 'Aún no tienes un docente asesor asignado. Esto ocurre cuando te vinculan a una práctica.')
        return render(request, 'estudiante/mi_docente_asesor.html', {
            'estudiante': estudiante,
            'practica': None,
            'docente': None,
        })

    docente = practica.docente_asesor

    # Contar mensajes no leídos del docente
    from coordinacion.models import Mensaje
    mensajes_no_leidos = Mensaje.objects.filter(
        practica=practica,
        remitente=docente.user,
        leido=False
    ).count()

    context = {
        'estudiante': estudiante,
        'practica': practica,
        'docente': docente,
        'mensajes_no_leidos': mensajes_no_leidos,
    }

    return render(request, 'estudiante/mi_docente_asesor.html', context)


@estudiante_required
def chat_con_docente(request):
    """Vista del chat con el docente asesor"""
    from django.http import JsonResponse
    from coordinacion.models import Mensaje

    estudiante = request.user.estudiante

    # Obtener la práctica activa
    practica = PracticaEmpresarial.objects.filter(
        estudiante=estudiante,
        estado='EN_CURSO'
    ).select_related('docente_asesor').first()

    if not practica or not practica.docente_asesor:
        messages.error(request, 'No tienes un docente asesor asignado.')
        return redirect('estudiante:dashboard')

    docente = practica.docente_asesor

    # Obtener mensajes de esta práctica (últimos 100)
    mensajes_list = list(Mensaje.objects.filter(
        practica=practica
    ).select_related('remitente').order_by('fecha_envio')[:100])

    # Marcar como leídos los mensajes del docente
    Mensaje.objects.filter(
        practica=practica,
        remitente=docente.user,
        leido=False
    ).update(leido=True, fecha_lectura=timezone.now())

    # Obtener ID del último mensaje
    ultimo_mensaje_id = mensajes_list[-1].id if mensajes_list else 0

    context = {
        'estudiante': estudiante,
        'practica': practica,
        'docente': docente,
        'mensajes': mensajes_list,
        'ultimo_mensaje_id': ultimo_mensaje_id,
    }

    return render(request, 'estudiante/chat.html', context)


@estudiante_required
def enviar_mensaje(request):
    """AJAX: Enviar mensaje al docente"""
    from django.http import JsonResponse
    from coordinacion.models import Mensaje

    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    estudiante = request.user.estudiante

    # Obtener la práctica activa
    practica = PracticaEmpresarial.objects.filter(
        estudiante=estudiante,
        estado='EN_CURSO'
    ).first()

    if not practica:
        return JsonResponse({'error': 'No tienes práctica activa'}, status=400)

    contenido = request.POST.get('contenido', '').strip()
    archivo = request.FILES.get('archivo')

    if not contenido and not archivo:
        return JsonResponse({'error': 'Debes escribir un mensaje o adjuntar un archivo'}, status=400)

    # Crear el mensaje
    mensaje = Mensaje.objects.create(
        practica=practica,
        remitente=request.user,
        contenido=contenido,
        archivo_adjunto=archivo
    )

    return JsonResponse({
        'success': True,
        'mensaje': {
            'id': mensaje.id,
            'contenido': mensaje.contenido,
            'fecha_envio': mensaje.fecha_envio.strftime('%d/%m/%Y %H:%M'),
            'remitente': mensaje.remitente.username,
            'archivo': mensaje.archivo_adjunto.url if mensaje.archivo_adjunto else None,
        }
    })


@estudiante_required
def obtener_mensajes(request):
    """AJAX: Obtener nuevos mensajes"""
    from django.http import JsonResponse
    from coordinacion.models import Mensaje

    estudiante = request.user.estudiante

    # Obtener la práctica activa
    practica = PracticaEmpresarial.objects.filter(
        estudiante=estudiante,
        estado='EN_CURSO'
    ).first()

    if not practica:
        return JsonResponse({'mensajes': []})

    # Obtener ID del último mensaje que tiene el cliente
    ultimo_id = request.GET.get('ultimo_id', 0)

    # Obtener mensajes nuevos
    mensajes = Mensaje.objects.filter(
        practica=practica,
        id__gt=ultimo_id
    ).select_related('remitente').order_by('fecha_envio')

    # Marcar como leídos los mensajes del docente
    Mensaje.objects.filter(
        practica=practica,
        remitente=practica.docente_asesor.user,
        leido=False,
        id__gt=ultimo_id
    ).update(leido=True, fecha_lectura=timezone.now())

    mensajes_data = []
    for mensaje in mensajes:
        mensajes_data.append({
            'id': mensaje.id,
            'contenido': mensaje.contenido,
            'fecha_envio': mensaje.fecha_envio.strftime('%d/%m/%Y %H:%M'),
            'remitente': mensaje.remitente.username,
            'remitente_nombre': (
                mensaje.remitente.estudiante.nombre_completo
                if hasattr(mensaje.remitente, 'estudiante')
                else mensaje.remitente.docente_asesor.nombre_completo
            ),
            'es_mio': mensaje.remitente == request.user,
            'archivo': mensaje.archivo_adjunto.url if mensaje.archivo_adjunto else None,
            'leido': mensaje.leido,
        })

    return JsonResponse({'mensajes': mensajes_data})





