import os
import glob
import re

print("=" * 60)
print("LIMPIANDO LÍNEAS VACÍAS EN SIDEBARS DE ESTUDIANTE")
print("=" * 60)

base_path = r"C:\Users\maho4\PycharmProjects\DjangoProject\Estudiante\templates\estudiante"
html_files = glob.glob(os.path.join(base_path, "**", "*.html"), recursive=True)

# Excluir archivos que no tienen sidebar
exclude_files = ['base.html', 'registro.html', 'login.html.old', 'registro.html.old', 
                 'seleccionar_rol.html', 'chat.html', 'no_apto.html', 'dashboard.html']

count = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    
    # Saltar archivos excluidos
    if filename in exclude_files:
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar y reemplazar el patrón con línea vacía
        pattern = r'(<i class="fas fa-home me-2"></i>Dashboard\s*</a>)\s*\n\s*\n\s*(<a href=)'
        replacement = r'\1\n                \2'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            relative_path = filepath.replace(base_path + "\\", "")
            print(f"✅ {relative_path}")
            count += 1
            
    except Exception as e:
        print(f"❌ Error en {filename}: {e}")

print(f"\n🎉 Limpiadas {count} líneas vacías")

