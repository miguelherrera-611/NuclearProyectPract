from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden
from django.db import transaction

from .models import Empresa, TutorEmpresarial
from .forms import EmpresaForm, TutorEmpresarialFormSet


def coordinator_required(view_func):
    """Decorador compatible con el definido en `views.py` para proteger rutas de coordinador."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('coordinacion:login')
        if not hasattr(request.user, 'coordinador'):
            messages.error(request, 'Acceso denegado: se requiere rol Coordinador')
            return HttpResponseForbidden('Acceso denegado')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@coordinator_required
def empresa_crear(request):
    """Crear una nueva empresa formadora (CRUD)"""
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES)
        tutor_formset = TutorEmpresarialFormSet(request.POST, prefix='tutores')

        if form.is_valid() and tutor_formset.is_valid():
            with transaction.atomic():
                empresa = form.save(commit=False)
                if empresa.estado == 'APROBADA':
                    empresa.fecha_aprobacion = timezone.now()
                    empresa.aprobada_por = request.user.coordinador
                empresa.save()

                # Guardar tutores
                tutor_formset.instance = empresa
                tutor_formset.save()

            messages.success(request, f'✅ Empresa "{empresa.razon_social}" creada correctamente')
            return redirect('coordinacion:empresa_detalle', empresa_id=empresa.id)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = EmpresaForm()
        tutor_formset = TutorEmpresarialFormSet(prefix='tutores')

    return render(request, 'coordinacion/empresas/crear.html', {
        'form': form,
        'tutor_formset': tutor_formset
    })


@coordinator_required
def empresa_editar(request, empresa_id):
    """Editar una empresa existente"""
    empresa = get_object_or_404(Empresa, id=empresa_id)

    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        tutor_formset = TutorEmpresarialFormSet(request.POST, instance=empresa, prefix='tutores')

        if form.is_valid() and tutor_formset.is_valid():
            with transaction.atomic():
                emp = form.save(commit=False)
                if emp.estado == 'APROBADA' and empresa.estado != 'APROBADA':
                    emp.fecha_aprobacion = timezone.now()
                    emp.aprobada_por = request.user.coordinador
                emp.save()

                # Guardar tutores
                tutor_formset.save()

            messages.success(request, f'✅ Empresa "{emp.razon_social}" actualizada correctamente')
            return redirect('coordinacion:empresa_detalle', empresa_id=emp.id)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = EmpresaForm(instance=empresa)
        tutor_formset = TutorEmpresarialFormSet(instance=empresa, prefix='tutores')

    return render(request, 'coordinacion/empresas/editar.html', {
        'form': form,
        'tutor_formset': tutor_formset,
        'empresa': empresa
    })


@coordinator_required
def empresa_eliminar(request, empresa_id):
    """Eliminar una empresa (confirmación GET, eliminación en POST)."""
    empresa = get_object_or_404(Empresa, id=empresa_id)

    if request.method == 'POST':
        razon = empresa.razon_social
        empresa.delete()
        messages.success(request, f'✅ Empresa "{razon}" eliminada correctamente')
        return redirect('coordinacion:empresas_lista')

    # GET: mostrar confirmación
    return render(request, 'coordinacion/empresas/eliminar.html', {'empresa': empresa})
