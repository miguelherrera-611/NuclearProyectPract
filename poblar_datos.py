"""
Script para poblar la base de datos con datos de ejemplo
Ejecutar con: python manage.py shell < poblar_datos.py
O: python manage.py shell
    exec(open('poblar_datos.py').read())
"""

from django.contrib.auth.models import User
from coordinacion.models import (
    Coordinador, Empresa, Vacante, Estudiante, TutorEmpresarial,
    DocenteAsesor, Postulacion, PracticaEmpresarial
)
from datetime import date, timedelta
from django.utils import timezone

print("=" * 60)
print("🚀 INICIANDO POBLACIÓN DE BASE DE DATOS")
print("=" * 60)

# ============================================
# 1. CREAR USUARIOS Y COORDINADORES
# ============================================
print("\n📋 Creando Coordinadores...")

# Coordinador Principal
if not User.objects.filter(username='coordinador').exists():
    user_coord = User.objects.create_user(
        username='coordinador',
        password='admin123',
        email='coordinador@humboldt.edu.co',
        first_name='María',
        last_name='González'
    )

    coordinador = Coordinador.objects.create(
        user=user_coord,
        nombre_completo='María González Pérez',
        email='coordinador@humboldt.edu.co',
        telefono='3101234567',
        activo=True
    )
    print(f"✅ Coordinador creado: {coordinador.nombre_completo}")
else:
    coordinador = Coordinador.objects.get(user__username='coordinador')
    print(f"✅ Coordinador ya existe: {coordinador.nombre_completo}")

# ============================================
# 2. CREAR EMPRESAS
# ============================================
print("\n🏢 Creando Empresas...")

empresas_data = [
    {
        'razon_social': 'Tecnologías Innovadoras S.A.S.',
        'nit': '900123456-7',
        'direccion': 'Calle 100 #15-20',
        'telefono': '6017001234',
        'email': 'rrhh@tecnologias.com',
        'ciudad': 'Bogotá',
        'representante_nombre': 'Carlos Mendoza',
        'representante_cargo': 'Gerente General',
        'representante_email': 'cmendoza@tecnologias.com',
        'representante_telefono': '3201234567',
        'estado': 'APROBADA'
    },
    {
        'razon_social': 'Desarrollos Web Colombia Ltda.',
        'nit': '900234567-8',
        'direccion': 'Carrera 7 #80-50',
        'telefono': '6017002345',
        'email': 'contacto@desarrollosweb.co',
        'ciudad': 'Bogotá',
        'representante_nombre': 'Ana López',
        'representante_cargo': 'Directora de Talento Humano',
        'representante_email': 'alopez@desarrollosweb.co',
        'representante_telefono': '3102345678',
        'estado': 'APROBADA'
    },
    {
        'razon_social': 'Marketing Digital Pro S.A.S.',
        'nit': '900345678-9',
        'direccion': 'Avenida El Dorado #50-30',
        'telefono': '6017003456',
        'email': 'info@marketingpro.co',
        'ciudad': 'Bogotá',
        'representante_nombre': 'Luis Ramírez',
        'representante_cargo': 'CEO',
        'representante_email': 'lramirez@marketingpro.co',
        'representante_telefono': '3153456789',
        'estado': 'APROBADA'
    },
    {
        'razon_social': 'Soluciones Empresariales Tech S.A.',
        'nit': '900456789-0',
        'direccion': 'Calle 72 #10-30',
        'telefono': '6017004567',
        'email': 'contacto@soltech.com',
        'ciudad': 'Bogotá',
        'representante_nombre': 'Patricia Gómez',
        'representante_cargo': 'Gerente de Operaciones',
        'representante_email': 'pgomez@soltech.com',
        'representante_telefono': '3204567890',
        'estado': 'PENDIENTE'
    },
    {
        'razon_social': 'Innovación y Sistemas Ltda.',
        'nit': '900567890-1',
        'direccion': 'Carrera 15 #93-20',
        'telefono': '6017005678',
        'email': 'rrhh@innovasistemas.co',
        'ciudad': 'Bogotá',
        'representante_nombre': 'Roberto Castro',
        'representante_cargo': 'Director General',
        'representante_email': 'rcastro@innovasistemas.co',
        'representante_telefono': '3115678901',
        'estado': 'APROBADA'
    }
]

empresas_creadas = []
for empresa_data in empresas_data:
    empresa, created = Empresa.objects.get_or_create(
        nit=empresa_data['nit'],
        defaults={
            **empresa_data,
            'aprobada_por': coordinador if empresa_data['estado'] == 'APROBADA' else None,
            'fecha_aprobacion': timezone.now() if empresa_data['estado'] == 'APROBADA' else None
        }
    )
    empresas_creadas.append(empresa)
    status = "✅ Creada" if created else "ℹ️  Ya existe"
    print(f"{status}: {empresa.razon_social}")

# ============================================
# 3. CREAR TUTORES EMPRESARIALES
# ============================================
print("\n👔 Creando Tutores Empresariales...")

tutores_data = [
    {'empresa': empresas_creadas[0], 'nombre': 'Jorge Martínez', 'cargo': 'Líder de Desarrollo'},
    {'empresa': empresas_creadas[0], 'nombre': 'Sandra Ruiz', 'cargo': 'Jefe de Proyectos'},
    {'empresa': empresas_creadas[1], 'nombre': 'Miguel Ángel Torres', 'cargo': 'Coordinador Técnico'},
    {'empresa': empresas_creadas[2], 'nombre': 'Laura Jiménez', 'cargo': 'Gerente de Marketing'},
    {'empresa': empresas_creadas[4], 'nombre': 'Fernando Vargas', 'cargo': 'Supervisor de TI'},
]

for tutor_data in tutores_data:
    tutor, created = TutorEmpresarial.objects.get_or_create(
        empresa=tutor_data['empresa'],
        nombre_completo=tutor_data['nombre'],
        defaults={
            'cargo': tutor_data['cargo'],
            'email': f"{tutor_data['nombre'].lower().replace(' ', '.')}@{tutor_data['empresa'].email.split('@')[1]}",
            'telefono': f"310{str(hash(tutor_data['nombre']))[-7:]}",
            'activo': True
        }
    )
    status = "✅ Creado" if created else "ℹ️  Ya existe"
    print(f"{status}: {tutor.nombre_completo} - {tutor.empresa.razon_social}")

# ============================================
# 4. CREAR DOCENTES ASESORES
# ============================================
print("\n👨‍🏫 Creando Docentes Asesores...")

docentes_data = [
    {'nombre': 'Dr. Carlos Rodríguez', 'especialidad': 'Ingeniería de Software'},
    {'nombre': 'Mg. Diana Pérez', 'especialidad': 'Desarrollo de Aplicaciones'},
    {'nombre': 'Esp. Ricardo Gómez', 'especialidad': 'Gestión de Proyectos'},
    {'nombre': 'Dr. Andrea Morales', 'especialidad': 'Bases de Datos'},
]

for docente_data in docentes_data:
    username = docente_data['nombre'].lower().replace(' ', '.').replace('dr.', '').replace('mg.', '').replace('esp.', '').strip()

    if not User.objects.filter(username=username).exists():
        user_docente = User.objects.create_user(
            username=username,
            password='docente123',
            email=f"{username}@humboldt.edu.co"
        )

        docente = DocenteAsesor.objects.create(
            user=user_docente,
            nombre_completo=docente_data['nombre'],
            email=f"{username}@humboldt.edu.co",
            telefono=f"320{str(hash(username))[-7:]}",
            especialidad=docente_data['especialidad'],
            activo=True
        )
        print(f"✅ Creado: {docente.nombre_completo} - {docente.especialidad}")
    else:
        print(f"ℹ️  Ya existe: {docente_data['nombre']}")

# ============================================
# 5. CREAR ESTUDIANTES
# ============================================
print("\n🎓 Creando Estudiantes...")

estudiantes_data = [
    {
        'codigo': '2020001',
        'nombre': 'Juan Sebastián Ramírez',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 8,
        'promedio': 4.2,
        'estado': 'APTO'
    },
    {
        'codigo': '2020002',
        'nombre': 'María Fernanda Castro',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 7,
        'promedio': 4.5,
        'estado': 'APTO'
    },
    {
        'codigo': '2020003',
        'nombre': 'Andrés Felipe Moreno',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 9,
        'promedio': 3.8,
        'estado': 'APTO'
    },
    {
        'codigo': '2019004',
        'nombre': 'Carolina Gutiérrez',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 10,
        'promedio': 4.0,
        'estado': 'EN_PRACTICA'
    },
    {
        'codigo': '2019005',
        'nombre': 'Diego Alejandro Vargas',
        'programa': 'Ingeniería Industrial',
        'semestre': 8,
        'promedio': 4.3,
        'estado': 'APTO'
    },
    {
        'codigo': '2020006',
        'nombre': 'Laura Sofía Martínez',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 7,
        'promedio': 4.1,
        'estado': 'APTO'
    },
]

for est_data in estudiantes_data:
    username = f"est{est_data['codigo']}"

    if not User.objects.filter(username=username).exists():
        user_est = User.objects.create_user(
            username=username,
            password='estudiante123',
            email=f"{username}@humboldt.edu.co"
        )

        estudiante = Estudiante.objects.create(
            user=user_est,
            codigo=est_data['codigo'],
            nombre_completo=est_data['nombre'],
            email=f"{username}@humboldt.edu.co",
            telefono=f"315{str(hash(username))[-7:]}",
            programa_academico=est_data['programa'],
            semestre=est_data['semestre'],
            promedio_academico=est_data['promedio'],
            estado=est_data['estado']
        )
        print(f"✅ Creado: {estudiante.codigo} - {estudiante.nombre_completo}")
    else:
        print(f"ℹ️  Ya existe: {est_data['codigo']} - {est_data['nombre']}")

# ============================================
# 6. CREAR VACANTES
# ============================================
print("\n💼 Creando Vacantes...")

vacantes_data = [
    {
        'empresa': empresas_creadas[0],
        'titulo': 'Practicante de Desarrollo Full Stack',
        'area': 'Desarrollo de Software',
        'descripcion': 'Buscamos estudiante de últimos semestres para apoyar en el desarrollo de aplicaciones web usando tecnologías modernas como React, Node.js y PostgreSQL. El practicante participará en proyectos reales, trabajará en equipo y aprenderá metodologías ágiles.',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 7,
        'cupos': 2,
        'duracion': 6,
        'estado': 'DISPONIBLE'
    },
    {
        'empresa': empresas_creadas[1],
        'titulo': 'Practicante de Diseño UX/UI',
        'area': 'Diseño de Experiencia de Usuario',
        'descripcion': 'Apoyo en el diseño de interfaces de usuario y experiencia para proyectos web y móviles. Se requiere conocimiento en Figma, Adobe XD y principios de diseño centrado en el usuario.',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 6,
        'cupos': 1,
        'duracion': 5,
        'estado': 'DISPONIBLE'
    },
    {
        'empresa': empresas_creadas[2],
        'titulo': 'Practicante de Marketing Digital',
        'area': 'Marketing y Comunicaciones',
        'descripcion': 'Apoyo en estrategias de marketing digital, gestión de redes sociales, análisis de métricas y creación de contenido. Ideal para estudiantes creativos y analíticos.',
        'programa': 'Ingeniería Industrial',
        'semestre': 7,
        'cupos': 2,
        'duracion': 6,
        'estado': 'DISPONIBLE'
    },
    {
        'empresa': empresas_creadas[0],
        'titulo': 'Practicante de Analítica de Datos',
        'area': 'Business Intelligence',
        'descripcion': 'Participación en proyectos de análisis de datos, creación de dashboards y reportes. Conocimientos en Python, SQL y Power BI son valorados.',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 8,
        'cupos': 1,
        'duracion': 6,
        'estado': 'OCUPADA'
    },
    {
        'empresa': empresas_creadas[4],
        'titulo': 'Practicante de Soporte Técnico',
        'area': 'Infraestructura TI',
        'descripcion': 'Apoyo en la gestión de soporte técnico a usuarios, mantenimiento de equipos y administración de redes. Excelente oportunidad para aprender sobre infraestructura tecnológica.',
        'programa': 'Ingeniería de Sistemas',
        'semestre': 6,
        'cupos': 2,
        'duracion': 6,
        'estado': 'DISPONIBLE'
    },
]

for vac_data in vacantes_data:
    vacante, created = Vacante.objects.get_or_create(
        empresa=vac_data['empresa'],
        titulo=vac_data['titulo'],
        defaults={
            'area_practica': vac_data['area'],
            'descripcion': vac_data['descripcion'],
            'programa_academico': vac_data['programa'],
            'semestre_minimo': vac_data['semestre'],
            'cantidad_cupos': vac_data['cupos'],
            'cupos_ocupados': 1 if vac_data['estado'] == 'OCUPADA' else 0,
            'duracion_meses': vac_data['duracion'],
            'horario': 'Lunes a Viernes, 8:00 AM - 5:00 PM',
            'habilidades_requeridas': 'Trabajo en equipo, comunicación efectiva, proactividad',
            'estado': vac_data['estado'],
            'creada_por': coordinador,
            'fecha_publicacion': timezone.now()
        }
    )
    status = "✅ Creada" if created else "ℹ️  Ya existe"
    print(f"{status}: {vacante.titulo} - {vacante.empresa.razon_social}")

# ============================================
# 7. CREAR POSTULACIONES
# ============================================
print("\n📝 Creando Postulaciones...")

# Obtener vacantes y estudiantes
vacante_fullstack = Vacante.objects.filter(titulo__icontains='Full Stack').first()
vacante_ux = Vacante.objects.filter(titulo__icontains='UX').first()
vacante_marketing = Vacante.objects.filter(titulo__icontains='Marketing').first()

estudiante_juan = Estudiante.objects.filter(codigo='2020001').first()
estudiante_maria = Estudiante.objects.filter(codigo='2020002').first()
estudiante_andres = Estudiante.objects.filter(codigo='2020003').first()
estudiante_carolina = Estudiante.objects.filter(codigo='2019004').first()

postulaciones_crear = []

if vacante_fullstack and estudiante_juan:
    postulaciones_crear.append({
        'vacante': vacante_fullstack,
        'estudiante': estudiante_juan,
        'estado': 'POSTULADO'
    })

if vacante_fullstack and estudiante_maria:
    postulaciones_crear.append({
        'vacante': vacante_fullstack,
        'estudiante': estudiante_maria,
        'estado': 'SELECCIONADO'
    })

if vacante_ux and estudiante_andres:
    postulaciones_crear.append({
        'vacante': vacante_ux,
        'estudiante': estudiante_andres,
        'estado': 'POSTULADO'
    })

if vacante_marketing and estudiante_carolina:
    postulaciones_crear.append({
        'vacante': vacante_marketing,
        'estudiante': estudiante_carolina,
        'estado': 'VINCULADO'
    })

for post_data in postulaciones_crear:
    postulacion, created = Postulacion.objects.get_or_create(
        vacante=post_data['vacante'],
        estudiante=post_data['estudiante'],
        defaults={
            'postulado_por': coordinador,
            'estado': post_data['estado'],
            'observaciones': 'Estudiante con excelente perfil académico'
        }
    )
    status = "✅ Creada" if created else "ℹ️  Ya existe"
    print(f"{status}: {postulacion.estudiante.nombre_completo} -> {postulacion.vacante.titulo}")

# ============================================
# 8. CREAR UNA PRÁCTICA EN CURSO
# ============================================
print("\n🎯 Creando Práctica en Curso...")

if estudiante_carolina and vacante_marketing:
    tutor = TutorEmpresarial.objects.filter(empresa=vacante_marketing.empresa).first()
    docente = DocenteAsesor.objects.first()

    if tutor and docente:
        practica, created = PracticaEmpresarial.objects.get_or_create(
            estudiante=estudiante_carolina,
            empresa=vacante_marketing.empresa,
            defaults={
                'vacante': vacante_marketing,
                'tutor_empresarial': tutor,
                'docente_asesor': docente,
                'fecha_inicio': date.today() - timedelta(days=60),
                'fecha_fin_estimada': date.today() + timedelta(days=120),
                'estado': 'EN_CURSO',
                'plan_aprobado': True,
                'asignada_por': coordinador,
                'observaciones': 'Práctica iniciada correctamente'
            }
        )

        if created:
            # Actualizar estado del estudiante
            estudiante_carolina.estado = 'EN_PRACTICA'
            estudiante_carolina.save()

            print(f"✅ Práctica creada: {practica.estudiante.nombre_completo} en {practica.empresa.razon_social}")
        else:
            print(f"ℹ️  Práctica ya existe")

# ============================================
# RESUMEN FINAL
# ============================================
print("\n" + "=" * 60)
print("📊 RESUMEN DE DATOS CREADOS")
print("=" * 60)
print(f"👥 Coordinadores: {Coordinador.objects.count()}")
print(f"🏢 Empresas: {Empresa.objects.count()}")
print(f"   - Aprobadas: {Empresa.objects.filter(estado='APROBADA').count()}")
print(f"   - Pendientes: {Empresa.objects.filter(estado='PENDIENTE').count()}")
print(f"💼 Vacantes: {Vacante.objects.count()}")
print(f"   - Disponibles: {Vacante.objects.filter(estado='DISPONIBLE').count()}")
print(f"   - Ocupadas: {Vacante.objects.filter(estado='OCUPADA').count()}")
print(f"🎓 Estudiantes: {Estudiante.objects.count()}")
print(f"   - Aptos: {Estudiante.objects.filter(estado='APTO').count()}")
print(f"   - En Práctica: {Estudiante.objects.filter(estado='EN_PRACTICA').count()}")
print(f"👔 Tutores Empresariales: {TutorEmpresarial.objects.count()}")
print(f"👨‍🏫 Docentes Asesores: {DocenteAsesor.objects.count()}")
print(f"📝 Postulaciones: {Postulacion.objects.count()}")
print(f"🎯 Prácticas: {PracticaEmpresarial.objects.count()}")

print("\n" + "=" * 60)
print("✅ POBLACIÓN DE DATOS COMPLETADA")
print("=" * 60)

print("\n🔑 CREDENCIALES DE ACCESO:")
print("-" * 60)
print("Coordinador:")
print("  Usuario: coordinador")
print("  Contraseña: admin123")
print("\nEstudiantes:")
print("  Usuario: est2020001, est2020002, etc.")
print("  Contraseña: estudiante123")
print("\nDocentes:")
print("  Usuario: carlos.rodriguez, diana.perez, etc.")
print("  Contraseña: docente123")
print("-" * 60)