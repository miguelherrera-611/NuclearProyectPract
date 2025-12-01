"""
Vistas para gestión de Docentes Asesores desde Coordinación
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden

from .models import DocenteAsesor, PracticaEmpresarial, SeguimientoSemanal
from .forms import DocenteAsesorForm


def coordinator_required(view_func):
    """Decorador para proteger rutas de coordinador."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_unificado')
        if not hasattr(request.user, 'coordinador'):
            messages.error(request, 'Acceso denegado: se requiere rol Coordinador')
            return HttpResponseForbidden('Acceso denegado')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@coordinator_required
def docentes_asesores_lista(request):
    """Lista de todos los docentes asesores"""
    docentes = DocenteAsesor.objects.all().order_by('nombre_completo')

    # Filtros
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro == 'activos':
        docentes = docentes.filter(activo=True)
    elif estado_filtro == 'inactivos':
        docentes = docentes.filter(activo=False)

    # Agregar estadísticas a cada docente
    for docente in docentes:
        docente.practicas_activas = PracticaEmpresarial.objects.filter(
            docente_asesor=docente,
            estado='EN_CURSO'
        ).count()
        docente.seguimientos_pendientes = SeguimientoSemanal.objects.filter(
            practica__docente_asesor=docente,
            estado='PENDIENTE'
        ).count()

    context = {
        'docentes': docentes,
        'estado_filtro': estado_filtro,
    }

    return render(request, 'coordinacion/docentes_asesores/lista.html', context)


@coordinator_required
def docente_asesor_crear(request):
    """Crear un nuevo docente asesor"""
    if request.method == 'POST':
        form = DocenteAsesorForm(request.POST)
        if form.is_valid():
            docente = form.save()
            messages.success(request, f'✅ Docente Asesor "{docente.nombre_completo}" creado correctamente')
            return redirect('coordinacion:docente_asesor_detalle', docente_id=docente.id)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = DocenteAsesorForm()

    return render(request, 'coordinacion/docentes_asesores/crear.html', {'form': form})


@coordinator_required
def docente_asesor_editar(request, docente_id):
    """Editar un docente asesor existente"""
    docente = get_object_or_404(DocenteAsesor, id=docente_id)

    if request.method == 'POST':
        form = DocenteAsesorForm(request.POST, instance=docente)
        if form.is_valid():
            docente = form.save()
            messages.success(request, f'✅ Docente Asesor "{docente.nombre_completo}" actualizado correctamente')
            return redirect('coordinacion:docente_asesor_detalle', docente_id=docente.id)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = DocenteAsesorForm(instance=docente)

    return render(request, 'coordinacion/docentes_asesores/editar.html', {
        'form': form,
        'docente': docente
    })


@coordinator_required
def docente_asesor_detalle(request, docente_id):
    """Ver detalles de un docente asesor y sus estudiantes asignados"""
    docente = get_object_or_404(DocenteAsesor, id=docente_id)

    # Obtener prácticas del docente con información relacionada
    practicas = PracticaEmpresarial.objects.filter(
        docente_asesor=docente
    ).select_related(
        'estudiante', 'empresa', 'tutor_empresarial'
    ).prefetch_related('seguimientos').order_by('-fecha_inicio')

    # Filtros
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        practicas = practicas.filter(estado=estado_filtro)

    # Estadísticas generales
    total_practicas_activas = practicas.filter(estado='EN_CURSO').count()
    total_practicas_finalizadas = practicas.filter(estado='FINALIZADA').count()
    total_seguimientos_pendientes = SeguimientoSemanal.objects.filter(
        practica__docente_asesor=docente,
        estado='PENDIENTE'
    ).count()

    context = {
        'docente': docente,
        'practicas': practicas,
        'estado_filtro': estado_filtro,
        'total_practicas_activas': total_practicas_activas,
        'total_practicas_finalizadas': total_practicas_finalizadas,
        'total_seguimientos_pendientes': total_seguimientos_pendientes,
    }

    return render(request, 'coordinacion/docentes_asesores/detalle.html', context)


@coordinator_required
def docente_asesor_practica_detalle(request, docente_id, practica_id):
    """Ver detalles de una práctica específica de un docente (igual a la vista del docente)"""
    docente = get_object_or_404(DocenteAsesor, id=docente_id)
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
        'desde_coordinacion': True,  # Flag para saber que es vista desde coordinación
    }

    return render(request, 'coordinacion/docentes_asesores/practica_detalle.html', context)


@coordinator_required
def docente_asesor_seguimiento_detalle(request, docente_id, seguimiento_id):
    """Ver detalles de un seguimiento específico"""
    docente = get_object_or_404(DocenteAsesor, id=docente_id)
    seguimiento = get_object_or_404(
        SeguimientoSemanal,
        id=seguimiento_id,
        practica__docente_asesor=docente
    )

    context = {
        'docente': docente,
        'seguimiento': seguimiento,
        'desde_coordinacion': True,
    }

    return render(request, 'coordinacion/docentes_asesores/seguimiento_detalle.html', context)


@coordinator_required
def docente_asesor_toggle_activo(request, docente_id):
    """Activar/desactivar un docente asesor"""
    docente = get_object_or_404(DocenteAsesor, id=docente_id)

    docente.activo = not docente.activo
    docente.save()

    estado = "activado" if docente.activo else "desactivado"
    messages.success(request, f'✅ Docente Asesor "{docente.nombre_completo}" {estado} correctamente')

    return redirect('coordinacion:docente_asesor_detalle', docente_id=docente.id)

