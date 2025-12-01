import os
import glob

# Patrón a buscar y reemplazar
old_pattern = """            <ul class="navbar-nav ms-auto">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user-circle me-1"></i>{{ request.user.username }}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="{% url 'coordinacion:logout' %}">
                            <i class="fas fa-sign-out-alt me-2"></i>Cerrar Sesión
                        </a></li>
                    </ul>
                </li>
            </ul>"""

new_pattern = """            <ul class="navbar-nav ms-auto">
                {% include 'coordinacion/_navbar_user_dropdown.html' %}
            </ul>"""

# Buscar todos los archivos HTML en coordinacion/templates
base_path = r"C:\Users\maho4\PycharmProjects\DjangoProject\coordinacion\templates\coordinacion"
html_files = glob.glob(os.path.join(base_path, "**", "*.html"), recursive=True)

# Excluir archivos que no deben modificarse
exclude_files = ['_navbar_user_dropdown.html', 'base.html', 'dashboard.html', 'perfil.html']

count = 0
for filepath in html_files:
    filename = os.path.basename(filepath)

    if filename in exclude_files:
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_pattern in content:
            new_content = content.replace(old_pattern, new_pattern)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ {filename}")
            count += 1
    except Exception as e:
        print(f"❌ Error en {filename}: {e}")

print(f"\n🎉 Total actualizados: {count} archivos")

