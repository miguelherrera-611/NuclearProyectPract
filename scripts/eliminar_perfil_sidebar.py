import os
import glob

print("=" * 60)
print("ELIMINANDO 'MI PERFIL' DEL SIDEBAR EN TEMPLATES DE ESTUDIANTE")
print("=" * 60)

# Línea a eliminar del sidebar
line_to_remove = """                <a href="{% url 'estudiante:perfil' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-user-edit me-2"></i>Mi Perfil
                </a>"""

# También manejar variaciones con active
line_to_remove_active = """                <a href="{% url 'estudiante:perfil' %}" class="list-group-item list-group-item-action active">
                    <i class="fas fa-user-edit me-2"></i>Mi Perfil
                </a>"""

base_path = r"C:\Users\maho4\PycharmProjects\DjangoProject\Estudiante\templates\estudiante"
html_files = glob.glob(os.path.join(base_path, "**", "*.html"), recursive=True)

# Excluir archivos que no tienen sidebar
exclude_files = ['base.html', 'registro.html', 'login.html.old', 'registro.html.old',
                 'seleccionar_rol.html', 'chat.html', 'no_apto.html']

count = 0
updated_files = []

for filepath in html_files:
    filename = os.path.basename(filepath)

    # Saltar archivos excluidos
    if filename in exclude_files:
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False

        # Eliminar versión normal
        if line_to_remove in content:
            content = content.replace(line_to_remove, "")
            modified = True

        # Eliminar versión con active
        if line_to_remove_active in content:
            content = content.replace(line_to_remove_active, "")
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            relative_path = filepath.replace(base_path + "\\", "")
            print(f"✅ {relative_path}")
            updated_files.append(relative_path)
            count += 1

    except Exception as e:
        print(f"❌ Error en {filename}: {e}")

print("\n" + "=" * 60)
print(f"🎉 COMPLETADO: {count} archivos actualizados")
print("=" * 60)

if updated_files:
    print("\nArchivos modificados:")
    for f in updated_files:
        print(f"  • {f}")
else:
    print("\n⚠️ No se encontraron archivos para actualizar")

