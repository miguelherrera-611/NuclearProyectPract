import os, sys
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from coordinacion.models import Empresa

for e in Empresa.objects.all():
    print('ID', e.id)
    print('camara:', e.camara_comercio)
    try:
        print('camara.url:', e.camara_comercio.url)
    except Exception as ex:
        print('camara.url error:', ex)
    print('rut:', e.rut)
    try:
        print('rut.url:', e.rut.url)
    except Exception as ex:
        print('rut.url error:', ex)
    print('---')

