"""
Script para poblar la base de datos con datos de ejemplo
Ejecutar con: python poblar_datos.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Ahora importar los modelos
from django.contrib.auth.models import User
from coordinacion.models import *
from django.utils import timezone
from datetime import timedelta
import random

print("🚀 Iniciando población de datos...")

# 1. Crear Coordinador
print("\n📌 Creando coordinador...")
user_coord, created = User.objects.get_or_create(
    username='coordinador',
    defaults={'email': 'coordinador@ejemplo.com'}
)
if created:
    user_coord.set_password('admin123')
    user_coord.save()
    print("   ✅ Usuario coordinador creado")
else:
    print("   ℹ️  Usuario coordinador ya existe")

coordinador, created = Coordinador.objects.get_or_create(
    user=user_coord,
    defaults={
        'nombre_completo': 'María González',
        'email': 'coordinador@ejemplo.com',
        'telefono': '3001234567'
    }
)
if created:
    print("   ✅ Perfil de coordinador creado")
else:
    print("   ℹ️  Perfil de coordinador ya existe")

# 2. Crear Empresas
print("\n📌 Creando empresas...")
empresas_data = [
    {
        'razon_social': 'Tech Solutions SAS',
        'nit': '900123456-1',
        'ciudad': 'Barranquilla',
        'estado': 'APROBADA',
    },
    {
        'razon_social': 'Innovación Digital LTDA',
        'nit': '900234567-2',
        'ciudad': 'Barranquilla',
        'estado': 'APROBADA',
    },
    {
        'razon_social': 'Consultores Empresariales SA',
        'nit': '900345678-3',
        'ciudad': 'Cartagena',
        'estado': 'PENDIENTE',
    },
    {
        'razon_social': 'Software Development Inc',
        'nit': '900456789-4',
        'ciudad': 'Santa Marta',
        'estado': 'APROBADA',
    },
    {
        'razon_social': 'Marketing Digital Group',
        'nit': '900567890-5',
        'ciudad': 'Barranquilla',
        'estado': 'APROBADA',
    },
]

empresas_creadas = []
for emp_data in empresas_data:
    empresa, created = Empresa.objects.get_or_create(
        nit=emp_data['nit'],
        defaults={
            'razon_social': emp_data['razon_social'],
            'direccion': 'Calle 123 #45-67',
            'telefono': '6051234567',
            'email': f"info@{emp_data['nit']}.com",
            'ciudad': emp_data['ciudad'],
            'representante_nombre': 'Carlos Pérez',
            'representante_cargo': 'Gerente General',
            'representante_email': 'gerente@empresa.com',
            'representante_telefono': '3009876543',
            'estado': emp_data['estado'],
            'aprobada_por': coordinador if emp_data['estado'] == 'APROBADA' else None,
            'fecha_aprobacion': timezone.now() if emp_data['estado'] == 'APROBADA' else None,
        }
    )
    empresas_creadas.append(empresa)
    if created:
        print(f"   ✅ {empresa.razon_social}")
    else:
        print(f"   ℹ️  {empresa.razon_social} ya existe")

print(f"\n✅ Total empresas: {len(empresas_creadas)}")

# 3. Crear Vacantes
print("\n📌 Creando vacantes...")
programas = ['Ingeniería de Sistemas', 'Ingeniería Industrial', 'Administración de Empresas']
areas = ['Desarrollo de Software', 'Análisis de Datos', 'Gestión de Proyectos', 'Soporte Técnico', 'Marketing Digital']

vacantes_count = 0
for empresa in [e for e in empresas_creadas if e.estado == 'APROBADA']:
    for j in range(random.randint(1, 2)):
        vacante, created = Vacante.objects.get_or_create(
            empresa=empresa,
            titulo=f'Practicante de {programas[j % 3]} - {empresa.razon_social[:20]}',
            defaults={
                'area_practica': areas[j % len(areas)],
                'descripcion': f'Apoyo en proyectos del área de {areas[j % len(areas)]}. Se requiere estudiante proactivo con ganas de aprender.',
                'cantidad_cupos': random.randint(1, 3),
                'programa_academico': programas[j % 3],
                'semestre_minimo': random.choice([6, 7, 8]),
                'habilidades_requeridas': 'Trabajo en equipo, comunicación efectiva, responsabilidad',
                'horario': 'Lunes a Viernes 8:00am - 5:00pm',
                'duracion_meses': 6,
                'estado': random.choice(['DISPONIBLE', 'DISPONIBLE', 'OCUPADA']),
                'creada_por': coordinador,
                'fecha_publicacion': timezone.now(),
            }
        )
        if created:
            vacantes_count += 1

print(f"   ✅ {vacantes_count} vacantes creadas")

# 4. Crear Estudiantes
print("\n📌 Creando estudiantes...")
nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Laura', 'Pedro', 'Sofía', 'Diego', 'Camila']
apellidos = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 'Hernández', 'Díaz']

estudiantes_count = 0
for i in range(20):
    codigo = f'202{random.randint(0,3)}{str(i+100).zfill(3)}'
    nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"

    user_est, user_created = User.objects.get_or_create(
        username=codigo,
        defaults={'email': f'{codigo}@estudiante.com'}
    )
    if user_created:
        user_est.set_password('estudiante123')
        user_est.save()

    estudiante, created = Estudiante.objects.get_or_create(
        codigo=codigo,
        defaults={
            'user': user_est,
            'nombre_completo': nombre,
            'email': f'{codigo}@estudiante.com',
            'telefono': f'300{random.randint(1000000, 9999999)}',
            'programa_academico': random.choice(programas),
            'semestre': random.randint(6, 10),
            'estado': random.choice(['APTO', 'APTO', 'APTO', 'EN_PRACTICA']),
            'promedio_academico': round(random.uniform(3.5, 4.8), 2),
        }
    )
    if created:
        estudiantes_count += 1

print(f"   ✅ {estudiantes_count} estudiantes creados")

# 5. Crear Tutores
print("\n📌 Creando tutores empresariales...")
tutores_count = 0
for empresa in [e for e in empresas_creadas if e.estado == 'APROBADA']:
    tutor, created = TutorEmpresarial.objects.get_or_create(
        empresa=empresa,
        email=f'tutor@{empresa.nit}.com',
        defaults={
            'nombre_completo': f'Tutor de {empresa.razon_social}',
            'cargo': 'Jefe de Recursos Humanos',
            'telefono': f'300{random.randint(1000000, 9999999)}',
        }
    )
    if created:
        tutores_count += 1

print(f"   ✅ {tutores_count} tutores creados")

# 6. Crear Docentes Asesores
print("\n📌 Creando docentes asesores...")
docentes_nombres = ['Dr. Roberto Silva', 'Ing. Patricia Gómez', 'Mg. Fernando Castro', 'Dra. Ana Martínez', 'Dr. Luis Ramírez']
docentes_count = 0

for nombre in docentes_nombres:
    username = nombre.lower().replace(' ', '').replace('.', '')
    user_doc, user_created = User.objects.get_or_create(
        username=username,
        defaults={'email': f'{username}@universidad.com'}
    )
    if user_created:
        user_doc.set_password('docente123')
        user_doc.save()

    docente, created = DocenteAsesor.objects.get_or_create(
        user=user_doc,
        defaults={
            'nombre_completo': nombre,
            'email': f'{username}@universidad.com',
            'telefono': f'300{random.randint(1000000, 9999999)}',
            'especialidad': random.choice(programas),
        }
    )
    if created:
        docentes_count += 1

print(f"   ✅ {docentes_count} docentes creados")

# 7. Crear algunas Postulaciones
print("\n📌 Creando postulaciones...")
estudiantes_aptos = list(Estudiante.objects.filter(estado='APTO')[:10])
vacantes_disponibles = list(Vacante.objects.filter(estado='DISPONIBLE')[:5])

postulaciones_count = 0
if estudiantes_aptos and vacantes_disponibles:
    for estudiante in estudiantes_aptos:
        num_postulaciones = random.randint(1, min(2, len(vacantes_disponibles)))
        vacantes_seleccionadas = random.sample(vacantes_disponibles, num_postulaciones)

        for vacante in vacantes_seleccionadas:
            postulacion, created = Postulacion.objects.get_or_create(
                estudiante=estudiante,
                vacante=vacante,
                defaults={
                    'postulado_por': coordinador,
                    'estado': random.choice(['POSTULADO', 'POSTULADO', 'SELECCIONADO', 'VINCULADO']),
                }
            )
            if created:
                postulaciones_count += 1

print(f"   ✅ {postulaciones_count} postulaciones creadas")

# 8. Crear Prácticas Empresariales
print("\n📌 Creando prácticas empresariales...")
practicas_count = 0

postulaciones_para_practica = Postulacion.objects.filter(estado__in=['SELECCIONADO', 'VINCULADO'])[:5]
tutores_disponibles = list(TutorEmpresarial.objects.all())
docentes_disponibles = list(DocenteAsesor.objects.all())

if postulaciones_para_practica and tutores_disponibles and docentes_disponibles:
    for postulacion in postulaciones_para_practica:
        # Buscar tutor de la empresa de la vacante
        tutor = TutorEmpresarial.objects.filter(empresa=postulacion.vacante.empresa).first()
        if not tutor:
            tutor = random.choice(tutores_disponibles)

        docente = random.choice(docentes_disponibles)

        fecha_inicio = timezone.now().date() - timedelta(days=random.randint(30, 90))

        practica, created = PracticaEmpresarial.objects.get_or_create(
            estudiante=postulacion.estudiante,
            empresa=postulacion.vacante.empresa,
            defaults={
                'vacante': postulacion.vacante,
                'tutor_empresarial': tutor,
                'docente_asesor': docente,
                'fecha_inicio': fecha_inicio,
                'fecha_fin_estimada': fecha_inicio + timedelta(days=180),
                'estado': random.choice(['INICIADA', 'EN_CURSO', 'EN_CURSO', 'FINALIZADA']),
                'plan_aprobado': random.choice([True, False]),
                'asignada_por': coordinador,
                'observaciones': 'Práctica creada automáticamente para pruebas',
            }
        )

        if created:
            practicas_count += 1
            # Actualizar estado del estudiante
            if practica.estado in ['INICIADA', 'EN_CURSO']:
                postulacion.estudiante.estado = 'EN_PRACTICA'
                postulacion.estudiante.save()
            elif practica.estado == 'FINALIZADA':
                postulacion.estudiante.estado = 'FINALIZADO'
                postulacion.estudiante.save()

            # Actualizar estado de postulación
            postulacion.estado = 'VINCULADO'
            postulacion.save()

print(f"   ✅ {practicas_count} prácticas creadas")

# 9. Crear Sustentaciones
print("\n📌 Creando sustentaciones...")
sustentaciones_count = 0

practicas_para_sustentacion = PracticaEmpresarial.objects.filter(estado__in=['EN_CURSO', 'FINALIZADA'])[:3]
docentes_jurados = list(DocenteAsesor.objects.all())

if practicas_para_sustentacion and len(docentes_jurados) >= 2:
    for practica in practicas_para_sustentacion:
        # Seleccionar 2 jurados diferentes
        jurados = random.sample(docentes_jurados, 2)

        fecha_programada = timezone.now() + timedelta(days=random.randint(10, 30))

        sustentacion, created = Sustentacion.objects.get_or_create(
            practica=practica,
            defaults={
                'fecha_programada': fecha_programada,
                'lugar': random.choice(['Auditorio Principal', 'Sala de Conferencias A', 'Aula Magna']),
                'jurado_1': jurados[0],
                'jurado_2': jurados[1],
                'estado': random.choice(['PROGRAMADA', 'REALIZADA', 'APROBADA']),
                'calificacion': round(random.uniform(3.5, 5.0), 1) if random.choice([True, False]) else None,
                'registrada_por': coordinador,
                'observaciones': 'Sustentación registrada para pruebas',
            }
        )

        if created:
            sustentaciones_count += 1

print(f"   ✅ {sustentaciones_count} sustentaciones creadas")

# Resumen final
print("\n" + "="*50)
print("🎉 ¡Datos de prueba creados exitosamente!")
print("="*50)
print("\n📊 Resumen:")
print(f"   👤 Coordinadores: {Coordinador.objects.count()}")
print(f"   🏢 Empresas: {Empresa.objects.count()}")
print(f"   💼 Vacantes: {Vacante.objects.count()}")
print(f"   🎓 Estudiantes: {Estudiante.objects.count()}")
print(f"   👨‍💼 Tutores: {TutorEmpresarial.objects.count()}")
print(f"   👨‍🏫 Docentes: {DocenteAsesor.objects.count()}")
print(f"   📝 Postulaciones: {Postulacion.objects.count()}")
print(f"   💼 Prácticas: {PracticaEmpresarial.objects.count()}")
print(f"   🎓 Sustentaciones: {Sustentacion.objects.count()}")
print("\n✅ Puedes iniciar sesión con:")
print("   Usuario: coordinador")
print("   Contraseña: admin123")
print("="*50)