from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme


def login_unificado(request):
    """
    Login único que detecta automáticamente si es Coordinador o Estudiante
    """
    # Si ya está autenticado, redirigir según su rol (usar active_role si está en sesión)
    if request.user.is_authenticated:
        active_role = request.session.get('active_role')
        # Si ya se definió un rol activo en la sesión, respetarlo
        if active_role == 'coordinador':
            return redirect('coordinacion:dashboard')
        if active_role == 'estudiante':
            return redirect('estudiante:dashboard')

        # Si no hay rol activo, detectar por relaciones OneToOne
        only_coordinador = hasattr(request.user, 'coordinador') and not hasattr(request.user, 'estudiante')
        only_estudiante = hasattr(request.user, 'estudiante') and not hasattr(request.user, 'coordinador')
        both_roles = hasattr(request.user, 'coordinador') and hasattr(request.user, 'estudiante')

        if only_coordinador:
            request.session['active_role'] = 'coordinador'
            return redirect('coordinacion:dashboard')
        if only_estudiante:
            request.session['active_role'] = 'estudiante'
            return redirect('estudiante:dashboard')
        if both_roles:
            request.session['available_roles'] = ['coordinador', 'estudiante']
            return redirect('seleccionar_rol')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next')

        # Autenticar usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verificar cuenta activa
            if not user.is_active:
                messages.error(request, '❌ Tu cuenta está desactivada. Contacta al administrador.')
                return render(request, 'login_unificado.html')

            login(request, user)

            # DETECTAR TIPO DE USUARIO Y REDIRIGIR
            roles = []
            if hasattr(user, 'coordinador'):
                roles.append('coordinador')
            if hasattr(user, 'estudiante'):
                roles.append('estudiante')

            # Si tiene múltiples roles, pedir selección
            if len(roles) > 1:
                request.session['available_roles'] = roles
                return redirect('seleccionar_rol')

            # Si sólo tiene un rol, establecer active_role en sesión
            if 'coordinador' in roles:
                request.session['active_role'] = 'coordinador'
                messages.success(request, f'¡Bienvenido/a, Coordinador {user.coordinador.nombre_completo}! 👋')
                # Redirigir al next si es seguro
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('coordinacion:dashboard')

            elif 'estudiante' in roles:
                request.session['active_role'] = 'estudiante'
                messages.success(request, f'¡Bienvenido/a {user.estudiante.nombre_completo}! 👋')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('estudiante:dashboard')

            else:
                # Usuario sin rol asignado
                messages.error(request, '❌ Tu cuenta no tiene un rol asignado. Contacta al administrador.')
                return redirect('login_unificado')
        else:
            messages.error(request, '❌ Usuario o contraseña incorrectos')

    return render(request, 'login_unificado.html')


def seleccionar_rol(request):
    """Permite a usuarios con múltiples roles elegir con cuál entrar en la sesión actual."""
    available = request.session.get('available_roles', [])

    # Si no hay roles en sesión, redirigir al login
    if not available:
        return redirect('login_unificado')

    if request.method == 'POST':
        role = request.POST.get('role')
        if role not in available:
            messages.error(request, 'Rol inválido seleccionado')
            return redirect('seleccionar_rol')

        # Guardar rol activo y limpiar available_roles
        request.session['active_role'] = role
        request.session.pop('available_roles', None)

        if role == 'coordinador':
            return redirect('coordinacion:dashboard')
        else:
            return redirect('estudiante:dashboard')

    # GET -> mostrar opciones
    display = []
    for r in available:
        if r == 'coordinador':
            display.append({'key': 'coordinador', 'label': 'Coordinador'})
        elif r == 'estudiante':
            display.append({'key': 'estudiante', 'label': 'Estudiante'})

    return render(request, 'seleccionar_rol.html', {'roles': display})
