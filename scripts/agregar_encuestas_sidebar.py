#!/usr/bin/env python
"""
Script para agregar el enlace de Encuestas en todos los sidebars de coordinación
"""
import os
import re

# Directorio base de templates de coordinación
BASE_DIR = r'C:\Users\maho4\PycharmProjects\DjangoProject\coordinacion\templates\coordinacion'

# Patrón a buscar (antes de Reportes)
PATTERN_BEFORE = r"(<a href=\"{% url 'coordinacion:sustentaciones_lista' %}\".*?>\s*<i class=\"fas fa-graduation-cap.*?\"></i>Sustentaciones\s*</a>)"

# Texto a insertar después de sustentaciones y antes de reportes
ENCUESTAS_LINK = '''                <a href="{% url 'coordinacion:encuestas_lista' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-poll-h me-2"></i>Encuestas
                </a>'''

def actualizar_template(filepath):
    """Actualiza un template agregando el enlace de encuestas si no existe"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si ya tiene el enlace de encuestas
    if "coordinacion:encuestas_lista" in content:
        print(f"✓ Ya tiene encuestas: {filepath}")
        return False

    # Buscar el patrón y agregar después de sustentaciones
    if "coordinacion:sustentaciones_lista" in content:
        # Reemplazar agregando el nuevo enlace después de sustentaciones
        new_content = re.sub(
            r"(</a>\s*\n\s*<a href=\"{% url 'coordinacion:reportes_dashboard' %}\")",
            f"\n{ENCUESTAS_LINK}\n                <a href=\"{{% url 'coordinacion:reportes_dashboard' %}}\"",
            content
        )

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Actualizado: {filepath}")
            return True
        else:
            print(f"⚠ No se pudo actualizar: {filepath}")
            return False
    else:
        print(f"⏭ No tiene sidebar estándar: {filepath}")
        return False

def main():
    """Función principal"""
    print("🔄 Actualizando templates de coordinación...\n")

    updated_count = 0
    skipped_count = 0

    # Recorrer todos los subdirectorios y archivos HTML
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if actualizar_template(filepath):
                    updated_count += 1
                else:
                    skipped_count += 1

    print(f"\n📊 Resumen:")
    print(f"  ✅ Archivos actualizados: {updated_count}")
    print(f"  ⏭ Archivos omitidos: {skipped_count}")
    print(f"\n✨ ¡Proceso completado!")

if __name__ == '__main__':
    main()

