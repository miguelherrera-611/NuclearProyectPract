import os
import glob

print("=" * 60)
print("ACTUALIZANDO TOP-BAR DE DOCENTE CON DROPDOWN")
print("=" * 60)

# Patrón antiguo (sin dropdown) - versión 1
old_pattern_1 = """    <div class="user-info">
        <div class="user-avatar">
            <i class="fas fa-chalkboard-teacher"></i>
        </div>
        <div class="user-details">
            <strong>{{ docente.nombre_completo }}</strong>
            <small>Docente Asesor</small>
        </div>
    </div>"""

# Patrón antiguo (sin dropdown) - versión 2 con foto
old_pattern_2 = """    <div class="user-info">
        <div class="user-avatar" style="width: 40px; height: 40px; border-radius: 50%; overflow: hidden; background: linear-gradient(135deg, var(--primary-blue), var(--accent-blue)); display: flex; align-items: center; justify-content: center;">
            {% if docente_actual.foto_perfil %}
                <img src="{{ docente_actual.foto_perfil.url }}" alt="{{ docente_actual.nombre_completo }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% else %}
                <i class="fas fa-chalkboard-teacher"></i>
            {% endif %}
        </div>
        <div class="user-details">
            <strong>{{ docente_actual.nombre_completo|default:user.username }}</strong>
            <small>Docente Asesor</small>
        </div>
    </div>"""

# Patrón nuevo (con dropdown)
new_pattern = """    {% include 'docente/_topbar_user_dropdown.html' %}"""

base_path = r"C:\Users\maho4\PycharmProjects\DjangoProject\docente\templates\docente"
html_files = glob.glob(os.path.join(base_path, "*.html"))

# Excluir archivos
exclude_files = ['base.html', '_topbar_user_dropdown.html']

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

        if old_pattern_1 in content:
            new_content = content.replace(old_pattern_1, new_pattern)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ {filename} (patrón 1)")
            updated_files.append(filename)
            count += 1
        elif old_pattern_2 in content:
            new_content = content.replace(old_pattern_2, new_pattern)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ {filename} (patrón 2)")
            updated_files.append(filename)
            count += 1

    except Exception as e:
        print(f"❌ Error en {filename}: {e}")

print("\n" + "=" * 60)
print(f"🎉 COMPLETADO: {count} archivos actualizados")
print("=" * 60)

if updated_files:
    print("\nArchivos actualizados:")
    for f in updated_files:
        print(f"  • {f}")

