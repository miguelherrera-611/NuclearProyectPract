from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Avg, Count, Q
from apps.coordinacion.models import (
    TutorEmpresarial, PracticaEmpresarial, Encuesta,
    RespuestaEncuesta, DetalleRespuestaEncuesta, PreguntaEncuesta,
    SeguimientoSemanal
)
from apps.tutor_empresarial.forms import TutorPerfilForm
from apps.core.decorators import tutor_required


# ============================================
# VISTA: DASHBOARD TUTOR
# ============================================
@login_required
@tutor_required
def dashboard_tutor(request):
    """Dashboard principal del tutor empresarial"""
    tutor = request.user.tutor_empresarial

    # Estadísticas generales
    total_estudiantes = PracticaEmpresarial.objects.filter(
        tutor_empresarial=tutor,
        estado='EN_CURSO'
    ).count()

    encuestas_pendientes = Encuesta.objects.filter(
        estado='ACTIVA',
        fecha_inicio__lte=timezone.now().date(),
        fecha_fin__gte=timezone.now().date()
    ).exclude(
        respuestas__tutor=tutor
    ).count()

    encuestas_completadas = RespuestaEncuesta.objects.filter(
        tutor=tutor,
        estado='COMPLETADA'
    ).count()

    # Prácticas activas
    practicas_activas = PracticaEmpresarial.objects.filter(
        tutor_empresarial=tutor,
        estado='EN_CURSO'
    ).select_related('estudiante', 'empresa', 'docente_asesor')

    # Encuestas pendientes de responder
    encuestas_disponibles = Encuesta.objects.filter(
        estado='ACTIVA',
        fecha_inicio__lte=timezone.now().date(),
        fecha_fin__gte=timezone.now().date()
    ).exclude(
        respuestas__tutor=tutor
    )[:5]

    context = {
        'total_estudiantes': total_estudiantes,
        'encuestas_pendientes': encuestas_pendientes,
        'encuestas_completadas': encuestas_completadas,
        'practicas_activas': practicas_activas,
        'encuestas_disponibles': encuestas_disponibles,
    }

    return render(request, 'tutor/dashboard.html', context)


# ============================================
# VISTA: MIS ESTUDIANTES
# ============================================
@login_required
@tutor_required
def mis_estudiantes(request):
    """Lista de estudiantes asignados al tutor"""
    tutor = request.user.tutor_empresarial

    # Filtros
    estado_filtro = request.GET.get('estado', '')
    busqueda = request.GET.get('q', '')

    practicas = PracticaEmpresarial.objects.filter(
        tutor_empresarial=tutor
    ).select_related('estudiante', 'empresa', 'docente_asesor', 'vacante')

    if estado_filtro:
        practicas = practicas.filter(estado=estado_filtro)

    if busqueda:
        practicas = practicas.filter(
            Q(estudiante__nombre_completo__icontains=busqueda) |
            Q(estudiante__codigo__icontains=busqueda)
        )

    context = {
        'practicas': practicas,
        'estado_filtro': estado_filtro,
        'busqueda': busqueda,
    }

    return render(request, 'tutor/mis_estudiantes.html', context)


# ============================================
# VISTA: DETALLE ESTUDIANTE
# ============================================
@login_required
@tutor_required
def detalle_estudiante(request, practica_id):
    """Detalle completo de un estudiante en práctica"""
    tutor = request.user.tutor_empresarial

    practica = get_object_or_404(
        PracticaEmpresarial.objects.select_related(
            'estudiante', 'empresa', 'docente_asesor', 'vacante'
        ),
        id=practica_id,
        tutor_empresarial=tutor
    )

    # Seguimientos semanales
    seguimientos = SeguimientoSemanal.objects.filter(
        practica=practica
    ).order_by('-semana_numero')

    # Estadísticas de seguimientos
    total_seguimientos = seguimientos.count()
    aprobados = seguimientos.filter(estado='APROBADO').count()
    pendientes = seguimientos.filter(estado='PENDIENTE').count()

    context = {
        'practica': practica,
        'seguimientos': seguimientos,
        'total_seguimientos': total_seguimientos,
        'aprobados': aprobados,
        'pendientes': pendientes,
    }

    return render(request, 'tutor/detalle_estudiante.html', context)


# ============================================
# VISTA: ENCUESTAS DISPONIBLES
# ============================================
@login_required
@tutor_required
def encuestas_disponibles(request):
    """Lista de encuestas disponibles para responder"""
    tutor = request.user.tutor_empresarial

    # Encuestas activas que aún no ha respondido
    encuestas_pendientes = Encuesta.objects.filter(
        estado='ACTIVA',
        fecha_inicio__lte=timezone.now().date(),
        fecha_fin__gte=timezone.now().date()
    ).annotate(
        total_respuestas=Count('respuestas')
    )

    # Encuestas completadas por el tutor
    encuestas_completadas = RespuestaEncuesta.objects.filter(
        tutor=tutor,
        estado='COMPLETADA'
    ).select_related('encuesta', 'practica__estudiante')

    # Prácticas activas para poder responder encuestas
    practicas_activas = PracticaEmpresarial.objects.filter(
        tutor_empresarial=tutor,
        estado='EN_CURSO'
    ).select_related('estudiante')

    context = {
        'encuestas_pendientes': encuestas_pendientes,
        'encuestas_completadas': encuestas_completadas,
        'practicas_activas': practicas_activas,
    }

    return render(request, 'tutor/encuestas_disponibles.html', context)


# ============================================
# VISTA: RESPONDER ENCUESTA
# ============================================
@login_required
@tutor_required
def responder_encuesta(request, encuesta_id, practica_id):
    """Formulario para responder una encuesta sobre un estudiante"""
    tutor = request.user.tutor_empresarial

    encuesta = get_object_or_404(Encuesta, id=encuesta_id, estado='ACTIVA')
    practica = get_object_or_404(
        PracticaEmpresarial,
        id=practica_id,
        tutor_empresarial=tutor
    )

    # Verificar si ya existe una respuesta
    respuesta_existente = RespuestaEncuesta.objects.filter(
        encuesta=encuesta,
        practica=practica,
        tutor=tutor
    ).first()

    if request.method == 'POST':
        # Crear o actualizar respuesta
        if respuesta_existente:
            respuesta = respuesta_existente
        else:
            respuesta = RespuestaEncuesta.objects.create(
                encuesta=encuesta,
                practica=practica,
                tutor=tutor
            )

        # Procesar respuestas de las preguntas
        preguntas = encuesta.preguntas.all()
        suma_calificaciones = 0
        count_calificaciones = 0

        for pregunta in preguntas:
            campo_nombre = f'pregunta_{pregunta.id}'

            # Eliminar respuesta anterior si existe
            DetalleRespuestaEncuesta.objects.filter(
                respuesta_encuesta=respuesta,
                pregunta=pregunta
            ).delete()

            # Crear nueva respuesta
            detalle = DetalleRespuestaEncuesta(
                respuesta_encuesta=respuesta,
                pregunta=pregunta
            )

            if pregunta.tipo == 'CALIFICACION':
                calificacion = int(request.POST.get(campo_nombre, 0))
                detalle.calificacion = calificacion
                suma_calificaciones += calificacion
                count_calificaciones += 1

            elif pregunta.tipo == 'TEXTO':
                detalle.texto_respuesta = request.POST.get(campo_nombre, '')

            elif pregunta.tipo == 'OPCION_MULTIPLE':
                detalle.opcion_seleccionada = request.POST.get(campo_nombre, '')

            detalle.save()

        # Calcular promedio de calificaciones
        if count_calificaciones > 0:
            respuesta.calificacion_promedio = suma_calificaciones / count_calificaciones

        respuesta.estado = 'COMPLETADA'
        respuesta.fecha_completado = timezone.now()
        respuesta.save()

        messages.success(request, '¡Encuesta completada exitosamente!')
        return redirect('tutor:encuestas_disponibles')

    # GET: Mostrar formulario
    preguntas = encuesta.preguntas.all().order_by('orden')

    # Cargar respuestas existentes si las hay
    respuestas_guardadas = {}
    if respuesta_existente:
        for detalle in respuesta_existente.detalles.all():
            pregunta_id = detalle.pregunta.id
            if detalle.calificacion:
                respuestas_guardadas[f'pregunta_{pregunta_id}'] = detalle.calificacion
            elif detalle.texto_respuesta:
                respuestas_guardadas[f'pregunta_{pregunta_id}'] = detalle.texto_respuesta
            elif detalle.opcion_seleccionada:
                respuestas_guardadas[f'pregunta_{pregunta_id}'] = detalle.opcion_seleccionada

    context = {
        'encuesta': encuesta,
        'practica': practica,
        'preguntas': preguntas,
        'respuestas_guardadas': respuestas_guardadas,
        'respuesta_existente': respuesta_existente,
    }

    return render(request, 'tutor/responder_encuesta.html', context)


# ============================================
# VISTA: PERFIL TUTOR
# ============================================
@login_required
@tutor_required
def perfil_tutor(request):
    """Perfil del tutor empresarial"""
    tutor = request.user.tutor_empresarial

    if request.method == 'POST':
        form = TutorPerfilForm(request.POST, request.FILES, instance=tutor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('tutor:perfil')
    else:
        form = TutorPerfilForm(instance=tutor)

    context = {
        'form': form,
        'tutor': tutor,
    }

    return render(request, 'tutor/perfil.html', context)


# ============================================
# VISTA: LOGOUT
# ============================================
@login_required
def logout_tutor(request):
    """Cerrar sesión del tutor"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login_unificado')


