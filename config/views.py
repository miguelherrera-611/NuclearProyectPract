from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme


def login_unificado(request):
    """
    Login único que detecta automáticamente si es Coordinador, Estudiante o Docente Asesor
    """
    # Si ya está autenticado, redirigir según su rol activo
    if request.user.is_authenticated:
        active_role = request.session.get('active_role')
        if active_role == 'coordinador':
            return redirect('coordinacion:dashboard')
        if active_role == 'estudiante':
            return redirect('estudiante:dashboard')
        if active_role == 'docente':
            return redirect('docente:dashboard')

        # Si no hay rol activo, detectar por relaciones OneToOne
        roles = []
        if hasattr(request.user, 'coordinador'):
            roles.append('coordinador')
        if hasattr(request.user, 'estudiante'):
            roles.append('estudiante')
        if hasattr(request.user, 'docente_asesor'):
            roles.append('docente')

        # Si tiene un solo rol, redirigir directamente
        if len(roles) == 1:
            request.session['active_role'] = roles[0]
            if roles[0] == 'coordinador':
                return redirect('coordinacion:dashboard')
            elif roles[0] == 'estudiante':
                return redirect('estudiante:dashboard')
            elif roles[0] == 'docente':
                return redirect('docente:dashboard')

        # Si tiene múltiples roles, pedir selección
        if len(roles) > 1:
            request.session['available_roles'] = roles
            return redirect('seleccionar_rol')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_role = request.POST.get('selected_role')  # Rol seleccionado desde el frontend
        next_url = request.POST.get('next') or request.GET.get('next')

        # Autenticar usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verificar cuenta activa
            if not user.is_active:
                messages.error(request, '❌ Tu cuenta está desactivada. Contacta al administrador.')
                return render(request, 'login_unificado.html')

            # Verificar que el usuario tenga el rol seleccionado
            has_role = False
            role_name = ''

            if selected_role == 'coordinador':
                has_role = hasattr(user, 'coordinador')
                role_name = 'Coordinador'
            elif selected_role == 'estudiante':
                has_role = hasattr(user, 'estudiante')
                role_name = 'Estudiante'
            elif selected_role == 'docente':
                has_role = hasattr(user, 'docente_asesor')
                role_name = 'Docente Asesor'

            if not has_role:
                messages.error(request, f'❌ Tu cuenta no tiene permisos de {role_name}. Verifica tu rol.')
                return render(request, 'login_unificado.html')

            # Login exitoso
            login(request, user)
            request.session['active_role'] = selected_role

            # Mensaje de bienvenida personalizado
            if selected_role == 'coordinador':
                messages.success(request, f'¡Bienvenido/a, Coordinador {user.coordinador.nombre_completo}! 👋')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('coordinacion:dashboard')

            elif selected_role == 'estudiante':
                messages.success(request, f'¡Bienvenido/a {user.estudiante.nombre_completo}! 👋')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('estudiante:dashboard')

            elif selected_role == 'docente':
                messages.success(request, f'¡Bienvenido/a, Docente {user.docente_asesor.nombre_completo}! 👋')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('docente:dashboard')

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
        elif role == 'estudiante':
            return redirect('estudiante:dashboard')
        elif role == 'docente':
            return redirect('docente:dashboard')

    # GET -> mostrar opciones
    display = []
    for r in available:
        if r == 'coordinador':
            display.append({'key': 'coordinador', 'label': 'Coordinador', 'icon': 'fa-user-tie'})
        elif r == 'estudiante':
            display.append({'key': 'estudiante', 'label': 'Estudiante', 'icon': 'fa-user-graduate'})
        elif r == 'docente':
            display.append({'key': 'docente', 'label': 'Docente Asesor', 'icon': 'fa-chalkboard-teacher'})

    return render(request, 'seleccionar_rol.html', {'roles': display})


def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login_unificado')

