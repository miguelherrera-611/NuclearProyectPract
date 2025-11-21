from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.db import IntegrityError
from .forms import CoordinadorLoginForm, VacanteForm, PostulacionForm, TutorEmpresarialForm, \
    SustentacionForm
from .models import (
    Coordinador, Empresa, Vacante, Estudiante, Postulacion,
    TutorEmpresarial, DocenteAsesor, PracticaEmpresarial,
    Sustentacion, Evaluacion, SeguimientoSemanal
)
from . import serializers
from .forms import SustentacionForm


# ============================================
# AUTENTICACIÓN
# ============================================

def coordinador_login(request):
    """Vista para el login del Coordinador Empresarial"""
    if request.user.is_authenticated:
        return redirect('coordinacion:dashboard')

    if request.method == 'POST':
        form = CoordinadorLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido/a {user.username}!')
            return redirect('coordinacion:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = CoordinadorLoginForm()

    return render(request, 'coordinacion/login.html', {'form': form})


def coordinador_logout(request):
    """Cerrar sesión del Coordinador"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('coordinacion:login')


# ============================================
# DASHBOARD PRINCIPAL
# ============================================

from functools import wraps
from django.http import HttpResponseForbidden

def coordinator_required(view_func):
    """Decorador que exige que el usuario esté autenticado y tenga un objeto `coordinador` asociado."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Si no está autenticado, redirigir al login del coordinador
        if not request.user.is_authenticated:
            return redirect('coordinacion:login')
        # Si no tiene atributo 'coordinador', denegar acceso
        if not hasattr(request.user, 'coordinador'):
            messages.error(request, 'Acceso denegado: se requiere rol Coordinador')
            return HttpResponseForbidden('Acceso denegado')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@coordinator_required
def coordinador_dashboard(request):
    """Dashboard principal del Coordinador Empresarial"""

    # Obtener el nombre del usuario
    nombre_usuario = request.user.username
    if hasattr(request.user, 'coordinador'):
        nombre_usuario = request.user.coordinador.nombre_completo

    # Estadísticas para el dashboard
    stats = {
        'empresas_activas': Empresa.objects.filter(estado='APROBADA').count(),
        'vacantes_disponibles': Vacante.objects.filter(estado='DISPONIBLE').count(),
        'estudiantes_en_practica': PracticaEmpresarial.objects.filter(estado='EN_CURSO').count(),
        'postulaciones_pendientes': Postulacion.objects.filter(estado='POSTULADO').count(),
    }

    # Convertir stats a JSON para React
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    stats_json = json.dumps(stats, cls=DjangoJSONEncoder)

    context = {
        'nombre_usuario': nombre_usuario,
        'stats': stats_json,
    }

    return render(request, 'coordinacion/dashboard.html', context)


# ============================================
# GESTIÓN DE EMPRESAS (RF-01)
# ============================================

@coordinator_required
def empresas_lista(request):
    """Listar todas las empresas registradas"""
    estado_filtro = request.GET.get('estado', '')
    buscar = request.GET.get('buscar', '')

    empresas = Empresa.objects.all()

    if estado_filtro:
        empresas = empresas.filter(estado=estado_filtro)

    if buscar:
        empresas = empresas.filter(
            Q(razon_social__icontains=buscar) |
            Q(nit__icontains=buscar)
        )

    # Serializar empresas para React
    empresas_json = serializers.to_json([
        serializers.serialize_empresa(empresa) for empresa in empresas
    ])

    context = {
        'empresas': empresas_json,
        'estado_filtro': estado_filtro,
        'buscar': buscar,
    }

    return render(request, 'coordinacion/empresas/lista.html', context)


@coordinator_required
def empresa_detalle(request, empresa_id):
    """Ver detalles completos de una empresa"""
    empresa = get_object_or_404(Empresa, id=empresa_id)

    context = {
        'empresa': empresa,
        'vacantes': empresa.vacantes.all(),
        'tutores': empresa.tutores.all(),
        'practicas': empresa.practicas.all(),
    }

    return render(request, 'coordinacion/empresas/detalle.html', context)


@coordinator_required
def empresa_validar(request, empresa_id):
    """Validar/Aprobar o Rechazar una empresa"""
    empresa = get_object_or_404(Empresa, id=empresa_id)

    # Verificar que la empresa esté en estado PENDIENTE
    if empresa.estado != 'PENDIENTE':
        messages.warning(request, f'Esta empresa ya fue {empresa.estado.lower()}')
        return redirect('coordinacion:empresa_detalle', empresa_id=empresa.id)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        observaciones = request.POST.get('observaciones', '').strip()

        # Obtener el coordinador actual
        coordinador = request.user.coordinador

        if accion == 'aprobar':
            empresa.estado = 'APROBADA'
            empresa.fecha_aprobacion = timezone.now()
            empresa.aprobada_por = coordinador
            empresa.observaciones = observaciones if observaciones else 'Empresa aprobada correctamente'
            empresa.save()

            messages.success(
                request,
                f'✅ Empresa "{empresa.razon_social}" aprobada correctamente. Ahora puede crear vacantes de práctica.'
            )

        elif accion == 'rechazar':
            if not observaciones:
                messages.error(request, 'Debes proporcionar observaciones al rechazar una empresa')
                return render(request, 'coordinacion/empresas/validar.html', {'empresa': empresa})

            empresa.estado = 'RECHAZADA'
            empresa.observaciones = observaciones
            empresa.save()

            messages.warning(
                request,
                f'❌ Empresa "{empresa.razon_social}" rechazada. Motivo: {observaciones[:50]}...'
            )

        return redirect('coordinacion:empresa_detalle', empresa_id=empresa.id)

    # GET request - mostrar formulario
    return render(request, 'coordinacion/empresas/validar.html', {'empresa': empresa})


# ============================================
# GESTIÓN DE VACANTES (RF-02)
# ============================================

@coordinator_required
def vacantes_lista(request):
    """Listar todas las vacantes"""
    estado_filtro = request.GET.get('estado', '')

    vacantes = Vacante.objects.select_related('empresa', 'creada_por').all()

    if estado_filtro:
        vacantes = vacantes.filter(estado=estado_filtro)

    # ✅ CORRECCIÓN: Usar el serializador existente
    vacantes_json = serializers.to_json([
        serializers.serialize_vacante(vacante) for vacante in vacantes
    ])

    context = {
        'vacantes': vacantes_json,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'coordinacion/vacantes/lista.html', context)


@coordinator_required
def vacante_crear(request):
    """Crear una nueva vacante oficial"""

    if request.method == 'POST':
        form = VacanteForm(request.POST)
        if form.is_valid():
            vacante = form.save(commit=False)
            vacante.creada_por = request.user.coordinador
            vacante.fecha_publicacion = timezone.now()
            vacante.cupos_ocupados = 0
            vacante.save()

            messages.success(
                request,
                f'✅ Vacante "{vacante.titulo}" creada exitosamente para {vacante.empresa.razon_social}'
            )
            return redirect('coordinacion:vacante_detalle', vacante_id=vacante.id)
        else:
            messages.error(request, '❌ Por favor, corrige los errores en el formulario')
    else:
        form = VacanteForm()

    # Verificar si hay empresas aprobadas
    empresas_aprobadas = Empresa.objects.filter(estado='APROBADA')

    if not empresas_aprobadas.exists():
        messages.warning(
            request,
            'No hay empresas aprobadas. Debes aprobar al menos una empresa antes de crear vacantes.'
        )

    context = {
        'form': form,
        'empresas_aprobadas': empresas_aprobadas,
    }

    return render(request, 'coordinacion/vacantes/crear.html', context)


@coordinator_required
def vacante_editar(request, vacante_id):
    """Editar una vacante existente"""
    vacante = get_object_or_404(Vacante, id=vacante_id)

    # Contar postulaciones activas
    postulaciones_count = vacante.postulaciones.exclude(estado='RECHAZADO').count()

    if request.method == 'POST':
        form = VacanteForm(request.POST, instance=vacante)
        if form.is_valid():
            # Validar que no se reduzcan cupos por debajo de los ocupados
            nueva_cantidad = form.cleaned_data.get('cantidad_cupos')
            if nueva_cantidad < vacante.cupos_ocupados:
                messages.error(
                    request,
                    f'❌ No puedes reducir los cupos por debajo de {vacante.cupos_ocupados} (cupos ya ocupados)'
                )
                return render(request, 'coordinacion/vacantes/editar.html', {
                    'form': form,
                    'vacante': vacante,
                    'postulaciones_count': postulaciones_count,
                })

            vacante = form.save()

            messages.success(
                request,
                f'✅ Vacante "{vacante.titulo}" actualizada exitosamente'
            )
            return redirect('coordinacion:vacante_detalle', vacante_id=vacante.id)
        else:
            messages.error(request, '❌ Por favor, corrige los errores en el formulario')
    else:
        form = VacanteForm(instance=vacante)

    context = {
        'form': form,
        'vacante': vacante,
        'postulaciones_count': postulaciones_count,
    }

    return render(request, 'coordinacion/vacantes/editar.html', context)


@coordinator_required
def vacante_detalle(request, vacante_id):
    """Ver detalles de una vacante"""
    vacante = get_object_or_404(Vacante, id=vacante_id)

    context = {
        'vacante': vacante,
        'postulaciones': vacante.postulaciones.select_related('estudiante').all(),
    }

    return render(request, 'coordinacion/vacantes/detalle.html', context)


# ============================================
# POSTULACIÓN DE ESTUDIANTES (RF-03)
# ============================================

@coordinator_required
def estudiantes_lista(request):
    """Listar estudiantes aptos para postular"""
    estado_filtro = request.GET.get('estado', '')

    estudiantes = Estudiante.objects.all()

    if estado_filtro:
        estudiantes = estudiantes.filter(estado=estado_filtro)

    # Serializar estudiantes para React
    estudiantes_json = serializers.to_json([
        serializers.serialize_estudiante(estudiante) for estudiante in estudiantes
    ])

    context = {
        'estudiantes': estudiantes_json,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'coordinacion/estudiantes/lista.html', context)

@coordinator_required
def estudiante_detalle(request, estudiante_id):
    """
    Ver detalle completo de un estudiante incluyendo:
    - Datos personales y académicos
    - Postulaciones realizadas
    - Práctica actual (si tiene)
    - Historial de prácticas
    """
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)

    # Obtener postulaciones del estudiante
    postulaciones = Postulacion.objects.filter(
        estudiante=estudiante
    ).select_related('vacante', 'vacante__empresa', 'postulado_por').order_by('-fecha_postulacion')

    # Obtener práctica actual (si está en práctica)
    practica_actual = None
    if estudiante.estado == 'EN_PRACTICA':
        practica_actual = PracticaEmpresarial.objects.filter(
            estudiante=estudiante,
            estado__in=['INICIADA', 'EN_CURSO']
        ).select_related('empresa', 'tutor_empresarial', 'docente_asesor').first()

    # Obtener historial de prácticas
    practicas_historial = PracticaEmpresarial.objects.filter(
        estudiante=estudiante
    ).select_related('empresa', 'tutor_empresarial', 'docente_asesor').order_by('-fecha_inicio')

    context = {
        'estudiante': estudiante,
        'postulaciones': postulaciones,
        'practica_actual': practica_actual,
        'practicas_historial': practicas_historial,
    }

    return render(request, 'coordinacion/estudiantes/detalle.html', context)


@coordinator_required
def postulaciones_lista(request):
    """Listar todas las postulaciones"""
    estado_filtro = request.GET.get('estado', '')

    postulaciones = Postulacion.objects.select_related(
        'estudiante', 'vacante', 'vacante__empresa'
    ).all()

    if estado_filtro:
        postulaciones = postulaciones.filter(estado=estado_filtro)

    # Serializar postulaciones para React
    postulaciones_json = serializers.to_json([
        serializers.serialize_postulacion(postulacion) for postulacion in postulaciones
    ])

    context = {
        'postulaciones': postulaciones_json,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'coordinacion/postulaciones/lista.html', context)


@coordinator_required
def postulacion_crear(request):
    """
    RF-03: Crear nueva postulación de estudiante a vacante
    El estudiante queda directamente en estado SELECCIONADO
    """
    if request.method == 'POST':
        form = PostulacionForm(request.POST)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.postulado_por = request.user.coordinador
            postulacion.estado = 'SELECCIONADO'  # ✅ CAMBIO: Directamente SELECCIONADO
            postulacion.fecha_respuesta = timezone.now()  # ✅ NUEVO: Registrar fecha
            postulacion.save()

            messages.success(
                request,
                f'✅ Postulación creada exitosamente. '
                f'{postulacion.estudiante.nombre_completo} está listo para vinculación.'
            )
            return redirect('coordinacion:postulaciones_lista')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'❌ {error}')
    else:
        form = PostulacionForm()

    context = {
        'form': form,
    }

    return render(request, 'coordinacion/postulaciones/crear.html', context)


@coordinator_required
def postulacion_aprobar(request, postulacion_id):
    """
    RF-04: Aprobar o rechazar una postulación seleccionada por la empresa
    Solo se pueden aprobar postulaciones en estado SELECCIONADO
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    # Verificar que la postulación esté en estado SELECCIONADO
    if postulacion.estado != 'SELECCIONADO':
        messages.warning(
            request,
            f'Esta postulación está en estado "{postulacion.get_estado_display()}". '
            f'Solo se pueden aprobar postulaciones seleccionadas por la empresa.'
        )
        return redirect('coordinacion:postulaciones_lista')

    if request.method == 'POST':
        accion = request.POST.get('accion')
        observaciones = request.POST.get('observaciones', '').strip()

        coordinador = request.user.coordinador

        if accion == 'aprobar':
            # APROBAR Y VINCULAR
            postulacion.estado = 'VINCULADO'
            postulacion.fecha_respuesta = timezone.now()
            postulacion.observaciones = observaciones if observaciones else 'Postulación aprobada y estudiante vinculado'
            postulacion.save()

            # Actualizar el estado del estudiante
            postulacion.estudiante.estado = 'EN_PRACTICA'
            postulacion.estudiante.save()

            # Incrementar cupos ocupados de la vacante
            vacante = postulacion.vacante
            vacante.cupos_ocupados += 1

            # Actualizar estado de la vacante si se llenaron todos los cupos
            if vacante.cupos_ocupados >= vacante.cantidad_cupos:
                vacante.estado = 'OCUPADA'

            vacante.save()

            messages.success(
                request,
                f'✅ Postulación aprobada. {postulacion.estudiante.nombre_completo} '
                f'ha sido vinculado a {postulacion.vacante.empresa.razon_social}'
            )

            # Redirigir a crear la práctica empresarial
            return redirect('coordinacion:practica_crear_desde_postulacion', postulacion_id=postulacion.id)

        elif accion == 'rechazar':
            # RECHAZAR POSTULACIÓN
            if not observaciones:
                messages.error(
                    request,
                    'Debes proporcionar observaciones al rechazar una postulación seleccionada'
                )
                return render(request, 'coordinacion/postulaciones/aprobar.html', {
                    'postulacion': postulacion
                })

            postulacion.estado = 'RECHAZADO'
            postulacion.fecha_respuesta = timezone.now()
            postulacion.observaciones = observaciones
            postulacion.save()

            # El estudiante vuelve a estar APTO
            if postulacion.estudiante.estado != 'EN_PRACTICA':
                postulacion.estudiante.estado = 'APTO'
                postulacion.estudiante.save()

            messages.warning(
                request,
                f'❌ Postulación rechazada. Motivo: {observaciones[:100]}'
            )

            return redirect('coordinacion:postulaciones_lista')

    # GET request - mostrar formulario de aprobación
    context = {
        'postulacion': postulacion,
    }

    return render(request, 'coordinacion/postulaciones/aprobar.html', context)

@coordinator_required
def postulacion_detalle(request, postulacion_id):
    """
    Ver detalles completos de una postulación
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    context = {
        'postulacion': postulacion,
    }

    return render(request, 'coordinacion/postulaciones/detalle.html', context)


@coordinator_required
def practica_crear_desde_postulacion(request, postulacion_id):
    """
    Crear automáticamente una práctica empresarial desde una postulación vinculada
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    # Verificar que la postulación esté vinculada
    if postulacion.estado != 'VINCULADO':
        messages.error(request, 'Solo se pueden crear prácticas desde postulaciones vinculadas')
        return redirect('coordinacion:postulaciones_lista')

    # Verificar que no exista ya una práctica para este estudiante y vacante
    practica_existente = PracticaEmpresarial.objects.filter(
        estudiante=postulacion.estudiante,
        vacante=postulacion.vacante
    ).first()

    if practica_existente:
        messages.info(request, 'Ya existe una práctica registrada para este estudiante')
        return redirect('coordinacion:practica_detalle', practica_id=practica_existente.id)

    # Obtener tutores y docentes disponibles
    tutores = TutorEmpresarial.objects.filter(
        empresa=postulacion.vacante.empresa,
        activo=True
    )
    docentes = DocenteAsesor.objects.filter(activo=True)

    if request.method == 'POST':
        tutor_id = request.POST.get('tutor_empresarial')
        docente_id = request.POST.get('docente_asesor')
        fecha_inicio = request.POST.get('fecha_inicio')
        duracion_meses = int(request.POST.get('duracion_meses', postulacion.vacante.duracion_meses))

        # Validaciones
        if not tutor_id:
            messages.error(request, 'Debes seleccionar un tutor empresarial')
            return render(request, 'coordinacion/practicas/crear_desde_postulacion.html', {
                'postulacion': postulacion,
                'tutores': tutores,
                'docentes': docentes,
            })

        if not docente_id:
            messages.error(request, 'Debes seleccionar un docente asesor')
            return render(request, 'coordinacion/practicas/crear_desde_postulacion.html', {
                'postulacion': postulacion,
                'tutores': tutores,
                'docentes': docentes,
            })

        # Crear la práctica empresarial
        from datetime import datetime, timedelta

        fecha_inicio_date = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_estimada = fecha_inicio_date + timedelta(days=duracion_meses * 30)

        practica = PracticaEmpresarial.objects.create(
            estudiante=postulacion.estudiante,
            empresa=postulacion.vacante.empresa,
            vacante=postulacion.vacante,
            tutor_empresarial_id=tutor_id,
            docente_asesor_id=docente_id,
            fecha_inicio=fecha_inicio_date,
            fecha_fin_estimada=fecha_fin_estimada,
            estado='EN_CURSO',  # ✅ CAMBIADO DE 'INICIADA' A 'EN_CURSO'
            plan_aprobado=False,
            asignada_por=request.user.coordinador,
            observaciones=f'Práctica creada desde postulación #{postulacion.id}'
        )

        messages.success(
            request,
            f'✅ Práctica empresarial creada exitosamente para {practica.estudiante.nombre_completo}'
        )

        return redirect('coordinacion:practica_detalle', practica_id=practica.id)

    # GET request
    context = {
        'postulacion': postulacion,
        'tutores': tutores,
        'docentes': docentes,
    }

    return render(request, 'coordinacion/practicas/crear_desde_postulacion.html', context)

@coordinator_required
def postulacion_editar(request, postulacion_id):
    """
    Editar una postulación existente (solo si está en estado POSTULADO)
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    # Verificar que la postulación esté en estado POSTULADO
    if postulacion.estado != 'POSTULADO':
        messages.warning(
            request,
            f'No se puede editar una postulación en estado "{postulacion.get_estado_display()}"'
        )
        return redirect('coordinacion:postulacion_detalle', postulacion_id=postulacion.id)

    if request.method == 'POST':
        form = PostulacionForm(request.POST, instance=postulacion)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Postulación actualizada exitosamente')
            return redirect('coordinacion:postulacion_detalle', postulacion_id=postulacion.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'❌ {error}')
    else:
        form = PostulacionForm(instance=postulacion)

    context = {
        'form': form,
        'postulacion': postulacion,
    }

    return render(request, 'coordinacion/postulaciones/editar.html', context)


@coordinator_required
def postulacion_eliminar(request, postulacion_id):
    """
    Eliminar una postulación (solo si está en estado POSTULADO)
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    # Verificar que la postulación esté en estado POSTULADO
    if postulacion.estado != 'POSTULADO':
        messages.warning(
            request,
            f'No se puede eliminar una postulación en estado "{postulacion.get_estado_display()}"'
        )
        return redirect('coordinacion:postulacion_detalle', postulacion_id=postulacion.id)

    if request.method == 'POST':
        estudiante_nombre = postulacion.estudiante.nombre_completo
        vacante_titulo = postulacion.vacante.titulo

        postulacion.delete()

        messages.success(
            request,
            f'✅ Postulación eliminada: {estudiante_nombre} - {vacante_titulo}'
        )
        return redirect('coordinacion:postulaciones_lista')

    # Si es GET, redirigir al detalle
    return redirect('coordinacion:postulacion_detalle', postulacion_id=postulacion.id)

@coordinator_required
def postulacion_rechazar(request, postulacion_id):
    """
    Rechazar una postulación directamente desde la lista
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    # Verificar que la postulación esté en estado SELECCIONADO
    if postulacion.estado != 'SELECCIONADO':
        messages.warning(
            request,
            f'Esta postulación está en estado "{postulacion.get_estado_display()}". '
            f'Solo se pueden rechazar postulaciones seleccionadas.'
        )
        return redirect('coordinacion:postulaciones_lista')

    if request.method == 'POST':
        observaciones = request.POST.get('observaciones', '').strip()

        if not observaciones:
            messages.error(request, 'Debes proporcionar un motivo para rechazar')
            return render(request, 'coordinacion/postulaciones/rechazar.html', {
                'postulacion': postulacion
            })

        # Rechazar postulación
        postulacion.estado = 'RECHAZADO'
        postulacion.fecha_respuesta = timezone.now()
        postulacion.observaciones = observaciones
        postulacion.save()

        # El estudiante vuelve a estar APTO
        if postulacion.estudiante.estado != 'EN_PRACTICA':
            postulacion.estudiante.estado = 'APTO'
            postulacion.estudiante.save()

        messages.warning(
            request,
            f'❌ Postulación rechazada: {postulacion.estudiante.nombre_completo}'
        )

        return redirect('coordinacion:postulaciones_lista')

    # GET request - mostrar formulario
    context = {
        'postulacion': postulacion,
    }

    return render(request, 'coordinacion/postulaciones/rechazar.html', context)




# ============================================
# ASIGNACIÓN DE TUTORES Y DOCENTES (RF-05)
# ============================================

@coordinator_required
def tutores_lista(request):
    """Listar tutores empresariales con filtros"""
    busqueda = request.GET.get('busqueda', '')
    filtro_activo = request.GET.get('activo', '')
    filtro_empresa = request.GET.get('empresa', '')

    tutores = TutorEmpresarial.objects.select_related('empresa').all()

    # Aplicar filtros
    if filtro_activo != '':
        activo = filtro_activo == 'true'
        tutores = tutores.filter(activo=activo)

    if filtro_empresa:
        tutores = tutores.filter(empresa_id=filtro_empresa)

    if busqueda:
        tutores = tutores.filter(
            Q(nombre_completo__icontains=busqueda) |
            Q(cargo__icontains=busqueda) |
            Q(email__icontains=busqueda) |
            Q(empresa__razon_social__icontains=busqueda)
        )

    # Obtener lista de empresas para el filtro
    empresas = Empresa.objects.filter(estado='APROBADA').order_by('razon_social')

    # Serializar tutores para React
    tutores_json = serializers.to_json([
        serializers.serialize_tutor(tutor) for tutor in tutores
    ])

    empresas_json = serializers.to_json([
        {'id': e.id, 'razon_social': e.razon_social} for e in empresas
    ])

    context = {
        'tutores': tutores_json,
        'empresas': empresas_json,
        'busqueda': busqueda,
        'filtro_activo': filtro_activo,
        'filtro_empresa': filtro_empresa,
    }

    return render(request, 'coordinacion/tutores/lista.html', context)

@coordinator_required
def tutor_crear(request):
    """Crear un nuevo tutor empresarial"""
    if request.method == 'POST':
        form = TutorEmpresarialForm(request.POST)
        if form.is_valid():
            tutor = form.save()
            messages.success(
                request,
                f'✅ Tutor "{tutor.nombre_completo}" creado exitosamente para {tutor.empresa.razon_social}'
            )
            return redirect('coordinacion:tutor_detalle', tutor_id=tutor.id)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = TutorEmpresarialForm()

    # Verificar si hay empresas aprobadas
    empresas_aprobadas = Empresa.objects.filter(estado='APROBADA')
    if not empresas_aprobadas.exists():
        messages.warning(
            request,
            'No hay empresas aprobadas. Debes aprobar al menos una empresa antes de crear tutores.'
        )

    context = {
        'form': form,
        'empresas_aprobadas': empresas_aprobadas,
    }

    return render(request, 'coordinacion/tutores/crear.html', context)

@coordinator_required
def tutor_detalle(request, tutor_id):
    """Ver detalles completos de un tutor empresarial"""
    tutor = get_object_or_404(
        TutorEmpresarial.objects.select_related('empresa'),
        id=tutor_id
    )

    # Obtener prácticas que supervisa este tutor
    practicas = PracticaEmpresarial.objects.filter(
        tutor_empresarial=tutor
    ).select_related('estudiante', 'empresa', 'docente_asesor').order_by('-fecha_inicio')

    # Estadísticas
    practicas_activas = practicas.filter(estado='EN_CURSO').count()
    practicas_finalizadas = practicas.filter(estado='FINALIZADA').count()

    context = {
        'tutor': tutor,
        'practicas': practicas,
        'practicas_activas': practicas_activas,
        'practicas_finalizadas': practicas_finalizadas,
        'total_practicas': practicas.count(),
    }

    return render(request, 'coordinacion/tutores/detalle.html', context)


@coordinator_required
def tutor_editar(request, tutor_id):
    """Editar un tutor empresarial existente"""
    tutor = get_object_or_404(TutorEmpresarial, id=tutor_id)

    # Verificar si tiene prácticas activas
    practicas_activas = PracticaEmpresarial.objects.filter(
        tutor_empresarial=tutor,
        estado='EN_CURSO'
    ).count()

    if request.method == 'POST':
        form = TutorEmpresarialForm(request.POST, instance=tutor)
        if form.is_valid():
            tutor = form.save()
            messages.success(
                request,
                f'✅ Tutor "{tutor.nombre_completo}" actualizado exitosamente'
            )
            return redirect('coordinacion:tutor_detalle', tutor_id=tutor.id)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = TutorEmpresarialForm(instance=tutor)

    context = {
        'form': form,
        'tutor': tutor,
        'practicas_activas': practicas_activas,
    }

    return render(request, 'coordinacion/tutores/editar.html', context)


@coordinator_required
def tutor_toggle_activo(request, tutor_id):
    """Activar/Desactivar un tutor empresarial"""
    tutor = get_object_or_404(TutorEmpresarial, id=tutor_id)

    if request.method == 'POST':
        # Verificar si tiene prácticas activas antes de desactivar
        if tutor.activo:
            practicas_activas = PracticaEmpresarial.objects.filter(
                tutor_empresarial=tutor,
                estado='EN_CURSO'
            ).count()

            if practicas_activas > 0:
                messages.error(
                    request,
                    f'❌ No se puede desactivar este tutor porque tiene {practicas_activas} práctica(s) activa(s)'
                )
                return redirect('coordinacion:tutor_detalle', tutor_id=tutor.id)

        # Toggle del estado
        tutor.activo = not tutor.activo
        tutor.save()

        estado = 'activado' if tutor.activo else 'desactivado'
        messages.success(
            request,
            f'✅ Tutor "{tutor.nombre_completo}" {estado} exitosamente'
        )

        return redirect('coordinacion:tutor_detalle', tutor_id=tutor.id)

    # Si es GET, redirigir al detalle
    return redirect('coordinacion:tutor_detalle', tutor_id=tutor.id)


@coordinator_required
def docentes_lista(request):
    """Listar docentes asesores"""
    docentes = DocenteAsesor.objects.filter(activo=True)

    context = {
        'docentes': docentes,
    }

    return render(request, 'coordinacion/docentes/lista.html', context)


@coordinator_required
def practica_asignar(request, postulacion_id):
    """Asignar tutor y docente a una práctica"""
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    tutores = TutorEmpresarial.objects.filter(
        empresa=postulacion.vacante.empresa,
        activo=True
    )
    docentes = DocenteAsesor.objects.filter(activo=True)

    if request.method == 'POST':
        # Procesar asignación
        messages.success(request, 'Tutor y docente asignados correctamente')
        return redirect('coordinacion:practicas_lista')

    context = {
        'postulacion': postulacion,
        'tutores': tutores,
        'docentes': docentes,
    }

    return render(request, 'coordinacion/practicas/asignar.html', context)


# ============================================
# GESTIÓN DE PRÁCTICAS
# ============================================

@coordinator_required
def practicas_lista(request):
    """Listar todas las prácticas"""
    estado_filtro = request.GET.get('estado', '')

    practicas = PracticaEmpresarial.objects.select_related(
        'estudiante', 'empresa', 'tutor_empresarial', 'docente_asesor'
    ).all()

    if estado_filtro:
        practicas = practicas.filter(estado=estado_filtro)

    # Serializar prácticas para React
    practicas_json = serializers.to_json([
        serializers.serialize_practica(practica) for practica in practicas
    ])

    print(f"DEBUG: Total prácticas: {practicas.count()}")  # ✅ AÑADIR ESTA LÍNEA PARA DEBUG
    print(f"DEBUG: JSON generado: {practicas_json[:200]}")  # ✅ VER LOS PRIMEROS 200 CARACTERES

    context = {
        'practicas': practicas_json,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'coordinacion/practicas/lista.html', context)


@coordinator_required
def practica_detalle(request, practica_id):
    """
    Ver detalle completo de una práctica empresarial
    """
    practica = get_object_or_404(
        PracticaEmpresarial.objects.select_related(
            'estudiante',
            'empresa',
            'vacante',
            'tutor_empresarial',
            'docente_asesor',
            'asignada_por'
        ),
        id=practica_id
    )

    context = {
        'practica': practica,
    }

    return render(request, 'coordinacion/practicas/detalle.html', context)


@coordinator_required
def practica_cancelar(request, practica_id):
    """
    Cancelar una práctica empresarial con motivo
    Solo se pueden cancelar prácticas en estado EN_CURSO
    """
    practica = get_object_or_404(PracticaEmpresarial, id=practica_id)

    # ✅ ACTUALIZADO: Solo verificar EN_CURSO
    if practica.estado != 'EN_CURSO':
        messages.warning(
            request,
            f'No se puede cancelar una práctica en estado "{practica.get_estado_display()}"'
        )
        return redirect('coordinacion:practica_detalle', practica_id=practica.id)

    if request.method == 'POST':
        motivo_cancelacion = request.POST.get('motivo_cancelacion', '').strip()

        if not motivo_cancelacion or len(motivo_cancelacion) < 20:
            messages.error(
                request,
                'Debes proporcionar un motivo de cancelación con al menos 20 caracteres'
            )
            return render(request, 'coordinacion/practicas/cancelar.html', {
                'practica': practica
            })

        # Cancelar la práctica
        practica.estado = 'CANCELADA'
        practica.fecha_fin = timezone.now().date()

        # Agregar motivo a observaciones
        if practica.observaciones:
            practica.observaciones += f"\n\n--- CANCELACIÓN ---\nFecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}\nMotivo: {motivo_cancelacion}"
        else:
            practica.observaciones = f"PRÁCTICA CANCELADA\nFecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}\nMotivo: {motivo_cancelacion}"

        practica.save()

        # Actualizar estado del estudiante a APTO
        estudiante = practica.estudiante
        estudiante.estado = 'APTO'
        estudiante.save()

        # Liberar cupo de la vacante
        vacante = practica.vacante
        if vacante and vacante.cupos_ocupados > 0:
            vacante.cupos_ocupados -= 1

            # Si la vacante estaba ocupada y ahora tiene cupos, cambiar a disponible
            if vacante.estado == 'OCUPADA' and vacante.cupos_ocupados < vacante.cantidad_cupos:
                vacante.estado = 'DISPONIBLE'

            vacante.save()

        messages.warning(
            request,
            f'⚠️ Práctica cancelada: {estudiante.nombre_completo} - {practica.empresa.razon_social}'
        )

        return redirect('coordinacion:practicas_lista')

    # GET request - mostrar formulario
    context = {
        'practica': practica,
    }

    return render(request, 'coordinacion/practicas/cancelar.html', context)

@coordinator_required
def practica_cerrar(request, practica_id):
    """Cerrar una práctica empresarial"""
    practica = get_object_or_404(PracticaEmpresarial, id=practica_id)

    # Validar requisitos
    checklist = {
        'plan_aprobado': practica.plan_aprobado,
        'evaluaciones_completas': practica.evaluaciones.count() >= 2,
        'seguimientos_completos': practica.seguimientos.count() >= 4,
        'sustentacion_realizada': hasattr(practica, 'sustentacion') and practica.sustentacion.estado == 'APROBADA',
    }

    puede_cerrar = all(checklist.values())

    if request.method == 'POST' and puede_cerrar:
        practica.estado = 'FINALIZADA'
        practica.fecha_fin_real = timezone.now().date()
        practica.save()

        # Actualizar estado del estudiante
        practica.estudiante.estado = 'FINALIZADO'
        practica.estudiante.save()

        messages.success(request, f'Práctica de {practica.estudiante.nombre_completo} cerrada exitosamente')
        return redirect('coordinacion:practicas_lista')

    context = {
        'practica': practica,
        'checklist': checklist,
        'puede_cerrar': puede_cerrar,
    }

    return render(request, 'coordinacion/practicas/cerrar.html', context)

@coordinator_required
def practica_finalizar(request, practica_id):
    """
    Marcar una práctica como finalizada exitosamente
    """
    practica = get_object_or_404(PracticaEmpresarial, id=practica_id)

    # Verificar que la práctica esté EN_CURSO
    if practica.estado != 'EN_CURSO':
        messages.warning(
            request,
            f'Solo se pueden finalizar prácticas en estado "En Curso"'
        )
        return redirect('coordinacion:practica_detalle', practica_id=practica.id)

    if request.method == 'POST':
        # Finalizar la práctica
        practica.estado = 'FINALIZADA'
        practica.fecha_fin = timezone.now().date()
        practica.save()

        # Actualizar estado del estudiante
        estudiante = practica.estudiante
        estudiante.estado = 'FINALIZADO'
        estudiante.save()

        messages.success(
            request,
            f'✅ Práctica finalizada exitosamente: {estudiante.nombre_completo}'
        )

        return redirect('coordinacion:practica_detalle', practica_id=practica.id)

    # Si es GET, redirigir al detalle
    return redirect('coordinacion:practica_detalle', practica_id=practica.id)


# ============================================
# GESTIÓN DE SUSTENTACIONES (RF-09)
# ============================================

# ============================================
# GESTIÓN DE SUSTENTACIONES (RF-09)
# ============================================

@coordinator_required
def sustentaciones_lista(request):
    """Listar sustentaciones con filtros"""
    estado_filtro = request.GET.get('estado', '')
    busqueda = request.GET.get('busqueda', '')

    sustentaciones = Sustentacion.objects.select_related(
        'practica', 'practica__estudiante', 'jurado_1', 'jurado_2', 'registrada_por'
    ).all()

    # Aplicar filtros
    if estado_filtro:
        sustentaciones = sustentaciones.filter(estado=estado_filtro)

    if busqueda:
        sustentaciones = sustentaciones.filter(
            Q(practica__estudiante__nombre_completo__icontains=busqueda) |
            Q(lugar__icontains=busqueda) |
            Q(jurado_1__nombre_completo__icontains=busqueda)
        )

    # Serializar sustentaciones para React
    sustentaciones_json = serializers.to_json([
        serializers.serialize_sustentacion(sustentacion) for sustentacion in sustentaciones
    ])

    context = {
        'sustentaciones': sustentaciones_json,
        'estado_filtro': estado_filtro,
        'busqueda': busqueda,
    }

    return render(request, 'coordinacion/sustentaciones/lista.html', context)


@coordinator_required
def sustentacion_crear(request):
    """Crear una nueva sustentación"""
    if request.method == 'POST':
        form = SustentacionForm(request.POST, request.FILES)
        if form.is_valid():
            sustentacion = form.save(commit=False)
            sustentacion.estado = 'PROGRAMADA'
            sustentacion.registrada_por = request.user.coordinador
            try:
                sustentacion.save()
            except IntegrityError:
                # Probable conflicto: ya existe una sustentación para esa práctica
                messages.error(request, '❌ Ya existe una sustentación registrada para la práctica seleccionada')
                return render(request, 'coordinacion/sustentaciones/crear.html', {
                    'form': form,
                    'practicas_disponibles': PracticaEmpresarial.objects.filter(estado='FINALIZADA', sustentacion__isnull=True).count()
                })

            messages.success(
                request,
                f'✅ Sustentación programada exitosamente para {sustentacion.practica.estudiante.nombre_completo}'
            )
            return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = SustentacionForm()

    # Verificar si hay prácticas disponibles
    practicas_disponibles = PracticaEmpresarial.objects.filter(
        estado='FINALIZADA',
        sustentacion__isnull=True
    ).count()

    if practicas_disponibles == 0:
        messages.warning(
            request,
            'No hay prácticas finalizadas sin sustentación. Debes finalizar al menos una práctica primero.'
        )

    context = {
        'form': form,
        'practicas_disponibles': practicas_disponibles,
    }

    return render(request, 'coordinacion/sustentaciones/crear.html', context)


@coordinator_required
def sustentacion_detalle(request, sustentacion_id):
    """Ver detalles completos de una sustentación"""
    sustentacion = get_object_or_404(
        Sustentacion.objects.select_related(
            'practica',
            'practica__estudiante',
            'practica__empresa',
            'jurado_1',
            'jurado_2',
            'registrada_por'
        ),
        id=sustentacion_id
    )

    context = {
        'sustentacion': sustentacion,
    }

    return render(request, 'coordinacion/sustentaciones/detalle.html', context)


@coordinator_required
def sustentacion_editar(request, sustentacion_id):
    """Editar una sustentación (solo si está PROGRAMADA)"""
    sustentacion = get_object_or_404(Sustentacion, id=sustentacion_id)

    # Solo se pueden editar sustentaciones programadas
    if sustentacion.estado != 'PROGRAMADA':
        messages.warning(
            request,
            f'No se puede editar una sustentación en estado "{sustentacion.get_estado_display()}"'
        )
        return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

    if request.method == 'POST':
        form = SustentacionForm(request.POST, instance=sustentacion)
        if form.is_valid():
            sustentacion = form.save()
            messages.success(
                request,
                f'✅ Sustentación actualizada exitosamente'
            )
            return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = SustentacionForm(instance=sustentacion)

    context = {
        'form': form,
        'sustentacion': sustentacion,
    }

    return render(request, 'coordinacion/sustentaciones/editar.html', context)


@coordinator_required
def sustentacion_eliminar(request, sustentacion_id):
    """Eliminar una sustentación (solo si está PROGRAMADA)"""
    sustentacion = get_object_or_404(Sustentacion, id=sustentacion_id)

    # Solo se pueden eliminar sustentaciones programadas
    if sustentacion.estado != 'PROGRAMADA':
        messages.warning(
            request,
            f'No se puede eliminar una sustentación en estado "{sustentacion.get_estado_display()}"'
        )
        return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

    if request.method == 'POST':
        estudiante = sustentacion.practica.estudiante.nombre_completo
        sustentacion.delete()

        messages.success(
            request,
            f'✅ Sustentación eliminada: {estudiante}'
        )
        return redirect('coordinacion:sustentaciones_lista')

    # GET: mostrar confirmación
    context = {
        'sustentacion': sustentacion,
    }

    return render(request, 'coordinacion/sustentaciones/eliminar.html', context)


@coordinator_required
def sustentacion_cancelar(request, sustentacion_id):
    """Cancelar una sustentación (solo si está PROGRAMADA)"""
    sustentacion = get_object_or_404(Sustentacion, id=sustentacion_id)

    # Solo se pueden cancelar sustentaciones programadas
    if sustentacion.estado != 'PROGRAMADA':
        messages.warning(
            request,
            f'No se puede cancelar una sustentación en estado "{sustentacion.get_estado_display()}"'
        )
        return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

    if request.method == 'POST':
        motivo = request.POST.get('motivo', '').strip()

        if not motivo or len(motivo) < 10:
            messages.error(
                request,
                'Debes proporcionar un motivo de cancelación con al menos 10 caracteres'
            )
            return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

        # Cancelar sustentación
        sustentacion.estado = 'CANCELADA'

        # Agregar motivo a observaciones
        if sustentacion.observaciones:
            sustentacion.observaciones += f"\n\n--- CANCELACIÓN ---\nFecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}\nMotivo: {motivo}"
        else:
            sustentacion.observaciones = f"SUSTENTACIÓN CANCELADA\nFecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}\nMotivo: {motivo}"

        sustentacion.save()

        messages.warning(
            request,
            f'⚠️ Sustentación cancelada: {sustentacion.practica.estudiante.nombre_completo}'
        )

        return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

    # Si es POST sin motivo o GET, redirigir al detalle
    return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)


@coordinator_required
def sustentacion_aprobar(request, sustentacion_id):
    """Aprobar una sustentación y registrar calificación"""
    sustentacion = get_object_or_404(Sustentacion, id=sustentacion_id)

    # Solo se pueden aprobar sustentaciones programadas
    if sustentacion.estado != 'PROGRAMADA':
        messages.warning(
            request,
            f'Solo se pueden aprobar sustentaciones programadas'
        )
        return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

    if request.method == 'POST':
        try:
            calificacion = float(request.POST.get('calificacion', 0))
            observaciones = request.POST.get('observaciones', '').strip()

            # Validar calificación
            if calificacion < 0 or calificacion > 5:
                messages.error(request, 'La calificación debe estar entre 0.0 y 5.0')
                return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

            # Aprobar sustentación
            sustentacion.estado = 'APROBADA'
            sustentacion.calificacion = calificacion

            if observaciones:
                if sustentacion.observaciones:
                    sustentacion.observaciones += f"\n\n--- APROBACIÓN ---\n{observaciones}"
                else:
                    sustentacion.observaciones = observaciones

            sustentacion.save()

            messages.success(
                request,
                f'✅ Sustentación aprobada con calificación {calificacion}'
            )

            return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

        except ValueError:
            messages.error(request, 'Calificación inválida')
            return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

    return redirect('coordinacion:sustentacion_detalle', sustentacion_id=sustentacion.id)

# ============================================
# REPORTES E INDICADORES (RF-12)
# ============================================

@coordinator_required
def reportes_dashboard(request):
    """Dashboard de reportes e indicadores"""

    # Estadísticas generales
    estadisticas = {
        'total_empresas': Empresa.objects.count(),
        'empresas_activas': Empresa.objects.filter(estado='APROBADA').count(),
        'total_vacantes': Vacante.objects.count(),
        'vacantes_disponibles': Vacante.objects.filter(estado='DISPONIBLE').count(),
        'total_estudiantes': Estudiante.objects.count(),
        'estudiantes_activos': Estudiante.objects.filter(estado='EN_PRACTICA').count(),
        'practicas_finalizadas': PracticaEmpresarial.objects.filter(estado='FINALIZADA').count(),
        'practicas_en_curso': PracticaEmpresarial.objects.filter(estado='EN_CURSO').count(),
    }

    # Empresas con más prácticas
    empresas_top = Empresa.objects.annotate(
        num_practicas=Count('practicas')
    ).order_by('-num_practicas')[:5]

    # ✅ CORRECCIÓN: Usar serialización consistente
    import json
    from django.core.serializers.json import DjangoJSONEncoder

    estadisticas_json = json.dumps(estadisticas, cls=DjangoJSONEncoder)
    empresas_top_json = json.dumps([
        {
            'id': empresa.id,
            'razon_social': empresa.razon_social,
            'nit': empresa.nit,
            'ciudad': empresa.ciudad,
            'num_practicas': empresa.num_practicas
        }
        for empresa in empresas_top
    ], cls=DjangoJSONEncoder)

    context = {
        'estadisticas': estadisticas_json,
        'empresas_top': empresas_top_json,
    }

    return render(request, 'coordinacion/reportes/dashboard.html', context)

