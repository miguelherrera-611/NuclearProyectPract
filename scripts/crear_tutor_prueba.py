"""
Script para crear un tutor empresarial de prueba
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from coordinacion.models import TutorEmpresarial, Empresa

def crear_tutor_prueba():
    """Crea un tutor empresarial de prueba"""

    # Verificar si ya existe
    if User.objects.filter(username='tutor001').exists():
        print("❌ El tutor 'tutor001' ya existe")
        return

    # Buscar empresa aprobada
    empresa = Empresa.objects.filter(estado='APROBADA').first()
    if not empresa:
        empresa = Empresa.objects.filter().first()

    if not empresa:
        print("❌ No hay empresas en la base de datos. Primero crea una empresa desde coordinación.")
        return

    # Crear usuario
    user = User.objects.create_user(
        username='tutor001',
        password='tutor123',
        email='tutor@empresa.com',
        first_name='Roberto',
        last_name='Sánchez'
    )

    # Crear tutor empresarial
    tutor = TutorEmpresarial.objects.create(
        user=user,
        empresa=empresa,
        nombre_completo='Ing. Roberto Sánchez',
        cargo='Jefe de Desarrollo',
        email='tutor@empresa.com',
        telefono='3001234567',
        activo=True
    )

    print("✅ Tutor empresarial creado exitosamente!")
    print(f"   Usuario: tutor001")
    print(f"   Contraseña: tutor123")
    print(f"   Nombre: {tutor.nombre_completo}")
    print(f"   Empresa: {empresa.razon_social}")
    print(f"\n🔗 Accede en: http://127.0.0.1:8000/login/")
    print(f"   Selecciona el rol: Tutor Empresarial")

if __name__ == '__main__':
    crear_tutor_prueba()

