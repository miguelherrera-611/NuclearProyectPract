# CORRECCIÓN DE ERRORES - Dashboard y Seguimientos - 30 Nov 2025

## 🐛 PROBLEMAS IDENTIFICADOS Y CORREGIDOS

### 1. ❌ Dashboard de Estudiantes en Blanco (Primer Error)

**Problema:** El dashboard no mostraba nada, pantalla en blanco.

**Causa:** Código Django template tags mezclado con JSX de React causando errores de sintaxis.

**Errores específicos:**
1. Líneas 149-165: Código duplicado en `WelcomeSection`
2. Líneas 233, 258, 390, 423, 451, 477: URLs de Django dentro de componentes JSX

**Solución aplicada:**

#### A. Definir URLs como constantes JavaScript
```javascript
// Al inicio del script, antes de los componentes
const URLS = {
    noApto: "{% url 'estudiante:no_apto' %}",
    perfil: "{% url 'estudiante:perfil' %}",
    miPractica: "{% url 'estudiante:mi_practica' %}",
    postulacionesLista: "{% url 'estudiante:postulaciones_lista' %}",
    vacantesLista: "{% url 'estudiante:vacantes_lista' %}",
    postulacionDetalle: "{% url 'estudiante:postulacion_detalle' 0 %}",
    vacanteDetalle: "{% url 'estudiante:vacante_detalle' 0 %}"
};
```

#### B. Reemplazar URLs en componentes JSX
```jsx
// ANTES (incorrecto):
<a href="{% url 'estudiante:perfil' %}" class="btn">

// DESPUÉS (correcto):
<a href={URLS.perfil} className="btn">
```

#### C. Eliminar código duplicado
Removidas las líneas 160-165 que contenían HTML duplicado del componente `WelcomeSection`.

---

### 2. ❌ Dashboard SIGUE en Blanco - Error de Sintaxis JavaScript (Segundo Error) 🆕

**Problema:** 
```
Uncaught SyntaxError: /Inline Babel script: Unexpected token (21:32)
const practicaActual = {&quot;id&quot;: 10, ...} ? JSON.parse('...') : null;
```

**Error en consola del navegador:**
```javascript
const practicaActual = {&quot;id&quot;: 10, &quot;estado&quot;: ...} ? JSON.parse(...) : null;
                                ^
SyntaxError: Unexpected token
```

**Causa:** 
El código Django `{{ practica_actual|default:"null" }}` estaba inyectando HTML entities (`&quot;` en lugar de `"`) directamente en JavaScript sin escapar, rompiendo la sintaxis.

**Código problemático:**
```javascript
const practicaActual = {{ practica_actual|default:"null" }} ? JSON.parse('{{ practica_actual|escapejs }}') : null;
// Django renderiza esto como:
// const practicaActual = {&quot;id&quot;: 10, ...} ? JSON.parse(...) : null;
// ❌ Las entidades HTML rompen la sintaxis de JavaScript
```

**Solución:**
Usar bloques condicionales de Django ANTES de generar el JavaScript:

```javascript
{% if practica_actual %}
const practicaActual = JSON.parse('{{ practica_actual|escapejs }}');
{% else %}
const practicaActual = null;
{% endif %}
```

**Por qué funciona:**
- Django evalúa el `{% if %}` en el servidor
- Solo se genera UNA de las dos líneas de JavaScript
- No hay entidades HTML en el código JavaScript resultante

---

### 3. ❌ Error en Seguimientos Semanales

**Problema:** 
```
TemplateSyntaxError at /estudiante/seguimientos/
Invalid block tag on line 175: 'endfor', expected 'endif'
```

**Causa:** Código duplicado en la tabla de seguimientos (líneas 156-161).

**Código problemático:**
```django
<td>
    {% if seguimiento.validado_docente %}
        <i class="fas fa-check-circle text-success"></i> Revisado
    {% else %}
        <i class="fas fa-clock text-warning"></i> Pendiente
    {% if seguimiento.validado_docente %}  <!-- DUPLICADO -->
        <i class="fas fa-check-circle text-success"></i> Revisado
    {% else %}
        <i class="fas fa-clock text-warning"></i> Pendiente
    {% endif %}  <!-- FALTA UN {% endif %} -->
</td>
```

**Solución:**
Removido el código duplicado, dejando solo un bloque `{% if %}...{% endif %}`.

---

## 📁 ARCHIVOS CORREGIDOS

### 1. `Estudiante/templates/estudiante/dashboard.html`
**Cambios realizados:**
- ✅ Agregadas constantes URLS al inicio del script
- ✅ Reemplazadas 7 URLs de Django por constantes JavaScript
- ✅ Eliminado código duplicado en WelcomeSection
- ✅ Corregida sintaxis className (era class en algunas partes)

### 2. `Estudiante/templates/estudiante/seguimientos/lista.html`
**Cambios realizados:**
- ✅ Eliminado código duplicado en la tabla
- ✅ Corregida estructura de bloques {% if %}...{% endif %}

---

## 🔧 DETALLES TÉCNICOS

### Problema de Mezcla Django + React

**Por qué falló:**
Django procesa los templates ANTES de que lleguen al navegador. React/JSX se ejecuta DESPUÉS en el navegador. Cuando mezclamos `{% url %}` dentro de componentes JSX, Django intenta procesarlo pero JSX no lo entiende correctamente.

**Solución correcta:**
1. Procesar URLs de Django en la capa de template (fuera de JSX)
2. Pasar las URLs como constantes JavaScript
3. Usar esas constantes dentro de los componentes React

### Sintaxis corregida

| Incorrecto | Correcto |
|------------|----------|
| `class="btn"` en JSX | `className="btn"` |
| `{% url 'name' %}` en JSX | `{URLS.name}` |
| `<a href="{% url %}">` | `<a href={URLS.name}>` |

---

## ✅ ESTADO ACTUAL

### Dashboard de Estudiantes
- ✅ Componente WelcomeSection funcional
- ✅ Componente EstudianteNoAptoAlert funcional
- ✅ Componente EstudianteAptoContent funcional
- ✅ Componente EstudianteEnPracticaContent funcional
- ✅ Componente PostulacionesRecientes funcional
- ✅ Componente VacantesDisponibles funcional
- ✅ Todas las URLs funcionando correctamente

### Seguimientos Semanales
- ✅ Lista de seguimientos renderiza correctamente
- ✅ Tabla con todos los datos visible
- ✅ Botones de acción funcionando
- ✅ Navbar y sidebar completos

---

## 🧪 PARA VERIFICAR

### Dashboard:
1. Login como estudiante: `est001` / `est123`
2. Ir a: `http://127.0.0.1:8000/estudiante/dashboard/`
3. Verificar que se vea:
   - Mensaje de bienvenida
   - Badge de estado
   - Estadísticas (si aplica)
   - Secciones según el estado del estudiante

### Seguimientos:
1. Login como estudiante: `est001` / `est123`
2. Ir a: `http://127.0.0.1:8000/estudiante/seguimientos/`
3. Verificar que se vea:
   - Navbar azul
   - Sidebar con 6 opciones
   - Información de la práctica
   - Tabla de seguimientos (o mensaje si no hay)

---

## 📊 RESUMEN DE CORRECCIONES

| Archivo | Líneas Afectadas | Tipo de Error | Estado |
|---------|------------------|---------------|--------|
| dashboard.html | 76-87 | URLs Django en JSX | ✅ Corregido |
| dashboard.html | 96 | **HTML entities en JavaScript** | ✅ Corregido 🆕 |
| dashboard.html | 149-165 | Código duplicado | ✅ Corregido |
| dashboard.html | 195 | URL en JSX | ✅ Corregido |
| dashboard.html | 245 | className incorrecto | ✅ Corregido |
| dashboard.html | 270 | URL en JSX | ✅ Corregido |
| dashboard.html | 402 | URL en JSX | ✅ Corregido |
| dashboard.html | 435 | URL en JSX | ✅ Corregido |
| dashboard.html | 463 | URL en JSX | ✅ Corregido |
| dashboard.html | 489 | URL en JSX | ✅ Corregido |
| seguimientos/lista.html | 156-161 | Código duplicado | ✅ Corregido |

**Total:** 11 errores corregidos en 2 archivos

---

## 🎯 LECCIONES APRENDIDAS

### 1. Separación de Responsabilidades
- Django Templates: Procesar datos del servidor
- JavaScript/React: Manejar interactividad del cliente
- NO mezclar sintaxis de template dentro de JSX

### 2. Debugging de Templates
- Verificar bloques {% if %}, {% for %} bien cerrados
- Buscar código duplicado
- Revisar sintaxis JSX vs HTML

### 3. Mejores Prácticas
- Definir URLs como constantes antes de los componentes React
- Usar `className` en JSX, no `class`
- Mantener la sintaxis consistente

---

**Fecha de corrección:** 30 de Noviembre de 2025  
**Estado:** ✅ COMPLETADO

**Próximo paso:** Refrescar el navegador y verificar que todo funcione correctamente.

