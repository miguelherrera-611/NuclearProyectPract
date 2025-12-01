# ✅ FOTO DE PERFIL DE COORDINADOR - IMPLEMENTACIÓN COMPLETA
**Fecha:** 30 de Noviembre de 2025

## 🎯 OBJETIVO
Mostrar la foto de perfil del coordinador en **TODAS** las secciones del sistema (empresas, vacantes, postulaciones, tutores, sustentaciones, prácticas, reportes, etc.)

---

## ✅ LO QUE SE IMPLEMENTÓ

### 1. **Context Processor** (Inyección Automática)
**Archivo:** `coordinacion/context_processors.py`

```python
def coordinador_data(request):
    """Añade el objeto coordinador al contexto de todos los templates"""
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'coordinador'):
        context['coordinador'] = request.user.coordinador
    return context
```

**Ventaja:** Ya no necesitas pasar `coordinador` manualmente en cada vista. Está disponible en **TODOS** los templates automáticamente.

---

### 2. **Registro en settings.py**
**Archivo:** `config/settings.py`

Agregado al `TEMPLATES['OPTIONS']['context_processors']`:
```python
'coordinacion.context_processors.coordinador_data',  # Foto de perfil coordinador
```

---

### 3. **Snippet Reutilizable**
**Archivo:** `coordinacion/templates/coordinacion/_navbar_user_dropdown.html`

Dropdown del navbar con:
- ✅ Foto de perfil circular (32x32px)
- ✅ Icono por defecto si no hay foto
- ✅ Nombre del coordinador
- ✅ Enlace a "Mi Perfil"
- ✅ Enlace a "Cerrar Sesión"

```html
{% if coordinador.foto_perfil %}
    <img src="{{ coordinador.foto_perfil.url }}" class="rounded-circle" ...>
{% else %}
    <i class="fas fa-user-circle"></i>
{% endif %}
{{ coordinador.nombre_completo }}
```

---

### 4. **Templates Actualizados**
**Total:** ~40 archivos HTML

Todos los templates con navbar ahora usan:
```django
{% include 'coordinacion/_navbar_user_dropdown.html' %}
```

**Secciones afectadas:**
- ✅ Dashboard
- ✅ Empresas (lista, crear, editar, detalle, validar)
- ✅ Vacantes (lista, crear, editar, detalle)
- ✅ Estudiantes (lista, detalle)
- ✅ Postulaciones (lista, crear, editar, detalle, aprobar, rechazar)
- ✅ Prácticas (lista, detalle, crear, cancelar)
- ✅ Tutores (lista, crear, editar, detalle)
- ✅ Docentes Asesores (lista, crear, editar, detalle)
- ✅ Sustentaciones (lista, crear, editar, detalle, eliminar)
- ✅ Reportes
- ✅ Perfil

---

## 📋 FORMULARIO Y VISTA DE PERFIL

### Formulario: `CoordinadorPerfilForm`
**Archivo:** `coordinacion/forms.py`

Campos editables:
- `nombre_completo`
- `email`
- `telefono`
- `foto_perfil` (acepta imágenes)

### Vista: `perfil_coordinador`
**Archivo:** `coordinacion/views.py`

- Permite ver y editar perfil
- Sube archivos con `request.FILES`
- Mensaje de éxito al guardar
- Redirige a `/coordinacion/perfil/`

### URL: `/coordinacion/perfil/`
**Archivo:** `coordinacion/urls.py`

```python
path('perfil/', views.perfil_coordinador, name='perfil'),
```

### Template: `perfil.html`
**Archivo:** `coordinacion/templates/coordinacion/perfil.html`

- Card con foto actual (150x150px circular)
- Formulario para editar datos
- Input para subir nueva foto
- Botones: Volver / Guardar

---

## 🎨 DISEÑO VISUAL

### En el Navbar (arriba a la derecha):
```
┌────────────────────────────────────┐
│  [🏠 Dashboard] [📊 Reportes]      │
│                                    │
│              [👤foto] María ▼      │  ← Foto circular + nombre + dropdown
│                └─────┬──────┘      │
│                      │             │
│              ┌───────▼──────────┐  │
│              │ 👤 Mi Perfil     │  │
│              │ ──────────────── │  │
│              │ 🚪 Cerrar Sesión │  │
│              └──────────────────┘  │
└────────────────────────────────────┘
```

### En el Perfil:
```
┌───────────────────────────────┐
│       Mi Perfil               │
├───────────────────────────────┤
│                               │
│          [👤foto]             │  ← Foto actual 150x150px
│                               │
│  Nombre: [______________]     │
│  Email:  [______________]     │
│  Tel:    [______________]     │
│  Foto:   [Elegir archivo]     │
│                               │
│  [← Volver]    [💾 Guardar]  │
└───────────────────────────────┘
```

---

## 🚀 CÓMO USAR

### Como Coordinador:

1. **Accede a cualquier sección** (Empresas, Vacantes, etc.)
2. **Verás tu foto** arriba a la derecha junto a tu nombre
3. **Haz clic** en tu nombre → "Mi Perfil"
4. **Sube una foto** desde el input
5. **Guardar** → La foto aparece en **TODAS** las secciones

### Subir Foto:
- Formatos: JPG, PNG, GIF
- Se guarda en: `media/coordinadores/fotos_perfil/`
- Se muestra: Automáticamente en todos los navbars

---

## 🔧 ARCHIVOS CLAVE

```
coordinacion/
├── context_processors.py          ← Context processor (NUEVO)
├── forms.py                        ← CoordinadorPerfilForm agregado
├── views.py                        ← perfil_coordinador() agregado
├── urls.py                         ← path('perfil/') agregado
└── templates/
    └── coordinacion/
        ├── _navbar_user_dropdown.html  ← Snippet reutilizable (NUEVO)
        ├── perfil.html                 ← Template de perfil (NUEVO)
        ├── dashboard.html              ← Actualizado
        ├── vacantes/*.html             ← Actualizados
        ├── empresas/*.html             ← Actualizados
        ├── postulaciones/*.html        ← Actualizados
        ├── practicas/*.html            ← Actualizados
        ├── tutores/*.html              ← Actualizados
        ├── sustentaciones/*.html       ← Actualizados
        └── reportes/dashboard.html     ← Actualizado

config/
└── settings.py                     ← context_processor agregado
```

---

## ✅ RESULTADO FINAL

### Antes:
```
[👤 usuario] ▼
└─ Cerrar Sesión
```

### Ahora:
```
[🖼️foto] María García ▼
├─ 👤 Mi Perfil
└─ 🚪 Cerrar Sesión
```

**En TODAS las secciones:**
✅ Dashboard
✅ Empresas  
✅ Vacantes
✅ Estudiantes
✅ Postulaciones
✅ Prácticas
✅ Tutores
✅ Docentes Asesores
✅ Sustentaciones
✅ Reportes

---

## 🎉 VENTAJAS DE ESTA IMPLEMENTACIÓN

1. **✅ DRY (Don't Repeat Yourself):** Un solo snippet reutilizable
2. **✅ Automático:** Context processor inyecta `coordinador` en todos los templates
3. **✅ Mantenible:** Cambios en un solo archivo afectan todo
4. **✅ Consistente:** Mismo diseño en todas las secciones
5. **✅ Escalable:** Fácil agregar más datos al context processor

---

**Estado:** ✅ **COMPLETADO Y FUNCIONANDO**  
**Archivos modificados:** 45+  
**Resultado:** Foto de perfil visible en TODO el sistema de coordinación 🎨✨

