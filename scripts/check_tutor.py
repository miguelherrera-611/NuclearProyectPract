import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from coordinacion.models import TutorEmpresarial, Empresa

# Verificar usuario
user = User.objects.filter(username='tutor001').first()
print("Usuario 'tutor001' existe:", user is not None)

if user:
    print("Tiene tutor asociado:", hasattr(user, 'tutor_empresarial'))
    if hasattr(user, 'tutor_empresarial'):
        print("Nombre tutor:", user.tutor_empresarial.nombre_completo)
    else:
        print("\n⚠️ El usuario existe pero NO tiene tutor asociado")
        print("Creando tutor...")
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
            print("✅ Tutor creado:", tutor.nombre_completo)
        else:
            print("❌ No hay empresas")
else:
    print("\n⚠️ Usuario NO existe. Creando...")
    empresa = Empresa.objects.first()
    if empresa:
        user = User.objects.create_user(
            username='tutor001',
            password='tutor123',
            email='tutor@empresa.com'
        )
        tutor = TutorEmpresarial.objects.create(
            user=user,
            empresa=empresa,
            nombre_completo='Ing. Roberto Sánchez',
            cargo='Jefe de Desarrollo',
            email='tutor@empresa.com',
            telefono='3001234567',
            activo=True
        )
        print("✅ Usuario y tutor creados")
        print("Usuario: tutor001")
        print("Contraseña: tutor123")
    else:
        print("❌ No hay empresas")

