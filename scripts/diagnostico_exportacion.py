"""
Script para diagnosticar y verificar las URLs de exportación
"""
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.insert(0, r'C:\Users\maho4\PycharmProjects\DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

print("=" * 70)
print("🔍 DIAGNÓSTICO DE URLS DE EXPORTACIÓN")
print("=" * 70)

# 1. Verificar que las funciones existen
print("\n1️⃣ Verificando funciones en views.py...")
try:
    from coordinacion.views import exportar_reportes_excel, exportar_reportes_pdf
    print("   ✅ exportar_reportes_excel - ENCONTRADA")
    print("   ✅ exportar_reportes_pdf - ENCONTRADA")
except ImportError as e:
    print(f"   ❌ ERROR al importar: {e}")
    sys.exit(1)

# 2. Verificar URLconf
print("\n2️⃣ Verificando URLconf...")
try:
    from coordinacion.urls import urlpatterns
    print(f"   Total de patrones en coordinacion/urls.py: {len(urlpatterns)}")

    # Buscar las URLs de exportación
    excel_found = False
    pdf_found = False

    for pattern in urlpatterns:
        pattern_str = str(pattern.pattern)
        if 'exportar-excel' in pattern_str:
            excel_found = True
            print(f"   ✅ Patrón Excel encontrado: {pattern_str}")
        if 'exportar-pdf' in pattern_str:
            pdf_found = True
            print(f"   ✅ Patrón PDF encontrado: {pattern_str}")

    if not excel_found:
        print("   ❌ Patrón Excel NO encontrado")
    if not pdf_found:
        print("   ❌ Patrón PDF NO encontrado")

except Exception as e:
    print(f"   ❌ ERROR: {e}")

# 3. Verificar el URLconf principal
print("\n3️⃣ Verificando config/urls.py...")
try:
    from config.urls import urlpatterns as main_patterns
    print(f"   Total de patrones principales: {len(main_patterns)}")

    for pattern in main_patterns:
        if hasattr(pattern, 'url_patterns'):
            # Es un include
            if 'coordinacion' in str(pattern.pattern):
                print(f"   ✅ Include de coordinación encontrado")

except Exception as e:
    print(f"   ❌ ERROR: {e}")

# 4. Intentar resolver las URLs
print("\n4️⃣ Intentando resolver las URLs...")
try:
    from django.urls import reverse

    try:
        url_excel = reverse('coordinacion:exportar_reportes_excel')
        print(f"   ✅ URL Excel resuelve a: {url_excel}")
    except Exception as e:
        print(f"   ❌ URL Excel NO se puede resolver: {e}")

    try:
        url_pdf = reverse('coordinacion:exportar_reportes_pdf')
        print(f"   ✅ URL PDF resuelve a: {url_pdf}")
    except Exception as e:
        print(f"   ❌ URL PDF NO se puede resolver: {e}")

except Exception as e:
    print(f"   ❌ ERROR general: {e}")

print("\n" + "=" * 70)
print("📋 CONCLUSIÓN:")
print("=" * 70)
print("""
Si las funciones existen pero las URLs no se resuelven, entonces:

⚠️  EL SERVIDOR DE DJANGO ESTÁ USANDO UNA VERSIÓN EN CACHÉ

SOLUCIÓN:
1. Ve a la terminal donde corre Django
2. Presiona Ctrl + C para detener el servidor
3. Ejecuta: python manage.py runserver
4. Vuelve a probar: http://127.0.0.1:8000/coordinacion/reportes/exportar-excel/

Si después de reiniciar aún no funciona, ejecuta:
python manage.py check
python manage.py validate_templates (si existe)
""")
print("=" * 70)

