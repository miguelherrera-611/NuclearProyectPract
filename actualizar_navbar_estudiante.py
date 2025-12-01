import os
import glob

print("=" * 60)
print("ACTUALIZANDO NAVBARS DE ESTUDIANTE CON FOTO DE PERFIL")
print("=" * 60)

# Patrón antiguo (sin foto)
old_pattern = """                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user-circle me-1"></i>
                        Mi Cuenta
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <a class="dropdown-item" href="{% url 'estudiante:perfil' %}">
                                <i class="fas fa-user-edit me-2"></i>Mi Perfil
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item text-danger" href="{% url 'estudiante:logout' %}">
                                <i class="fas fa-sign-out-alt me-2"></i>Cerrar Sesión
                            </a>
                        </li>
                    </ul>
                </li>"""

# Patrón nuevo (con foto y nombre)
new_pattern = """                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" role="button" data-bs-toggle="dropdown">
                        {% if estudiante_actual.foto_perfil %}
                            <img src="{{ estudiante_actual.foto_perfil.url }}" 
                                 alt="{{ estudiante_actual.nombre_completo }}"
                                 class="rounded-circle me-2"
                                 style="width: 32px; height: 32px; object-fit: cover; border: 2px solid white;">
                        {% else %}
                            <i class="fas fa-user-circle me-2" style="font-size: 1.5rem;"></i>
                        {% endif %}
                        {{ estudiante_actual.nombre_completo|default:user.username }}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <a class="dropdown-item" href="{% url 'estudiante:perfil' %}">
                                <i class="fas fa-user-edit me-2"></i>Mi Perfil
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item text-danger" href="{% url 'estudiante:logout' %}">
                                <i class="fas fa-sign-out-alt me-2"></i>Cerrar Sesión
                            </a>
                        </li>
                    </ul>
                </li>"""

base_path = r"C:\Users\maho4\PycharmProjects\DjangoProject\Estudiante\templates\estudiante"
html_files = glob.glob(os.path.join(base_path, "**", "*.html"), recursive=True)

# Excluir archivos que no deben modificarse
exclude_files = ['base.html', 'registro.html', 'login.html.old', 'registro.html.old',
                 'seleccionar_rol.html', 'chat.html', 'dashboard.html', 'perfil.html']

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

        if old_pattern in content:
            new_content = content.replace(old_pattern, new_pattern)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            relative_path = filepath.replace(base_path + "\\", "")
            print(f"✅ {relative_path}")
            updated_files.append(relative_path)
            count += 1
        elif "Mi Cuenta" in content and "dropdown" in content:
            print(f"⚠️  {filename} - Tiene 'Mi Cuenta' pero patrón diferente")
    except Exception as e:
        print(f"❌ Error en {filename}: {e}")

print("\n" + "=" * 60)
print(f"🎉 COMPLETADO: {count} archivos actualizados")
print("=" * 60)

if updated_files:
    print("\nArchivos actualizados:")
    for f in updated_files:
        print(f"  • {f}")
else:
    print("\n⚠️ No se encontraron archivos para actualizar")

