import os
import glob

# ===== ESTUDIANTE =====
print("=" * 50)
print("ACTUALIZANDO NAVBARS DE ESTUDIANTE")
print("=" * 50)

old_pattern_estudiante = """                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user-circle me-1"></i>
                        {{ estudiante.nombre_completo }}
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

new_pattern_estudiante = """                <li class="nav-item dropdown">
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

base_path_estudiante = r"C:\Users\maho4\PycharmProjects\DjangoProject\Estudiante\templates\estudiante"
html_files_estudiante = glob.glob(os.path.join(base_path_estudiante, "**", "*.html"), recursive=True)

count_estudiante = 0
for filepath in html_files_estudiante:
    filename = os.path.basename(filepath)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_pattern_estudiante in content:
            new_content = content.replace(old_pattern_estudiante, new_pattern_estudiante)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ {filename}")
            count_estudiante += 1
    except Exception as e:
        print(f"❌ Error en {filename}: {e}")

print(f"\n🎉 Estudiante: {count_estudiante} archivos actualizados\n")

# ===== DOCENTE =====
print("=" * 50)
print("ACTUALIZANDO NAVBARS DE DOCENTE")
print("=" * 50)

old_pattern_docente = """        <div class="user-info">
        <div class="user-avatar">
            <i class="fas fa-chalkboard-teacher"></i>
        </div>
        <div class="user-details">
            <strong>{{ docente.nombre_completo }}</strong>
            <small>Docente Asesor</small>
        </div>
    </div>"""

new_pattern_docente = """        <div class="user-info">
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

base_path_docente = r"C:\Users\maho4\PycharmProjects\DjangoProject\docente\templates\docente"
html_files_docente = glob.glob(os.path.join(base_path_docente, "**", "*.html"), recursive=True)

count_docente = 0
for filepath in html_files_docente:
    filename = os.path.basename(filepath)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_pattern_docente in content:
            new_content = content.replace(old_pattern_docente, new_pattern_docente)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ {filename}")
            count_docente += 1
    except Exception as e:
        print(f"❌ Error en {filename}: {e}")

print(f"\n🎉 Docente: {count_docente} archivos actualizados\n")

# RESUMEN
print("=" * 50)
print("RESUMEN FINAL")
print("=" * 50)
print(f"✅ Estudiante: {count_estudiante} archivos")
print(f"✅ Docente: {count_docente} archivos")
print(f"🎉 TOTAL: {count_estudiante + count_docente} archivos actualizados")

