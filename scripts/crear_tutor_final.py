"""
Script para crear tutor empresarial directamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from coordinacion.models import TutorEmpresarial, Empresa

try:
    # Verificar si el usuario existe
    if User.objects.filter(username='tutor001').exists():
        print("El usuario tutor001 ya existe")
        user = User.objects.get(username='tutor001')

        # Verificar si tiene tutor
        try:
            tutor = user.tutor_empresarial
            print(f"Tutor ya existe: {tutor.nombre_completo}")
            print(f"Empresa: {tutor.empresa.razon_social}")
        except TutorEmpresarial.DoesNotExist:
            print("Usuario existe pero sin tutor. Creando tutor...")
            empresa = Empresa.objects.first()
            if not empresa:
                print("ERROR: No hay empresas")
                sys.exit(1)

            tutor = TutorEmpresarial.objects.create(
                user=user,
                empresa=empresa,
                nombre_completo='Ing. Roberto Sánchez',
                cargo='Jefe de Desarrollo',
                email='tutor@empresa.com',
                telefono='3001234567',
                activo=True
            )
            print(f"TUTOR CREADO: {tutor.nombre_completo}")
    else:
        print("Creando usuario tutor001...")
        empresa = Empresa.objects.first()
        if not empresa:
            print("ERROR: No hay empresas en la base de datos")
            sys.exit(1)

        # Crear usuario
        user = User.objects.create_user(
            username='tutor001',
            password='tutor123',
            email='tutor@empresa.com',
            first_name='Roberto',
            last_name='Sánchez'
        )
        print("Usuario creado")

        # Crear tutor
        tutor = TutorEmpresarial.objects.create(
            user=user,
            empresa=empresa,
            nombre_completo='Ing. Roberto Sánchez',
            cargo='Jefe de Desarrollo',
            email='tutor@empresa.com',
            telefono='3001234567',
            activo=True
        )
        print(f"TUTOR CREADO: {tutor.nombre_completo}")

    print("\n=== CREDENCIALES ===")
    print("Usuario: tutor001")
    print("Contraseña: tutor123")
    print("Rol: Tutor Empresarial")
    print("\nURL: http://127.0.0.1:8000/login/")

except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

