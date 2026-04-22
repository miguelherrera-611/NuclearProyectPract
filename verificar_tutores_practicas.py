#!/usr/bin/env python
"""
Script para verificar tutores empresariales y sus prácticas
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from coordinacion.models import TutorEmpresarial, PracticaEmpresarial

print("🔍 VERIFICANDO TUTORES EMPRESARIALES Y PRÁCTICAS\n")
print("=" * 60)

# Contar tutores
total_tutores = TutorEmpresarial.objects.count()
print(f"\n📊 Total de Tutores Empresariales: {total_tutores}")

if total_tutores == 0:
    print("\n❌ NO HAY TUTORES REGISTRADOS")
    print("   Necesitas crear tutores empresariales primero.")
    print("   Ve a: /coordinacion/tutores/crear/")
else:
    print(f"\n✅ Hay {total_tutores} tutores registrados\n")
    print("-" * 60)

    for tutor in TutorEmpresarial.objects.all().select_related('empresa'):
        print(f"\n👔 {tutor.nombre_completo}")
        print(f"   🏢 Empresa: {tutor.empresa.razon_social}")
        print(f"   💼 Cargo: {tutor.cargo}")
        print(f"   ✉️  Email: {tutor.email}")

        # Contar prácticas
        practicas = tutor.practicas_supervisadas.all()
        total_practicas = practicas.count()

        if total_practicas == 0:
            print(f"   ⚠️  NO tiene prácticas asignadas")
        else:
            finalizadas = practicas.filter(estado='FINALIZADA').count()
            en_curso = practicas.filter(estado='EN_CURSO').count()
            canceladas = practicas.filter(estado='CANCELADA').count()

            print(f"   📋 Prácticas:")
            print(f"      • Total: {total_practicas}")
            print(f"      • Finalizadas: {finalizadas} ✅")
            print(f"      • En Curso: {en_curso} 🔵")
            print(f"      • Canceladas: {canceladas} ❌")

            # Mostrar estudiantes
            for practica in practicas:
                estado_emoji = {
                    'FINALIZADA': '✅',
                    'EN_CURSO': '🔵',
                    'CANCELADA': '❌'
                }.get(practica.estado, '❓')

                print(f"      {estado_emoji} {practica.estudiante.nombre_completo} ({practica.get_estado_display()})")

print("\n" + "=" * 60)
print("\n💡 INSTRUCCIONES:")
print("   1. Si no hay tutores: Créalos en /coordinacion/tutores/")
print("   2. Si no hay prácticas: Asígnalas desde /coordinacion/practicas/")
print("   3. Si hay prácticas FINALIZADAS: Podrás enviar encuestas")
print("   4. Si solo hay EN_CURSO: Espera a que finalicen")
print("\n✨ ¡Listo!\n")

