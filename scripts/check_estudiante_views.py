import os
import sys
import django
# Asegurar que la raíz del proyecto esté en sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
from coordinacion.models import Estudiante, Empresa, Vacante, Coordinador, Postulacion

print('Starting check_estudiante_views')
# Create or get test user
user, created = User.objects.get_or_create(username='test_est', defaults={'email':'test_est@example.com'})
print('User test_est created?', created)
if created:
    user.set_password('test123')
    user.save()

# Create or get estudiante object
est, ecr = Estudiante.objects.get_or_create(user=user, defaults={
    'codigo':'T001',
    'nombre_completo':'Estudiante Prueba',
    'email':'test_est@example.com',
    'telefono':'000',
    'programa_academico':'Ingenieria',
    'semestre':5,
})
print('Estudiante created?', ecr, 'Estudiante id:', est.id)
if not ecr:
    est.nombre_completo = est.nombre_completo or 'Estudiante Prueba'
    est.programa_academico = est.programa_academico or 'Ingenieria'
    est.semestre = est.semestre or 5
    est.save()

# Create coordinator and company and a vacante
coord_user, ccreated = User.objects.get_or_create(username='test_coord', defaults={'email':'coord@example.com'})
print('Coord user created?', ccreated)
if ccreated:
    coord_user.set_password('coord123')
    coord_user.save()
coord, ccr = Coordinador.objects.get_or_create(user=coord_user, defaults={'nombre_completo':'Coord Prueba','email':'coord@example.com'})
print('Coordinador created?', ccr)

empresa, empc = Empresa.objects.get_or_create(nit='0001', defaults={
    'razon_social':'Empresa Prueba',
    'direccion':'Av. Test 1',
    'telefono':'111',
    'email':'empresa@example.com',
    'ciudad':'Ciudad',
    'representante_nombre':'Rep',
    'representante_cargo':'Gerente',
    'representante_email':'rep@example.com',
    'representante_telefono':'222',
})
print('Empresa created?', empc)

vac, vcr = Vacante.objects.get_or_create(
    titulo='Vacante Prueba',
    empresa=empresa,
    creada_por=coord,
    defaults={
        'area_practica':'Desarrollo',
        'descripcion':'Descripcion prueba',
        'cantidad_cupos':2,
        'cupos_ocupados':0,
        'programa_academico':'Ingenieria',
        'semestre_minimo':4,
        'horario':'Diurno',
        'duracion_meses':6,
        'estado':'DISPONIBLE',
        'fecha_publicacion': timezone.now(),
    }
)
print('Vacante created?', vcr, 'Vacante id:', vac.id)

postu, pcr = Postulacion.objects.get_or_create(vacante=vac, estudiante=est, defaults={'postulado_por':coord, 'estado':'POSTULADO'})
print('Postulacion created?', pcr)

client = Client(HTTP_HOST='127.0.0.1')
client.force_login(user)

r1 = client.get('/estudiante/vacantes/')
print('VACANTES STATUS', r1.status_code, 'templates', [t.name for t in r1.templates])
open('tmp_vacantes_response.html','wb').write(r1.content)
print('Saved tmp_vacantes_response.html, length', len(r1.content))

r2 = client.get('/estudiante/postulaciones/')
print('POSTULACIONES STATUS', r2.status_code, 'templates', [t.name for t in r2.templates])
open('tmp_postulaciones_response.html','wb').write(r2.content)
print('Saved tmp_postulaciones_response.html, length', len(r2.content))

print('Done')
