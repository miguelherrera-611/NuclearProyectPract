from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .forms import CoordinadorLoginForm
from .models import (
    Coordinador, Empresa, Vacante, Estudiante, Postulacion,
    TutorEmpresarial, DocenteAsesor, PracticaEmpresarial,
    Sustentacion, Evaluacion, SeguimientoSemanal
)
from . import serializers


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

@login_required
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

@login_required
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


@login_required
def empresa_detalle(request, empresa_id):
    """Ver detalles de una empresa"""
    empresa = get_object_or_404(Empresa, id=empresa_id)

    context = {
        'empresa': empresa,
        'vacantes': empresa.vacantes.all(),
        'tutores': empresa.tutores.all(),
        'practicas': empresa.practicas.all(),
    }

    return render(request, 'coordinacion/empresas/detalle.html', context)


@login_required
def empresa_validar(request, empresa_id):
    """Validar/Aprobar o Rechazar una empresa"""
    empresa = get_object_or_404(Empresa, id=empresa_id)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        observaciones = request.POST.get('observaciones', '')

        coordinador = request.user.coordinador

        if accion == 'aprobar':
            empresa.estado = 'APROBADA'
            empresa.fecha_aprobacion = timezone.now()
            empresa.aprobada_por = coordinador
            empresa.observaciones = observaciones
            empresa.save()
            messages.success(request, f'Empresa {empresa.razon_social} aprobada correctamente')

        elif accion == 'rechazar':
            empresa.estado = 'RECHAZADA'
            empresa.observaciones = observaciones
            empresa.save()
            messages.warning(request, f'Empresa {empresa.razon_social} rechazada')

        return redirect('coordinacion:empresa_detalle', empresa_id=empresa.id)

    return render(request, 'coordinacion/empresas/validar.html', {'empresa': empresa})


# ============================================
# GESTIÓN DE VACANTES (RF-02)
# ============================================

@login_required
def vacantes_lista(request):
    """Listar todas las vacantes"""
    estado_filtro = request.GET.get('estado', '')

    vacantes = Vacante.objects.select_related('empresa', 'creada_por').all()

    if estado_filtro:
        vacantes = vacantes.filter(estado=estado_filtro)

    # Serializar vacantes para React
    vacantes_json = serializers.to_json([
        serializers.serialize_vacante(vacante) for vacante in vacantes
    ])

    context = {
        'vacantes': vacantes_json,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'coordinacion/vacantes/lista.html', context)


@login_required
def vacante_crear(request):
    """Crear una nueva vacante oficial"""
    empresas_aprobadas = Empresa.objects.filter(estado='APROBADA')

    if request.method == 'POST':
        # Aquí procesarías el formulario
        # Por ahora solo un placeholder
        messages.success(request, 'Vacante creada exitosamente')
        return redirect('coordinacion:vacantes_lista')

    context = {
        'empresas': empresas_aprobadas,
    }

    return render(request, 'coordinacion/vacantes/crear.html', context)


@login_required
def vacante_detalle(request, vacante_id):
    """Ver detalles de una vacante"""
    vacante = get_object_or_404(Vacante, id=vacante_id)

    context = {
        'vacante': vacante,
        'postulaciones': vacante.postulaciones.all(),
    }

    return render(request, 'coordinacion/vacantes/detalle.html', context)


# ============================================
# POSTULACIÓN DE ESTUDIANTES (RF-03)
# ============================================

@login_required
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


@login_required
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


@login_required
def postulacion_crear(request):
    """Crear una nueva postulación"""
    estudiantes = Estudiante.objects.filter(estado='APTO')
    vacantes = Vacante.objects.filter(estado='DISPONIBLE')

    if request.method == 'POST':
        # Procesar formulario
        messages.success(request, 'Estudiante postulado exitosamente')
        return redirect('coordinacion:postulaciones_lista')

    context = {
        'estudiantes': estudiantes,
        'vacantes': vacantes,
    }

    return render(request, 'coordinacion/postulaciones/crear.html', context)


# ============================================
# ASIGNACIÓN DE TUTORES Y DOCENTES (RF-05)
# ============================================

@login_required
def tutores_lista(request):
    """Listar tutores empresariales"""
    tutores = TutorEmpresarial.objects.select_related('empresa').all()

    # Serializar tutores para React
    tutores_json = serializers.to_json([
        serializers.serialize_tutor(tutor) for tutor in tutores
    ])

    context = {
        'tutores': tutores_json,
    }

    return render(request, 'coordinacion/tutores/lista.html', context)


@login_required
def docentes_lista(request):
    """Listar docentes asesores"""
    docentes = DocenteAsesor.objects.filter(activo=True)

    context = {
        'docentes': docentes,
    }

    return render(request, 'coordinacion/docentes/lista.html', context)


@login_required
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

@login_required
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

    context = {
        'practicas': practicas_json,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'coordinacion/practicas/lista.html', context)


@login_required
def practica_detalle(request, practica_id):
    """Ver detalles de una práctica"""
    practica = get_object_or_404(PracticaEmpresarial, id=practica_id)

    context = {
        'practica': practica,
        'seguimientos': practica.seguimientos.all(),
        'evaluaciones': practica.evaluaciones.all(),
    }

    return render(request, 'coordinacion/practicas/detalle.html', context)


# ============================================
# GESTIÓN DE SUSTENTACIONES (RF-09)
# ============================================

@login_required
def sustentaciones_lista(request):
    """Listar sustentaciones"""
    sustentaciones = Sustentacion.objects.select_related(
        'practica', 'practica__estudiante', 'jurado_1', 'jurado_2'
    ).all()

    # Serializar sustentaciones para React
    sustentaciones_json = serializers.to_json([
        serializers.serialize_sustentacion(sustentacion) for sustentacion in sustentaciones
    ])

    context = {
        'sustentaciones': sustentaciones_json,
    }

    return render(request, 'coordinacion/sustentaciones/lista.html', context)


@login_required
def sustentacion_crear(request, practica_id):
    """Registrar una nueva sustentación"""
    practica = get_object_or_404(PracticaEmpresarial, id=practica_id)
    docentes = DocenteAsesor.objects.filter(activo=True)

    if request.method == 'POST':
        # Procesar formulario
        messages.success(request, 'Sustentación registrada exitosamente')
        return redirect('coordinacion:sustentaciones_lista')

    context = {
        'practica': practica,
        'docentes': docentes,
    }

    return render(request, 'coordinacion/sustentaciones/crear.html', context)


# ============================================
# CIERRE DE PRÁCTICAS (RF-11)
# ============================================

@login_required
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


# ============================================
# REPORTES E INDICADORES (RF-12)
# ============================================

@login_required
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

    # Serializar datos
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