"""
Script para verificar y crear tutor empresarial
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from coordinacion.models import TutorEmpresarial, Empresa

def verificar_y_crear_tutor():
    """Verifica si existe el tutor y lo crea si no existe"""

    # Verificar si existe el usuario
    user_exists = User.objects.filter(username='tutor001').exists()

    if user_exists:
        user = User.objects.get(username='tutor001')
        print(f"✅ Usuario 'tutor001' existe")

        # Verificar si tiene tutor asociado
        if hasattr(user, 'tutor_empresarial'):
            tutor = user.tutor_empresarial
            print(f"✅ Tutor empresarial asociado: {tutor.nombre_completo}")
            print(f"   Empresa: {tutor.empresa.razon_social}")
            print(f"\n🔑 CREDENCIALES:")
            print(f"   Usuario: tutor001")
            print(f"   Contraseña: tutor123")
            print(f"\n🔗 URL: http://127.0.0.1:8000/login/")
            print(f"   Selecciona: Tutor Empresarial")
        else:
            print("❌ El usuario existe pero NO tiene tutor empresarial asociado")
            print("   Intentando asociar tutor...")

            # Buscar empresa
            empresa = Empresa.objects.filter(estado='APROBADA').first()
            if not empresa:
                empresa = Empresa.objects.first()

            if empresa:
                tutor = TutorEmpresarial.objects.create(
                    user=user,
                    empresa=empresa,
                    nombre_completo='Ing. Roberto Sánchez',
                    cargo='Jefe de Desarrollo',
                    email='tutor@empresa.com',
                    telefono='3001234567',
                    activo=True
                )
                print(f"✅ Tutor creado y asociado exitosamente")
                print(f"   Nombre: {tutor.nombre_completo}")
                print(f"   Empresa: {empresa.razon_social}")
            else:
                print("❌ No hay empresas disponibles")
    else:
        print("❌ Usuario 'tutor001' NO existe. Creando...")

        # Buscar empresa
        empresa = Empresa.objects.filter(estado='APROBADA').first()
        if not empresa:
            empresa = Empresa.objects.first()

        if not empresa:
            print("❌ No hay empresas en la base de datos")
            return

        # Crear usuario
        user = User.objects.create_user(
            username='tutor001',
            password='tutor123',
            email='tutor@empresa.com',
            first_name='Roberto',
            last_name='Sánchez'
        )

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

        print(f"✅ Tutor empresarial creado exitosamente!")
        print(f"   Usuario: tutor001")
        print(f"   Contraseña: tutor123")
        print(f"   Nombre: {tutor.nombre_completo}")
        print(f"   Empresa: {empresa.razon_social}")
        print(f"\n🔗 Accede en: http://127.0.0.1:8000/login/")
        print(f"   Selecciona el rol: Tutor Empresarial")

if __name__ == '__main__':
    verificar_y_crear_tutor()

