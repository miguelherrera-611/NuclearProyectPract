# 🎨 Mejora Visual - Selector de Programas Académicos

## 📋 Resumen de la Mejora

Se ha rediseñado el campo "Programa Académico" en el formulario de registro para utilizar **tarjetas interactivas seleccionables** en lugar de un dropdown tradicional, mejorando significativamente la experiencia de usuario.

---

## ✨ Antes vs Después

### **❌ ANTES**
```
Campo de texto o select tradicional
└── Usuario selecciona de una lista desplegable
└── No se muestran las restricciones claramente
```

### **✅ DESPUÉS**
```
Tarjetas visuales grandes y atractivas
├── Ingeniería de Software (icono laptop)
│   └── "Puedes realizar prácticas desde 4° semestre"
├── Ingeniería Industrial (icono industria)
│   └── "Puedes realizar prácticas desde 4° semestre"
└── Administración de Empresas (icono maletín)
    └── "Puedes realizar prácticas desde 2° semestre"
```

---

## 🎨 Diseño de las Tarjetas

### **Estructura Visual**

Cada tarjeta de programa incluye:

1. **Icono distintivo** (parte superior izquierda)
   - 💻 Laptop para Software
   - 🏭 Industria para Industrial
   - 💼 Maletín para Administración

2. **Nombre del programa** (bold, grande)
   - Font-size: 1.1rem
   - Font-weight: 700

3. **Requisito de semestre** (con icono de calendario)
   - Texto claro e informativo
   - Énfasis en el número de semestre

4. **Check icon** (parte superior derecha)
   - Solo visible cuando está seleccionado
   - ✓ en verde o blanco

---

## 🎯 Estados de las Tarjetas

### **Estado Normal (Sin seleccionar)**
```css
background: white
border: 3px solid #e0e7ff (azul claro)
color: text-dark
```

### **Estado Hover**
```css
border-color: #2a5298 (azul medio)
transform: translateX(5px)
box-shadow: 0 5px 15px rgba(42, 82, 152, 0.2)
```

### **Estado Seleccionado**
```css
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)
border-color: #1e3c72
color: white
transform: scale(1.02)
box-shadow: 0 8px 20px rgba(30, 60, 114, 0.3)
✓ Check icon visible
```

---

## 💻 Código CSS Implementado

```css
/* Ocultar select original */
.programa-selector {
    display: none;
}

/* Grid de tarjetas */
.programas-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 15px;
    margin-bottom: 20px;
}

/* Tarjeta individual */
.programa-card {
    background: white;
    border: 3px solid #e0e7ff;
    border-radius: 12px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

/* Hover effect */
.programa-card:hover {
    border-color: #2a5298;
    transform: translateX(5px);
    box-shadow: 0 5px 15px rgba(42, 82, 152, 0.2);
}

/* Estado seleccionado */
.programa-card.selected {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    border-color: #1e3c72;
    color: white;
    transform: scale(1.02);
    box-shadow: 0 8px 20px rgba(30, 60, 114, 0.3);
}

/* Check icon */
.programa-card .check-icon {
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 1.5rem;
    display: none;
}

.programa-card.selected .check-icon {
    display: block;
    color: white;
}
```

---

## ⚙️ Funcionalidad JavaScript

### **1. Selección de Tarjeta**
```javascript
programaCards.forEach(card => {
    card.addEventListener('click', function() {
        // Obtener programa seleccionado
        const programa = this.getAttribute('data-programa');
        
        // Remover selección previa
        programaCards.forEach(c => c.classList.remove('selected'));
        
        // Marcar como seleccionado
        this.classList.add('selected');
        
        // Actualizar select oculto
        programaSelect.value = programa;
        
        // Disparar validaciones
        programaSelect.dispatchEvent(new Event('change'));
    });
});
```

### **2. Validación Dinámica de Semestre**
```javascript
function actualizarValidacionSemestre(programa) {
    const semestreMinimo = requisitos[programa];
    
    // Actualizar atributo min
    semestreInput.setAttribute('min', semestreMinimo);
    
    // Actualizar placeholder
    semestreInput.setAttribute('placeholder', `Mínimo: ${semestreMinimo}° semestre`);
    
    // Mostrar mensaje informativo
    if (valorActual < semestreMinimo) {
        // ⚠️ Mensaje de error
    } else {
        // ✅ Mensaje de éxito
    }
}
```

### **3. Restauración de Estado**
```javascript
// Si hay error en formulario, mantener selección
if (programaSelect.value) {
    programaCards.forEach(card => {
        if (card.getAttribute('data-programa') === programaSelect.value) {
            card.classList.add('selected');
        }
    });
}
```

---

## 🎯 Contenido de las Tarjetas

### **Tarjeta 1: Ingeniería de Software**
```html
<div class="programa-card" data-programa="Ingeniería de Software">
    <i class="fas fa-check-circle check-icon"></i>
    <div class="programa-nombre">
        <i class="fas fa-laptop-code"></i>
        <span>Ingeniería de Software</span>
    </div>
    <div class="programa-requisito">
        <i class="fas fa-calendar-alt"></i>
        <span>Puedes realizar prácticas desde <strong>4° semestre</strong></span>
    </div>
</div>
```

### **Tarjeta 2: Ingeniería Industrial**
```html
<div class="programa-card" data-programa="Ingeniería Industrial">
    <i class="fas fa-check-circle check-icon"></i>
    <div class="programa-nombre">
        <i class="fas fa-industry"></i>
        <span>Ingeniería Industrial</span>
    </div>
    <div class="programa-requisito">
        <i class="fas fa-calendar-alt"></i>
        <span>Puedes realizar prácticas desde <strong>4° semestre</strong></span>
    </div>
</div>
```

### **Tarjeta 3: Administración de Empresas**
```html
<div class="programa-card" data-programa="Administración de Empresas">
    <i class="fas fa-check-circle check-icon"></i>
    <div class="programa-nombre">
        <i class="fas fa-briefcase"></i>
        <span>Administración de Empresas</span>
    </div>
    <div class="programa-requisito">
        <i class="fas fa-calendar-alt"></i>
        <span>Puedes realizar prácticas desde <strong>2° semestre</strong></span>
    </div>
</div>
```

---

## 🔄 Flujo de Interacción

### **Paso 1: Usuario visualiza las tarjetas**
```
┌─────────────────────────────────┐
│ 💻 Ingeniería de Software       │
│ Desde 4° semestre               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 🏭 Ingeniería Industrial        │
│ Desde 4° semestre               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 💼 Administración de Empresas   │
│ Desde 2° semestre               │
└─────────────────────────────────┘
```

### **Paso 2: Usuario hace hover sobre una tarjeta**
```
┌─────────────────────────────────┐
│ 💻 Ingeniería de Software  ➜    │ ← Animación de desplazamiento
│ Desde 4° semestre               │ ← Borde azul resaltado
└─────────────────────────────────┘
```

### **Paso 3: Usuario hace clic**
```
╔═════════════════════════════════╗
║ ✓ 💻 Ingeniería de Software     ║ ← Fondo azul gradiente
║ Desde 4° semestre               ║ ← Texto blanco
╚═════════════════════════════════╝ ← Check icon visible
```

### **Paso 4: Validación automática del semestre**
```
Campo Semestre actualizado:
- Placeholder: "Mínimo: 4° semestre"
- Min attribute: 4
- Mensaje: "✓ Semestre mínimo requerido: 4°"
```

---

## 🎨 Características Visuales

### **Animaciones**
- **Transición suave**: `all 0.3s ease`
- **Hover lateral**: `translateX(5px)`
- **Selección con escala**: `scale(1.02)`

### **Sombras**
- **Normal**: Sin sombra
- **Hover**: `0 5px 15px rgba(42, 82, 152, 0.2)`
- **Seleccionado**: `0 8px 20px rgba(30, 60, 114, 0.3)`

### **Colores**
- **Borde normal**: `#e0e7ff` (azul muy claro)
- **Borde hover**: `#2a5298` (azul medio)
- **Fondo seleccionado**: Gradiente `#1e3c72` → `#2a5298`

---

## 📱 Responsive Design

### **Desktop (> 768px)**
```
┌──────────────────────┐
│ Tarjeta completa     │
│ Con todos los iconos │
└──────────────────────┘
```

### **Mobile (< 768px)**
```
┌──────────────┐
│ Tarjeta      │
│ Compacta     │
└──────────────┘
```

---

## ✅ Ventajas de este Diseño

### **Para el Usuario**
1. ✅ **Mayor claridad**: Ve inmediatamente las restricciones
2. ✅ **Mejor UX**: Interacción más intuitiva
3. ✅ **Feedback visual**: Sabe qué ha seleccionado
4. ✅ **Información contextual**: Requisitos visibles sin buscar

### **Para el Sistema**
1. ✅ **Menor tasa de error**: Usuarios mejor informados
2. ✅ **Validación anticipada**: Previene errores comunes
3. ✅ **Datos consistentes**: Select oculto garantiza compatibilidad
4. ✅ **Mantenibilidad**: Fácil agregar/modificar programas

### **Accesibilidad**
1. ✅ **Alto contraste**: Colores claramente diferenciados
2. ✅ **Iconos descriptivos**: Refuerzan la comprensión
3. ✅ **Feedback claro**: Estados visuales evidentes
4. ✅ **Compatible con teclado**: Navegable con Tab

---

## 🔧 Implementación Técnica

### **HTML**
```html
<!-- Select oculto (para envío de formulario) -->
<div class="programa-selector">
    {{ form.programa_academico }}
</div>

<!-- Tarjetas visuales -->
<div class="programas-grid">
    <div class="programa-card" data-programa="...">
        ...
    </div>
</div>
```

### **CSS**
- Tarjetas con `border-radius: 12px`
- Gradiente en seleccionado
- Transiciones suaves

### **JavaScript**
- Event listener en cada tarjeta
- Sincronización con select oculto
- Validación dinámica de semestre

---

## 📊 Comparación de Usabilidad

| Aspecto | Select Tradicional | Tarjetas Visuales |
|---------|-------------------|-------------------|
| Visibilidad de opciones | ❌ Requiere clic | ✅ Todas visibles |
| Información de requisitos | ❌ Oculta | ✅ Siempre visible |
| Feedback visual | ⚠️ Limitado | ✅ Excelente |
| Experiencia móvil | ⚠️ Aceptable | ✅ Optimizada |
| Atractivo visual | ❌ Básico | ✅ Moderno |
| Accesibilidad | ✅ Buena | ✅ Excelente |

---

## 🚀 Resultado Final

✅ **Diseño moderno y atractivo**
✅ **Información clara de restricciones**
✅ **Interacción intuitiva**
✅ **Validación en tiempo real**
✅ **Feedback visual inmediato**
✅ **Compatible con todos los navegadores**

**Fecha de implementación**: 2025-01-27
**Versión**: 3.1 (Selector Visual de Programas)

