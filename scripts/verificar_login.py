"""
Script de verificación del sistema de login unificado
Verifica que todos los componentes estén correctamente configurados
"""

import os
import sys

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_file_exists(filepath, description):
    """Verifica si un archivo existe"""
    if os.path.exists(filepath):
        print(f"{GREEN}✓{RESET} {description}: OK")
        return True
    else:
        print(f"{RED}✗{RESET} {description}: NO ENCONTRADO")
        return False

def check_file_renamed(filepath, description):
    """Verifica si un archivo fue renombrado (respaldo)"""
    if os.path.exists(filepath):
        print(f"{GREEN}✓{RESET} {description}: Respaldado")
        return True
    else:
        print(f"{YELLOW}!{RESET} {description}: No encontrado (puede ser normal)")
        return False

def main():
    print("=" * 60)
    print("VERIFICACIÓN DEL SISTEMA DE LOGIN UNIFICADO")
    print("=" * 60)
    print()
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Verificar archivos nuevos/actualizados
    print("1. Verificando archivos principales...")
    print("-" * 60)
    
    files_to_check = [
        ("config/templates/login_unificado.html", "Login unificado"),
        ("config/templates/seleccionar_rol.html", "Selector de rol"),
        ("config/views.py", "Vistas de config"),
        ("coordinacion/views.py", "Vistas de coordinación"),
        ("Estudiante/estudiante_views.py", "Vistas de estudiante"),
    ]
    
    all_ok = True
    for filepath, desc in files_to_check:
        full_path = os.path.join(base_path, filepath)
        if not check_file_exists(full_path, desc):
            all_ok = False
    
    print()
    
    # 2. Verificar archivos de respaldo
    print("2. Verificando archivos de respaldo (antiguos logins)...")
    print("-" * 60)
    
    backup_files = [
        ("coordinacion/templates/coordinacion/login.html.old", "Login coordinación antiguo"),
        ("Estudiante/templates/estudiante/login.html.old", "Login estudiante antiguo"),
    ]
    
    for filepath, desc in backup_files:
        full_path = os.path.join(base_path, filepath)
        check_file_renamed(full_path, desc)
    
    print()
    
    # 3. Verificar contenido de archivos clave
    print("3. Verificando contenido de archivos clave...")
    print("-" * 60)
    
    # Verificar que config/views.py tiene login_unificado
    config_views = os.path.join(base_path, "config/views.py")
    if os.path.exists(config_views):
        with open(config_views, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'def login_unificado' in content:
                print(f"{GREEN}✓{RESET} config/views.py tiene 'login_unificado'")
            else:
                print(f"{RED}✗{RESET} config/views.py NO tiene 'login_unificado'")
                all_ok = False
            
            if 'def seleccionar_rol' in content:
                print(f"{GREEN}✓{RESET} config/views.py tiene 'seleccionar_rol'")
            else:
                print(f"{RED}✗{RESET} config/views.py NO tiene 'seleccionar_rol'")
                all_ok = False
    
    # Verificar que coordinacion/views.py redirige al unificado
    coord_views = os.path.join(base_path, "coordinacion/views.py")
    if os.path.exists(coord_views):
        with open(coord_views, 'r', encoding='utf-8') as f:
            content = f.read()
            if "redirect('login_unificado')" in content:
                print(f"{GREEN}✓{RESET} coordinacion/views.py redirige a login_unificado")
            else:
                print(f"{YELLOW}!{RESET} coordinacion/views.py podría no redirigir correctamente")
    
    # Verificar que estudiante/views.py redirige al unificado
    est_views = os.path.join(base_path, "Estudiante/estudiante_views.py")
    if os.path.exists(est_views):
        with open(est_views, 'r', encoding='utf-8') as f:
            content = f.read()
            if "redirect('login_unificado')" in content:
                print(f"{GREEN}✓{RESET} Estudiante/estudiante_views.py redirige a login_unificado")
            else:
                print(f"{YELLOW}!{RESET} Estudiante/estudiante_views.py podría no redirigir correctamente")
    
    print()
    
    # 4. Verificar templates
    print("4. Verificando templates...")
    print("-" * 60)
    
    login_template = os.path.join(base_path, "config/templates/login_unificado.html")
    if os.path.exists(login_template):
        with open(login_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
            checks = [
                ('roleSelector', 'Selector de rol'),
                ('loginForm', 'Formulario de login'),
                ('registerLink', 'Link de registro'),
                ('background: linear-gradient(135deg, #1e3c72', 'Diseño en azul'),
            ]
            
            for check_str, desc in checks:
                if check_str in content:
                    print(f"{GREEN}✓{RESET} {desc} presente")
                else:
                    print(f"{RED}✗{RESET} {desc} NO presente")
                    all_ok = False
    
    print()
    print("=" * 60)
    if all_ok:
        print(f"{GREEN}✓ VERIFICACIÓN COMPLETADA EXITOSAMENTE{RESET}")
    else:
        print(f"{YELLOW}! VERIFICACIÓN COMPLETADA CON ADVERTENCIAS{RESET}")
    print("=" * 60)
    print()
    print("Próximos pasos:")
    print("1. Ejecutar: python manage.py runserver")
    print("2. Abrir: http://127.0.0.1:8000/")
    print("3. Probar el login con diferentes roles")
    print()

if __name__ == '__main__':
    main()

