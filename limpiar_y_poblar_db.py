"""
Script para limpiar la base de datos y crear datos de prueba con las restricciones correctas.
Programas:
- Ingeniería de Software: Mínimo 4to semestre
- Ingeniería Industrial: Mínimo 4to semestre
- Administración de Empresas: Mínimo 2do semestre
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from coordinacion.models import (
    Coordinador, Estudiante, DocenteAsesor, Empresa,
    TutorEmpresarial, Vacante, Postulacion, PracticaEmpresarial,
    SeguimientoSemanal
)
from datetime import datetime, timedelta

def limpiar_base_datos():
    """Elimina todos los datos excepto superusuarios"""
    print("🗑️  Limpiando base de datos...")

    # Eliminar en orden correcto para evitar problemas de ForeignKey
    SeguimientoSemanal.objects.all().delete()
    PracticaEmpresarial.objects.all().delete()
    Postulacion.objects.all().delete()
    Vacante.objects.all().delete()
    TutorEmpresarial.objects.all().delete()
    Empresa.objects.all().delete()
    DocenteAsesor.objects.all().delete()
    Estudiante.objects.all().delete()
    Coordinador.objects.all().delete()

    # Eliminar usuarios que no sean superusuarios
    User.objects.filter(is_superuser=False).delete()

    print("✅ Base de datos limpiada\n")


def crear_coordinador():
    """Crea el coordinador de prácticas"""
    print("👔 Creando coordinador...")

    user = User.objects.create_user(
        username='coord001',
        password='coord123',
        email='coordinador@universidad.edu',
        first_name='María',
        last_name='García'
    )

    coordinador = Coordinador.objects.create(
        user=user,
        nombre_completo='María García Rodríguez',
        email='coordinador@universidad.edu',
        telefono='3001234567'
    )

    print(f"✅ Coordinador creado: {coordinador.nombre_completo}\n")
    return coordinador


def crear_docentes_asesores():
    """Crea 3 docentes asesores"""
    print("👨‍🏫 Creando docentes asesores...")

    docentes_data = [
        {
            'username': 'docente001',
            'password': 'doc123',
            'nombre_completo': 'Dr. Carlos Pérez López',
            'email': 'carlos.perez@universidad.edu',
            'telefono': '3101234567',
            'especialidad': 'Ingeniería de Software'
        },
        {
            'username': 'docente002',
            'password': 'doc123',
            'nombre_completo': 'Dra. Ana María Gómez',
            'email': 'ana.gomez@universidad.edu',
            'telefono': '3102234567',
            'especialidad': 'Ingeniería Industrial'
        },
        {
            'username': 'docente003',
            'password': 'doc123',
            'nombre_completo': 'Mg. Luis Alberto Torres',
            'email': 'luis.torres@universidad.edu',
            'telefono': '3103234567',
            'especialidad': 'Administración de Empresas'
        },
    ]

    docentes = []
    for data in docentes_data:
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['nombre_completo'].split()[1],
            last_name=data['nombre_completo'].split()[-1]
        )

        docente = DocenteAsesor.objects.create(
            user=user,
            nombre_completo=data['nombre_completo'],
            email=data['email'],
            telefono=data['telefono'],
            especialidad=data['especialidad']
        )

        docentes.append(docente)
        print(f"  ✅ {docente.nombre_completo} - {docente.especialidad}")

    print()
    return docentes


def crear_estudiantes():
    """Crea estudiantes de los 3 programas académicos"""
    print("🎓 Creando estudiantes...")

    estudiantes_data = [
        # Ingeniería de Software (mínimo 4to semestre)
        {
            'username': 'est001',
            'password': 'est123',
            'codigo': 'IS2021001',
            'nombre_completo': 'Juan Pablo Martínez',
            'email': 'juan.martinez@estudiante.edu',
            'telefono': '3201234567',
            'programa_academico': 'Ingeniería de Software',
            'semestre': 5,
            'promedio_academico': 4.2
        },
        {
            'username': 'est002',
            'password': 'est123',
            'codigo': 'IS2021002',
            'nombre_completo': 'María Camila Rodríguez',
            'email': 'maria.rodriguez@estudiante.edu',
            'telefono': '3202234567',
            'programa_academico': 'Ingeniería de Software',
            'semestre': 6,
            'promedio_academico': 4.5
        },
        {
            'username': 'est003',
            'password': 'est123',
            'codigo': 'IS2022001',
            'nombre_completo': 'Carlos Andrés López',
            'email': 'carlos.lopez@estudiante.edu',
            'telefono': '3203234567',
            'programa_academico': 'Ingeniería de Software',
            'semestre': 4,
            'promedio_academico': 4.0
        },

        # Ingeniería Industrial (mínimo 4to semestre)
        {
            'username': 'est004',
            'password': 'est123',
            'codigo': 'II2021001',
            'nombre_completo': 'Laura Valentina Gómez',
            'email': 'laura.gomez@estudiante.edu',
            'telefono': '3204234567',
            'programa_academico': 'Ingeniería Industrial',
            'semestre': 5,
            'promedio_academico': 4.3
        },
        {
            'username': 'est005',
            'password': 'est123',
            'codigo': 'II2021002',
            'nombre_completo': 'Santiago Hernández',
            'email': 'santiago.hernandez@estudiante.edu',
            'telefono': '3205234567',
            'programa_academico': 'Ingeniería Industrial',
            'semestre': 6,
            'promedio_academico': 4.1
        },

        # Administración de Empresas (mínimo 2do semestre)
        {
            'username': 'est006',
            'password': 'est123',
            'codigo': 'AE2022001',
            'nombre_completo': 'Daniela Alejandra Castro',
            'email': 'daniela.castro@estudiante.edu',
            'telefono': '3206234567',
            'programa_academico': 'Administración de Empresas',
            'semestre': 3,
            'promedio_academico': 4.4
        },
        {
            'username': 'est007',
            'password': 'est123',
            'codigo': 'AE2022002',
            'nombre_completo': 'Andrés Felipe Morales',
            'email': 'andres.morales@estudiante.edu',
            'telefono': '3207234567',
            'programa_academico': 'Administración de Empresas',
            'semestre': 4,
            'promedio_academico': 3.9
        },
        {
            'username': 'est008',
            'password': 'est123',
            'codigo': 'AE2023001',
            'nombre_completo': 'Isabella Ramírez',
            'email': 'isabella.ramirez@estudiante.edu',
            'telefono': '3208234567',
            'programa_academico': 'Administración de Empresas',
            'semestre': 2,
            'promedio_academico': 4.0
        },
    ]

    estudiantes = []
    for data in estudiantes_data:
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['nombre_completo'].split()[0],
            last_name=data['nombre_completo'].split()[-1]
        )

        # Determinar estado según el programa y semestre
        programa = data['programa_academico']
        semestre = data['semestre']

        if programa in ['Ingeniería de Software', 'Ingeniería Industrial']:
            estado = 'APTO' if semestre >= 4 else 'NO_APTO'
        else:  # Administración de Empresas
            estado = 'APTO' if semestre >= 2 else 'NO_APTO'

        estudiante = Estudiante.objects.create(
            user=user,
            codigo=data['codigo'],
            nombre_completo=data['nombre_completo'],
            email=data['email'],
            telefono=data['telefono'],
            programa_academico=data['programa_academico'],
            semestre=data['semestre'],
            promedio_academico=data['promedio_academico'],
            estado=estado
        )

        estudiantes.append(estudiante)
        print(f"  ✅ {estudiante.codigo} - {estudiante.nombre_completo} ({estudiante.programa_academico} - {estudiante.semestre}° sem) - {estudiante.estado}")

    print()
    return estudiantes


def crear_empresas_y_vacantes(coordinador):
    """Crea empresas con sus tutores y vacantes"""
    print("🏢 Creando empresas y vacantes...")

    empresas_data = [
        {
            'razon_social': 'TechSolutions S.A.S',
            'nit': '900123456-1',
            'direccion': 'Cra 7 #32-40, Bogotá',
            'telefono': '6013001234',
            'email': 'contacto@techsolutions.com',
            'ciudad': 'Bogotá',
            'representante_nombre': 'Carlos Alberto Pérez',
            'representante_cargo': 'Gerente General',
            'representante_email': 'carlos.perez@techsolutions.com',
            'representante_telefono': '3001112233',
            'tutor': {
                'nombre': 'Ing. Roberto Sánchez',
                'cargo': 'Director de TI',
                'email': 'roberto.sanchez@techsolutions.com',
                'telefono': '3301234567'
            },
            'vacantes': [
                {
                    'titulo': 'Practicante Desarrollo de Software',
                    'area_practica': 'Desarrollo de Software',
                    'descripcion': 'Apoyo en desarrollo de aplicaciones web con React y Django',
                    'programa_academico': 'Ingeniería de Software',
                    'semestre_minimo': 4,
                    'habilidades_requeridas': 'Python, JavaScript, React, Django',
                    'horario': 'Lunes a Viernes 8:00 AM - 2:00 PM',
                    'duracion_meses': 6,
                    'cantidad_cupos': 2
                }
            ]
        },
        {
            'razon_social': 'Manufacturas Industriales Ltda',
            'nit': '800234567-2',
            'direccion': 'Autopista Norte Km 15, Bogotá',
            'telefono': '6014002345',
            'email': 'rrhh@manufacturas.com',
            'ciudad': 'Bogotá',
            'representante_nombre': 'María Victoria Gómez',
            'representante_cargo': 'Gerente de Recursos Humanos',
            'representante_email': 'maria.gomez@manufacturas.com',
            'representante_telefono': '3002223344',
            'tutor': {
                'nombre': 'Ing. Patricia Vega',
                'cargo': 'Jefe de Producción',
                'email': 'patricia.vega@manufacturas.com',
                'telefono': '3302234567'
            },
            'vacantes': [
                {
                    'titulo': 'Practicante Ingeniería de Procesos',
                    'area_practica': 'Procesos Industriales',
                    'descripcion': 'Apoyo en optimización de procesos productivos',
                    'programa_academico': 'Ingeniería Industrial',
                    'semestre_minimo': 4,
                    'habilidades_requeridas': 'Lean Manufacturing, Six Sigma, Análisis de procesos',
                    'horario': 'Lunes a Viernes 7:00 AM - 1:00 PM',
                    'duracion_meses': 6,
                    'cantidad_cupos': 1
                }
            ]
        },
        {
            'razon_social': 'Comercializadora Global S.A',
            'nit': '900345678-3',
            'direccion': 'Av. El Dorado #68-55, Bogotá',
            'telefono': '6015003456',
            'email': 'info@comercializadora.com',
            'ciudad': 'Bogotá',
            'representante_nombre': 'Jorge Luis Ramírez',
            'representante_cargo': 'Gerente General',
            'representante_email': 'jorge.ramirez@comercializadora.com',
            'representante_telefono': '3003334455',
            'tutor': {
                'nombre': 'Adm. Claudia Moreno',
                'cargo': 'Gerente de Talento Humano',
                'email': 'claudia.moreno@comercializadora.com',
                'telefono': '3303234567'
            },
            'vacantes': [
                {
                    'titulo': 'Practicante Administración',
                    'area_practica': 'Gestión Administrativa',
                    'descripcion': 'Apoyo en gestión administrativa y comercial',
                    'programa_academico': 'Administración de Empresas',
                    'semestre_minimo': 2,
                    'habilidades_requeridas': 'Excel, gestión documental, atención al cliente',
                    'horario': 'Lunes a Viernes 8:00 AM - 3:00 PM',
                    'duracion_meses': 6,
                    'cantidad_cupos': 2
                }
            ]
        }
    ]

    empresas = []
    vacantes_todas = []

    for data in empresas_data:
        # Crear empresa
        empresa = Empresa.objects.create(
            razon_social=data['razon_social'],
            nit=data['nit'],
            direccion=data['direccion'],
            telefono=data['telefono'],
            email=data['email'],
            ciudad=data['ciudad'],
            representante_nombre=data['representante_nombre'],
            representante_cargo=data['representante_cargo'],
            representante_email=data['representante_email'],
            representante_telefono=data['representante_telefono'],
            estado='APROBADA',
            aprobada_por=coordinador
        )

        # Crear tutor empresarial
        tutor = TutorEmpresarial.objects.create(
            empresa=empresa,
            nombre_completo=data['tutor']['nombre'],
            cargo=data['tutor']['cargo'],
            email=data['tutor']['email'],
            telefono=data['tutor']['telefono']
        )

        print(f"  ✅ {empresa.razon_social}")
        print(f"     Tutor: {tutor.nombre_completo} - {tutor.cargo}")

        # Crear vacantes
        for vacante_data in data['vacantes']:
            vacante = Vacante.objects.create(
                empresa=empresa,
                titulo=vacante_data['titulo'],
                area_practica=vacante_data['area_practica'],
                descripcion=vacante_data['descripcion'],
                programa_academico=vacante_data['programa_academico'],
                semestre_minimo=vacante_data['semestre_minimo'],
                habilidades_requeridas=vacante_data['habilidades_requeridas'],
                horario=vacante_data['horario'],
                duracion_meses=vacante_data['duracion_meses'],
                cantidad_cupos=vacante_data['cantidad_cupos'],
                creada_por=coordinador,
                estado='DISPONIBLE'
            )
            vacantes_todas.append(vacante)
            print(f"     📋 {vacante.titulo} ({vacante.cantidad_cupos} cupos)")

        empresas.append(empresa)
        print()

    return empresas, vacantes_todas


def main():
    """Función principal"""
    print("="*80)
    print("🚀 SCRIPT DE INICIALIZACIÓN DE BASE DE DATOS")
    print("="*80)
    print()

    # Limpiar base de datos
    limpiar_base_datos()

    # Crear datos
    coordinador = crear_coordinador()
    docentes = crear_docentes_asesores()
    estudiantes = crear_estudiantes()
    empresas, vacantes = crear_empresas_y_vacantes(coordinador)

    # Resumen
    print("="*80)
    print("📊 RESUMEN DE DATOS CREADOS")
    print("="*80)
    print(f"✅ 1 Coordinador")
    print(f"✅ {len(docentes)} Docentes Asesores")
    print(f"✅ {len(estudiantes)} Estudiantes:")
    print(f"   - {len([e for e in estudiantes if e.programa_academico == 'Ingeniería de Software'])} Ingeniería de Software")
    print(f"   - {len([e for e in estudiantes if e.programa_academico == 'Ingeniería Industrial'])} Ingeniería Industrial")
    print(f"   - {len([e for e in estudiantes if e.programa_academico == 'Administración de Empresas'])} Administración de Empresas")
    print(f"✅ {len(empresas)} Empresas con {len(vacantes)} Vacantes")
    print()
    print("="*80)
    print("🎉 BASE DE DATOS INICIALIZADA CORRECTAMENTE")
    print("="*80)
    print()
    print("📝 CREDENCIALES DE ACCESO:")
    print("-" * 80)
    print("Coordinador:")
    print("  Usuario: coord001")
    print("  Contraseña: coord123")
    print()
    print("Docentes Asesores:")
    print("  Usuario: docente001, docente002, docente003")
    print("  Contraseña: doc123")
    print()
    print("Estudiantes:")
    print("  Usuario: est001, est002, est003, est004, est005, est006, est007, est008")
    print("  Contraseña: est123")
    print("="*80)


if __name__ == '__main__':
    main()

