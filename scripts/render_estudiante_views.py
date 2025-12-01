import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.utils import timezone
from coordinacion.models import Estudiante, Empresa, Vacante, Coordinador, Postulacion
from Estudiante import estudiante_views

# Crear datos mínimos
user, created = User.objects.get_or_create(username='rf_user', defaults={'email':'rf_user@example.com'})
if created:
    user.set_password('test')
    user.save()
est, ecr = Estudiante.objects.get_or_create(user=user, defaults={
    'codigo':'RF001', 'nombre_completo':'RF Estudiante', 'email':'rf@example.com', 'telefono':'0', 'programa_academico':'Ingenieria', 'semestre':5
})
coord_user, _ = User.objects.get_or_create(username='rf_coord', defaults={'email':'rf_coord@example.com'})
coord, _ = Coordinador.objects.get_or_create(user=coord_user, defaults={'nombre_completo':'RF Coord', 'email':'rf_coord@example.com'})
empresa, _ = Empresa.objects.get_or_create(nit='RF001', defaults={'razon_social':'RF Empresa','direccion':'X','telefono':'1','email':'e@e.com','ciudad':'C','representante_nombre':'R','representante_cargo':'G','representante_email':'r@e.com','representante_telefono':'1'})
vac, _ = Vacante.objects.get_or_create(titulo='RF Vacante', empresa=empresa, creada_por=coord, defaults={'area_practica':'Dev','descripcion':'D','cantidad_cupos':2,'cupos_ocupados':0,'programa_academico':'Ingenieria','semestre_minimo':4,'horario':'D','duracion_meses':6,'estado':'DISPONIBLE','fecha_publicacion':timezone.now()})
postu, _ = Postulacion.objects.get_or_create(vacante=vac, estudiante=est, defaults={'postulado_por':coord,'estado':'POSTULADO'})

# Preparar RequestFactory + middlewares
rf = RequestFactory()
req1 = rf.get('/estudiante/vacantes/')
req1.user = user
# Apply session and messages middleware (crear middlewares con get_response dummy)
dummy = lambda request: None
session_mw = SessionMiddleware(dummy)
msg_mw = MessageMiddleware(dummy)
session_mw.process_request(req1)
req1.session.save()
msg_mw.process_request(req1)

# Call view
resp1 = estudiante_views.vacantes_disponibles(req1)
content1 = getattr(resp1, 'content', b'').decode('utf-8', 'replace')
open('tmp_vacantes_rf.html','w', encoding='utf-8').write(content1)
print('VACANTES rendered length:', len(content1))

req2 = rf.get('/estudiante/postulaciones/')
req2.user = user
session_mw.process_request(req2)
req2.session.save()
msg_mw.process_request(req2)
resp2 = estudiante_views.mis_postulaciones(req2)
content2 = getattr(resp2, 'content', b'').decode('utf-8', 'replace')
open('tmp_postulaciones_rf.html','w', encoding='utf-8').write(content2)
print('POSTULACIONES rendered length:', len(content2))
print('Done')
