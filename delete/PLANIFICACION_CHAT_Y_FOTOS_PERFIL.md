# PLANIFICACIÓN: SISTEMA DE CHAT Y FOTOS DE PERFIL - 30 Nov 2025

## 🎯 OBJETIVO

Implementar un sistema completo que incluya:

1. **Fotos de perfil** para todos los roles (Estudiante, Docente, Coordinador)
2. **Sección "Mi Docente Asesor"** en el sidebar de Estudiante
3. **Sistema de chat en tiempo real** entre Estudiante y Docente Asesor
4. **Vista de información del docente** para el estudiante
5. **Perfil de coordinador** con foto

---

## ✅ PASO 1: MODELOS (COMPLETADO)

### Cambios en Base de Datos:

1. **Modelo Estudiante** - Agregar campo `foto_perfil` ✅
2. **Modelo DocenteAsesor** - Agregar campo `foto_perfil` y `cedula` ✅
3. **Modelo Coordinador** - Agregar campo `foto_perfil` ✅
4. **Modelo Mensaje** - Crear modelo nuevo para el chat ✅
5. **Pillow instalado** - Librería para manejar imágenes ✅

### Migraciones Pendientes:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📋 PASO 2: FORMULARIOS Y VISTAS (PENDIENTE)

### 2.1 Actualizar Formularios de Perfil

**Archivos a modificar:**
- `Estudiante/estudiante_forms.py` - Agregar campo foto_perfil
- `docente/forms.py` - Agregar campo foto_perfil  
- `coordinacion/forms.py` - Agregar campo foto_perfil

### 2.2 Actualizar Vistas de Perfil

**Archivos a modificar:**
- `Estudiante/estudiante_views.py` - Vista `perfil`
- `docente/docente_views.py` - Vista `perfil_docente`
- `coordinacion/views.py` - Crear vista `perfil_coordinador`

### 2.3 Crear Vistas de Chat

**Nuevas vistas necesarias:**
```python
# Estudiante/estudiante_views.py
- mi_docente_asesor()  # Información del docente
- chat_con_docente()    # Vista del chat
- enviar_mensaje()      # AJAX para enviar
- obtener_mensajes()    # AJAX para recibir

# docente/docente_views.py
- chat_con_estudiante() # Vista del chat
- enviar_mensaje()      # AJAX para enviar
- obtener_mensajes()    # AJAX para recibir
```

---

## 🎨 PASO 3: TEMPLATES (PENDIENTE)

### 3.1 Actualizar Sidebar de Estudiante

**Archivo:** `Estudiante/templates/estudiante/base.html`

Agregar nueva sección:
```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'estudiante:mi_docente_asesor' %}">
        <i class="fas fa-chalkboard-teacher"></i>
        <span>Mi Docente Asesor</span>
    </a>
</li>
```

### 3.2 Crear Template de Información del Docente

**Nuevo archivo:** `Estudiante/templates/estudiante/mi_docente_asesor.html`

Contenido:
- Card con foto de perfil del docente
- Información de contacto
- Especialidad
- Botón grande para acceder al chat

### 3.3 Crear Template de Chat

**Nuevos archivos:**
- `Estudiante/templates/estudiante/chat.html`
- `docente/templates/docente/chat.html`

Características del chat:
- Foto de perfil arriba
- Nombre del otro usuario
- Área de mensajes con scroll
- Input para escribir
- Botón enviar
- Soporte para adjuntar archivos
- Actualización en tiempo real (AJAX/WebSocket)

### 3.4 Actualizar Templates de Perfil

**Archivos a modificar:**
- `Estudiante/templates/estudiante/perfil.html`
- `docente/templates/docente/perfil.html`
- `coordinacion/templates/coordinacion/perfil.html` (crear)

Agregar:
- Preview de foto actual
- Input para cargar nueva foto
- Botón para cambiar foto

### 3.5 Actualizar Navbars para Mostrar Foto

**Archivos a modificar:**
- `Estudiante/templates/estudiante/base.html`
- `docente/templates/docente/base.html`
- `coordinacion/templates/coordinacion/base.html`

Cambiar dropdown de usuario:
```html
<img src="{{ user.estudiante.foto_perfil.url }}" class="rounded-circle" width="32" height="32">
{{ user.estudiante.nombre_completo }}
```

---

## 🔗 PASO 4: URLS (PENDIENTE)

### 4.1 URLs de Estudiante

**Archivo:** `Estudiante/urls.py`

Agregar:
```python
path('mi-docente/', views.mi_docente_asesor, name='mi_docente_asesor'),
path('chat/', views.chat_con_docente, name='chat_con_docente'),
path('chat/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
path('chat/mensajes/', views.obtener_mensajes, name='obtener_mensajes'),
```

### 4.2 URLs de Docente

**Archivo:** `docente/urls.py`

Agregar:
```python
path('chat/<int:practica_id>/', views.chat_con_estudiante, name='chat_con_estudiante'),
path('chat/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
path('chat/mensajes/<int:practica_id>/', views.obtener_mensajes, name='obtener_mensajes'),
```

### 4.3 URLs de Coordinación

**Archivo:** `coordinacion/urls.py`

Agregar:
```python
path('perfil/', views.perfil_coordinador, name='perfil_coordinador'),
path('perfil/actualizar/', views.actualizar_perfil_coordinador, name='actualizar_perfil'),
```

---

## 💾 PASO 5: CONFIGURACIÓN DE MEDIA (PENDIENTE)

### 5.1 Settings.py

**Archivo:** `config/settings.py`

Verificar/Agregar:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 5.2 URLs principales

**Archivo:** `config/urls.py`

Agregar:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...existing patterns...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🎨 PASO 6: DISEÑO DEL CHAT (PENDIENTE)

### Características del Chat:

1. **Header del Chat:**
```
┌────────────────────────────────────┐
│ [←] 📷 Dr. Carlos Pérez López      │
│     Docente Asesor                  │
└────────────────────────────────────┘
```

2. **Área de Mensajes:**
```
┌────────────────────────────────────┐
│                                     │
│  Hola, tengo una duda              │
│  📄 evidencia.pdf    [Yo - 10:30]  │
│                                     │
│      [Docente - 10:35]             │
│      Claro, dime en qué            │
│      te puedo ayudar               │
│                                     │
└────────────────────────────────────┘
```

3. **Input de Mensaje:**
```
┌────────────────────────────────────┐
│ 📎 [Escribir mensaje...]    [📤]   │
└────────────────────────────────────┘
```

### Estilos CSS:

- Mensajes propios: Alineados a la derecha, fondo azul
- Mensajes del otro: Alineados a la izquierda, fondo gris
- Fotos de perfil redondas (32x32px)
- Scroll automático al último mensaje
- Indicador "escribiendo..."
- Marca de "leído" (✓✓)

---

## 🔧 PASO 7: JAVASCRIPT/AJAX (PENDIENTE)

### Funcionalidades Necesarias:

1. **Envío de Mensajes:**
```javascript
function enviarMensaje() {
    fetch('/estudiante/chat/enviar/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        agregarMensajeAlChat(data);
        scrollToBottom();
    });
}
```

2. **Actualización Automática:**
```javascript
setInterval(() => {
    obtenerNuevosMensajes();
}, 3000); // Cada 3 segundos
```

3. **Subir Archivos:**
```javascript
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    uploadFile(file);
});
```

4. **Preview de Foto de Perfil:**
```javascript
fotoInput.addEventListener('change', (e) => {
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.src = e.target.result;
    };
    reader.readAsDataURL(file);
});
```

---

## 📊 PASO 8: FUNCIONALIDADES ESPECÍFICAS

### 8.1 Sección "Mi Docente Asesor"

**Qué muestra:**
- Card con foto de perfil del docente (circular, grande)
- Nombre completo
- Email y teléfono
- Especialidad
- Badge: "Tu Asesor Asignado"
- Botón grande: "💬 Abrir Chat"
- Estadísticas: X mensajes sin leer

**Restricción:**
- Solo visible si el estudiante tiene práctica activa
- Si no tiene docente asignado: Mensaje "Aún no tienes docente asesor asignado"

### 8.2 Chat Funcional

**Funcionalidades:**
- Ver historial completo de mensajes
- Enviar texto
- Adjuntar archivos (PDF, imágenes)
- Ver fecha/hora de cada mensaje
- Marca de "leído" cuando el otro usuario abre el chat
- Notificación de mensajes nuevos (badge en sidebar)
- Scroll automático al último mensaje
- Responsive (funciona en móvil)

### 8.3 Fotos de Perfil

**Ubicaciones donde se muestran:**
- Navbar superior derecha (todos los roles)
- Página de perfil (preview grande)
- Chat (arriba, circular pequeña)
- Listado de estudiantes para el docente
- Listado de docentes para coordinación

**Foto por defecto:**
- Si no hay foto: Icono de usuario (fa-user-circle)
- O avatar con iniciales del nombre

---

## 🔐 PASO 9: SEGURIDAD Y VALIDACIONES

### Validaciones Necesarias:

1. **Fotos de Perfil:**
   - Solo imágenes (JPG, PNG, GIF)
   - Tamaño máximo: 5MB
   - Redimensionar automáticamente a 300x300px

2. **Chat:**
   - Solo entre estudiante y su docente asignado
   - Validar que la práctica existe
   - Sanitizar mensajes (evitar XSS)
   - Archivos adjuntos: Max 10MB

3. **Permisos:**
   - Estudiante solo ve su docente
   - Docente solo ve sus estudiantes
   - Mensajes privados (no accesibles por otros)

---

## 📝 PASO 10: MIGRACIÓN Y DATOS

### Crear Migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Datos de Ejemplo:
```python
# Crear carpetas para fotos
mkdir media/estudiantes/fotos_perfil
mkdir media/docentes/fotos_perfil  
mkdir media/coordinadores/fotos_perfil
mkdir media/mensajes/adjuntos
```

---

## 🚀 IMPLEMENTACIÓN POR FASES

### FASE 1: Fotos de Perfil (2-3 horas)
1. ✅ Modelos actualizados
2. ⏳ Formularios actualizados
3. ⏳ Vistas de perfil
4. ⏳ Templates de perfil
5. ⏳ Navbar con foto

### FASE 2: Sección "Mi Docente" (1 hora)
1. ⏳ Vista de información
2. ⏳ Template card docente
3. ⏳ Sidebar con enlace
4. ⏳ Validación de acceso

### FASE 3: Sistema de Chat (4-5 horas)
1. ⏳ Vistas de chat
2. ⏳ Templates de chat
3. ⏳ AJAX para mensajes
4. ⏳ CSS del chat
5. ⏳ JavaScript funcional
6. ⏳ Notificaciones de mensajes nuevos

### FASE 4: Pruebas y Ajustes (1 hora)
1. ⏳ Pruebas de envío/recepción
2. ⏳ Pruebas de adjuntos
3. ⏳ Pruebas de fotos
4. ⏳ Ajustes visuales
5. ⏳ Responsive

---

## 📍 ARCHIVOS A CREAR/MODIFICAR

### Nuevos Archivos (Crear):
```
coordinacion/templates/coordinacion/perfil.html
Estudiante/templates/estudiante/mi_docente_asesor.html
Estudiante/templates/estudiante/chat.html
docente/templates/docente/chat.html
static/js/chat.js
static/css/chat.css
```

### Archivos Existentes (Modificar):
```
coordinacion/models.py ✅
Estudiante/estudiante_forms.py
Estudiante/estudiante_views.py
Estudiante/urls.py
Estudiante/templates/estudiante/base.html
Estudiante/templates/estudiante/perfil.html
docente/forms.py
docente/docente_views.py
docente/urls.py
docente/templates/docente/base.html
docente/templates/docente/perfil.html
coordinacion/forms.py
coordinacion/views.py
coordinacion/urls.py
coordinacion/templates/coordinacion/base.html
config/settings.py
config/urls.py
```

---

## ⚠️ CONSIDERACIONES TÉCNICAS

### 1. Rendimiento
- Implementar paginación en el chat (últimos 50 mensajes)
- Lazy loading de mensajes antiguos
- Compresión de imágenes antes de guardar

### 2. Escalabilidad
- Considerar WebSockets para chat en tiempo real (futuro)
- Por ahora: AJAX polling cada 3 segundos

### 3. UX/UI
- Loading spinners al enviar
- Animaciones smooth para nuevos mensajes
- Sonido de notificación (opcional)
- Emoji picker (opcional)

---

## 🎯 PRIORIDADES

### ALTA PRIORIDAD:
1. ✅ Modelos y migraciones
2. Fotos de perfil funcionales
3. Chat básico (texto solamente)
4. Sección "Mi Docente Asesor"

### MEDIA PRIORIDAD:
5. Adjuntar archivos en chat
6. Notificaciones de mensajes nuevos
7. Marca de "leído"

### BAJA PRIORIDAD:
8. Emojis
9. Indicador "escribiendo..."
10. Búsqueda en mensajes

---

**Fecha de planificación:** 30 de Noviembre de 2025  
**Tiempo estimado total:** 8-10 horas de desarrollo  
**Estado actual:** FASE 1 - Modelos completados ✅  
**Siguiente paso:** Ejecutar migraciones y crear formularios de perfil

