"""
Script para crear un Docente Asesor de prueba
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from coordinacion.models import DocenteAsesor

def crear_docente_asesor():
    """Crear un docente asesor de prueba"""

    # Verificar si ya existe
    if User.objects.filter(username='docente1').exists():
        print("❌ El usuario 'docente1' ya existe")
        user = User.objects.get(username='docente1')
        if hasattr(user, 'docente_asesor'):
            print(f"✅ Docente Asesor ya creado: {user.docente_asesor.nombre_completo}")
            return user.docente_asesor
    else:
        # Crear usuario
        user = User.objects.create_user(
            username='docente1',
            password='docente123',
            email='docente1@universidad.edu.co',
            first_name='Carlos',
            last_name='Rodríguez'
        )
        print(f"✅ Usuario creado: {user.username}")

    # Verificar si tiene perfil de docente
    if hasattr(user, 'docente_asesor'):
        print(f"✅ El usuario ya tiene perfil de Docente Asesor")
        return user.docente_asesor

    # Crear perfil de Docente Asesor
    docente = DocenteAsesor.objects.create(
        user=user,
        nombre_completo='Carlos Rodríguez Pérez',
        email='docente1@universidad.edu.co',
        telefono='3001234567',
        especialidad='Ingeniería de Software',
        activo=True
    )

    print(f"✅ Docente Asesor creado exitosamente")
    print(f"   Nombre: {docente.nombre_completo}")
    print(f"   Email: {docente.email}")
    print(f"   Especialidad: {docente.especialidad}")
    print(f"\n🔑 Credenciales de acceso:")
    print(f"   Usuario: docente1")
    print(f"   Contraseña: docente123")

    return docente


def crear_mas_docentes():
    """Crear docentes adicionales"""
    docentes_data = [
        {
            'username': 'docente2',
            'password': 'docente123',
            'nombre_completo': 'María González Torres',
            'email': 'maria.gonzalez@universidad.edu.co',
            'telefono': '3009876543',
            'especialidad': 'Ingeniería Industrial'
        },
        {
            'username': 'docente3',
            'password': 'docente123',
            'nombre_completo': 'Jorge Martínez López',
            'email': 'jorge.martinez@universidad.edu.co',
            'telefono': '3005551234',
            'especialidad': 'Administración de Empresas'
        }
    ]

    for data in docentes_data:
        if User.objects.filter(username=data['username']).exists():
            print(f"⚠️  El usuario '{data['username']}' ya existe, saltando...")
            continue

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email']
        )

        docente = DocenteAsesor.objects.create(
            user=user,
            nombre_completo=data['nombre_completo'],
            email=data['email'],
            telefono=data['telefono'],
            especialidad=data['especialidad'],
            activo=True
        )

        print(f"✅ Docente creado: {docente.nombre_completo} ({data['username']})")


if __name__ == '__main__':
    print("=" * 60)
    print("CREACIÓN DE DOCENTES ASESORES")
    print("=" * 60)
    print()

    # Crear docente principal
    docente1 = crear_docente_asesor()

    print("\n" + "=" * 60)
    print("CREANDO DOCENTES ADICIONALES")
    print("=" * 60)
    print()

    # Crear más docentes
    crear_mas_docentes()

    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print("\nTodos los docentes pueden acceder con su usuario y contraseña: docente123")
    print("Ejemplo: usuario 'docente1' con contraseña 'docente123'")

