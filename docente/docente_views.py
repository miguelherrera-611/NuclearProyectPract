"""
Vistas para el Docente Asesor
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from coordinacion.models import DocenteAsesor, PracticaEmpresarial, SeguimientoSemanal, Estudiante


@login_required
def dashboard_docente(request):
    """Dashboard principal del docente asesor"""
    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        messages.error(request, 'No tienes un perfil de Docente Asesor.')
        return redirect('login_unificado')

    # Obtener prácticas asignadas al docente
    practicas_activas = PracticaEmpresarial.objects.filter(
        docente_asesor=docente,
        estado='EN_CURSO'
    ).select_related('estudiante', 'empresa', 'tutor_empresarial')

    # Obtener seguimientos pendientes de revisión
    seguimientos_pendientes = SeguimientoSemanal.objects.filter(
        practica__docente_asesor=docente,
        estado='PENDIENTE'
    ).select_related('practica__estudiante').order_by('-fecha_registro')

    # Estadísticas
    total_practicas = practicas_activas.count()
    total_pendientes = seguimientos_pendientes.count()

    context = {
        'docente': docente,
        'practicas_activas': practicas_activas,
        'seguimientos_pendientes': seguimientos_pendientes[:10],  # Últimos 10
        'total_practicas': total_practicas,
        'total_pendientes': total_pendientes,
    }

    return render(request, 'docente/dashboard.html', context)


@login_required
def mis_estudiantes(request):
    """Lista de estudiantes asignados al docente"""
    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        messages.error(request, 'No tienes un perfil de Docente Asesor.')
        return redirect('login_unificado')

    # Obtener todas las prácticas del docente
    practicas = PracticaEmpresarial.objects.filter(
        docente_asesor=docente
    ).select_related(
        'estudiante', 'empresa', 'tutor_empresarial'
    ).prefetch_related('seguimientos').order_by('-fecha_creacion')

    # Filtros
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        practicas = practicas.filter(estado=estado_filtro)

    context = {
        'docente': docente,
        'practicas': practicas,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'docente/mis_estudiantes.html', context)


@login_required
def detalle_estudiante(request, practica_id):
    """Detalle de un estudiante específico y su práctica"""
    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        messages.error(request, 'No tienes un perfil de Docente Asesor.')
        return redirect('login_unificado')

    # Obtener la práctica
    practica = get_object_or_404(
        PracticaEmpresarial,
        id=practica_id,
        docente_asesor=docente
    )

    # Obtener todos los seguimientos de esta práctica
    seguimientos = SeguimientoSemanal.objects.filter(
        practica=practica
    ).order_by('semana_numero')

    # Identificar el seguimiento más reciente (el de mayor semana_numero)
    seguimiento_mas_reciente = seguimientos.order_by('-semana_numero').first() if seguimientos.exists() else None

    # Calcular estadísticas
    total_seguimientos = seguimientos.count()
    seguimientos_aprobados = seguimientos.filter(estado='APROBADO').count()
    seguimientos_reprobados = seguimientos.filter(estado='RECHAZADO').count()

    context = {
        'docente': docente,
        'practica': practica,
        'seguimientos': seguimientos,
        'seguimiento_mas_reciente_id': seguimiento_mas_reciente.id if seguimiento_mas_reciente else None,
        'total_seguimientos': total_seguimientos,
        'seguimientos_aprobados': seguimientos_aprobados,
        'seguimientos_reprobados': seguimientos_reprobados,
    }

    return render(request, 'docente/detalle_estudiante.html', context)


@login_required
def seguimientos_pendientes(request):
    """Lista de seguimientos pendientes de revisión"""
    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        messages.error(request, 'No tienes un perfil de Docente Asesor.')
        return redirect('login_unificado')

    # Obtener seguimientos pendientes
    seguimientos = SeguimientoSemanal.objects.filter(
        practica__docente_asesor=docente,
        estado='PENDIENTE'
    ).select_related(
        'practica__estudiante', 'practica__empresa'
    ).order_by('-fecha_registro')

    context = {
        'docente': docente,
        'seguimientos': seguimientos,
    }

    return render(request, 'docente/seguimientos_pendientes.html', context)


@login_required
def revisar_seguimiento(request, seguimiento_id):
    """Revisar y calificar un seguimiento semanal"""
    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        messages.error(request, 'No tienes un perfil de Docente Asesor.')
        return redirect('login_unificado')

    # Obtener el seguimiento
    seguimiento = get_object_or_404(
        SeguimientoSemanal,
        id=seguimiento_id,
        practica__docente_asesor=docente
    )

    # Verificar si es el seguimiento más reciente (el único editable)
    seguimiento_mas_reciente = SeguimientoSemanal.objects.filter(
        practica=seguimiento.practica
    ).order_by('-semana_numero').first()

    es_seguimiento_mas_reciente = seguimiento.id == seguimiento_mas_reciente.id if seguimiento_mas_reciente else False

    if request.method == 'POST':
        observaciones = request.POST.get('observaciones_docente', '')
        calificacion_str = request.POST.get('calificacion', '')

        # Validar que se haya ingresado una calificación
        if not calificacion_str:
            messages.error(request, 'Debes ingresar una calificación para evaluar el seguimiento')
            return render(request, 'docente/revisar_seguimiento.html', {
                'docente': docente,
                'seguimiento': seguimiento,
            })

        # Validar y procesar calificación
        try:
            calificacion = float(calificacion_str)
            if calificacion < 0 or calificacion > 5:
                messages.error(request, 'La calificación debe estar entre 0.0 y 5.0')
                return render(request, 'docente/revisar_seguimiento.html', {
                    'docente': docente,
                    'seguimiento': seguimiento,
                })
        except ValueError:
            messages.error(request, 'La calificación debe ser un número válido')
            return render(request, 'docente/revisar_seguimiento.html', {
                'docente': docente,
                'seguimiento': seguimiento,
            })

        # Asignar estado automáticamente según la calificación
        if calificacion >= 3.0:
            seguimiento.estado = 'APROBADO'
            seguimiento.validado_docente = True
            estado_msg = 'aprobado'
            msg_type = 'success'
        else:
            seguimiento.estado = 'RECHAZADO'
            seguimiento.validado_docente = False
            estado_msg = 'requiere correcciones (nota menor a 3.0)'
            msg_type = 'warning'

        # Guardar datos
        seguimiento.calificacion = calificacion
        seguimiento.observaciones_docente = observaciones
        seguimiento.fecha_revision_docente = timezone.now()
        seguimiento.save()

        # Mensaje de confirmación
        if msg_type == 'success':
            messages.success(request, f'Seguimiento semana {seguimiento.semana_numero} {estado_msg} con nota {calificacion}')
        else:
            messages.warning(request, f'Seguimiento semana {seguimiento.semana_numero} {estado_msg} - Nota: {calificacion}')

        return redirect('docente:seguimientos_pendientes')

    context = {
        'docente': docente,
        'seguimiento': seguimiento,
        'es_seguimiento_mas_reciente': es_seguimiento_mas_reciente,
        'puede_editar': es_seguimiento_mas_reciente or seguimiento.estado == 'PENDIENTE',
    }

    return render(request, 'docente/revisar_seguimiento.html', context)


@login_required
def perfil_docente(request):
    """Perfil del docente asesor"""
    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        messages.error(request, 'No tienes un perfil de Docente Asesor.')
        return redirect('login_unificado')

    # Importar el formulario
    from docente.forms import DocenteAsesorPerfilForm

    if request.method == 'POST':
        form = DocenteAsesorPerfilForm(request.POST, request.FILES, instance=docente)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Tu perfil ha sido actualizado correctamente.')
            return redirect('docente:perfil')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario.')
    else:
        form = DocenteAsesorPerfilForm(instance=docente)

    # Estadísticas generales
    total_practicas_activas = PracticaEmpresarial.objects.filter(
        docente_asesor=docente,
        estado='EN_CURSO'
    ).count()

    total_practicas_finalizadas = PracticaEmpresarial.objects.filter(
        docente_asesor=docente,
        estado='FINALIZADA'
    ).count()

    total_seguimientos_pendientes = SeguimientoSemanal.objects.filter(
        practica__docente_asesor=docente,
        estado='PENDIENTE'
    ).count()

    context = {
        'docente': docente,
        'form': form,
        'total_practicas_activas': total_practicas_activas,
        'total_practicas_finalizadas': total_practicas_finalizadas,
        'total_seguimientos_pendientes': total_seguimientos_pendientes,
    }

    return render(request, 'docente/perfil.html', context)


# ============================================
# VISTAS: CHAT CON ESTUDIANTES
# ============================================

@login_required
def chat_con_estudiante(request, practica_id):
    """Vista del chat con un estudiante específico"""
    from django.http import JsonResponse
    from coordinacion.models import Mensaje

    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        messages.error(request, 'No tienes un perfil de Docente Asesor.')
        return redirect('login_unificado')

    # Obtener la práctica
    practica = get_object_or_404(
        PracticaEmpresarial,
        id=practica_id,
        docente_asesor=docente
    )

    estudiante = practica.estudiante

    # Obtener mensajes de esta práctica (últimos 100)
    mensajes_list = list(Mensaje.objects.filter(
        practica=practica
    ).select_related('remitente').order_by('fecha_envio')[:100])

    # Marcar como leídos los mensajes del estudiante
    Mensaje.objects.filter(
        practica=practica,
        remitente=estudiante.user,
        leido=False
    ).update(leido=True, fecha_lectura=timezone.now())

    # Obtener ID del último mensaje
    ultimo_mensaje_id = mensajes_list[-1].id if mensajes_list else 0

    context = {
        'docente': docente,
        'practica': practica,
        'estudiante': estudiante,
        'mensajes': mensajes_list,
        'ultimo_mensaje_id': ultimo_mensaje_id,
    }

    return render(request, 'docente/chat.html', context)


@login_required
def enviar_mensaje_docente(request):
    """AJAX: Enviar mensaje al estudiante"""
    from django.http import JsonResponse
    from coordinacion.models import Mensaje

    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        return JsonResponse({'error': 'No tienes perfil de docente'}, status=400)

    practica_id = request.POST.get('practica_id')
    if not practica_id:
        return JsonResponse({'error': 'ID de práctica requerido'}, status=400)

    # Obtener la práctica
    practica = get_object_or_404(
        PracticaEmpresarial,
        id=practica_id,
        docente_asesor=docente
    )

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


@login_required
def obtener_mensajes_docente(request):
    """AJAX: Obtener nuevos mensajes"""
    from django.http import JsonResponse
    from coordinacion.models import Mensaje

    try:
        docente = request.user.docente_asesor
    except DocenteAsesor.DoesNotExist:
        return JsonResponse({'mensajes': []})

    # Obtener practica_id del query string
    practica_id = request.GET.get('practica_id')
    if not practica_id:
        return JsonResponse({'error': 'practica_id requerido'}, status=400)

    # Obtener la práctica
    practica = get_object_or_404(
        PracticaEmpresarial,
        id=practica_id,
        docente_asesor=docente
    )

    # Obtener ID del último mensaje que tiene el cliente
    ultimo_id = request.GET.get('ultimo_id', 0)

    # Obtener mensajes nuevos
    mensajes = Mensaje.objects.filter(
        practica=practica,
        id__gt=ultimo_id
    ).select_related('remitente').order_by('fecha_envio')

    # Marcar como leídos los mensajes del estudiante
    Mensaje.objects.filter(
        practica=practica,
        remitente=practica.estudiante.user,
        leido=False,
        id__gt=ultimo_id
    ).update(leido=True, fecha_lectura=timezone.now())

    mensajes_data = []
    for mensaje in mensajes:
        # Obtener foto de perfil del remitente
        foto_perfil_url = None
        if hasattr(mensaje.remitente, 'estudiante') and mensaje.remitente.estudiante.foto_perfil:
            foto_perfil_url = mensaje.remitente.estudiante.foto_perfil.url
        elif hasattr(mensaje.remitente, 'docente_asesor') and mensaje.remitente.docente_asesor.foto_perfil:
            foto_perfil_url = mensaje.remitente.docente_asesor.foto_perfil.url

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
            'remitente_foto': foto_perfil_url,
            'es_mio': mensaje.remitente == request.user,
            'archivo': mensaje.archivo_adjunto.url if mensaje.archivo_adjunto else None,
            'leido': mensaje.leido,
        })

    return JsonResponse({'mensajes': mensajes_data})

