# FUNCIONALIDAD DESVINCULAR POSTULACIONES - 30 Nov 2025

## 🎯 NUEVA FUNCIONALIDAD IMPLEMENTADA

Se ha agregado la capacidad de **desvincular postulaciones** que están en estado "VINCULADO" desde el módulo de coordinación.

---

## ✨ CARACTERÍSTICAS

### ¿Qué hace esta funcionalidad?

Permite al coordinador **revertir** una vinculación de estudiante, cambiando el estado de la postulación de "VINCULADO" de vuelta a "SELECCIONADO".

### Acciones que realiza:

1. ✅ **Cambia el estado** de la postulación de "VINCULADO" → "SELECCIONADO"
2. ✅ **Cancela la práctica asociada** (si existe) con estado "EN_CURSO"
3. ✅ **Actualiza el estado del estudiante** a "APTO" (si no tiene otras prácticas activas)
4. ✅ **Libera un cupo** en la vacante
5. ✅ **Registra el motivo** de la desvinculación en el historial

---

## 📁 ARCHIVOS MODIFICADOS/CREADOS

### 1. **coordinacion/urls.py**
```python
path('postulaciones/<int:postulacion_id>/desvincular/', 
     views.postulacion_desvincular, 
     name='postulacion_desvincular'),
```

### 2. **coordinacion/views.py**
Nueva función: `postulacion_desvincular(request, postulacion_id)`

**Lógica implementada:**
- Verifica que la postulación esté en estado "VINCULADO"
- Busca si existe una práctica empresarial asociada en curso
- Si existe práctica: la cancela y registra el motivo
- Cambia el estado de la postulación a "SELECCIONADO"
- Actualiza el estado del estudiante si es necesario
- Libera el cupo de la vacante

### 3. **coordinacion/templates/coordinacion/postulaciones/desvincular.html** ✨ NUEVO
Template completo con:
- Alerta de advertencia destacada
- Información de la postulación
- Alerta especial si hay práctica asociada
- Formulario para ingresar motivo de desvinculación
- Checkbox de confirmación (habilita el botón)
- Confirmación adicional con JavaScript
- Diseño responsivo con Bootstrap

### 4. **coordinacion/templates/coordinacion/postulaciones/lista.html**
Agregado botón para postulaciones vinculadas:
```jsx
{postulacion.estado === 'VINCULADO' && (
    <a href={'/coordinacion/postulaciones/' + postulacion.id + '/desvincular/'}
       className="btn btn-outline-warning"
       title="Desvincular postulación">
        <i className="fas fa-unlink"></i>
    </a>
)}
```

### 5. **coordinacion/templates/coordinacion/postulaciones/detalle.html**
Agregado botón en el detalle:
```django
{% elif postulacion.estado == 'VINCULADO' %}
    <a href="{% url 'coordinacion:postulacion_desvincular' postulacion.id %}" 
       class="btn btn-warning">
        <i class="fas fa-unlink me-2"></i>Desvincular
    </a>
{% endif %}
```

---

## 🔄 FLUJO DE DESVINCULACIÓN

### Paso 1: Identificar Postulación
- Coordinación ve la lista de postulaciones
- Identifica postulaciones con estado "VINCULADO"
- Ve el botón amarillo con icono de "unlink" (🔗)

### Paso 2: Iniciar Desvinculación
- Clic en el botón "Desvincular"
- Se muestra página de confirmación con toda la información

### Paso 3: Revisión de Información
Se muestra:
- ✅ Datos del estudiante
- ✅ Datos de la vacante
- ✅ Estado actual
- ⚠️ **ADVERTENCIA si hay práctica asociada**

### Paso 4: Ingresar Motivo
- Campo obligatorio para explicar por qué se desvincuala
- Motivo queda registrado en el historial

### Paso 5: Confirmar Acción
- Checkbox de confirmación
- Botón se habilita solo después de marcar el checkbox
- Al enviar: confirmación adicional con JavaScript

### Paso 6: Proceso Automático
Si hay práctica asociada:
```python
practica.estado = 'CANCELADA'
practica.fecha_fin_real = timezone.now().date()
practica.observaciones += f"\n\nCANCELADA: {motivo}"
```

Actualizar postulación:
```python
postulacion.estado = 'SELECCIONADO'
postulacion.observaciones += f"\n\nDESVINCULADO: {motivo}"
```

Actualizar estudiante:
```python
if not tiene_otras_practicas_activas:
    estudiante.estado = 'APTO'
```

Liberar cupo:
```python
vacante.cupos_ocupados -= 1
```

---

## 🚨 VALIDACIONES Y SEGURIDAD

### Validaciones Implementadas:

1. **Estado de Postulación**
   - Solo permite desvincular si está en estado "VINCULADO"
   - Muestra mensaje de error si está en otro estado

2. **Motivo Obligatorio**
   - No permite continuar sin ingresar un motivo
   - El motivo debe ser descriptivo

3. **Confirmación Doble**
   - Checkbox en el formulario
   - Confirmación JavaScript antes de enviar

4. **Práctica Asociada**
   - Detecta automáticamente si existe
   - Muestra advertencia clara y destacada
   - Cancela la práctica al desvincular

5. **Registro de Auditoría**
   - Todo queda registrado en el campo `observaciones`
   - Se mantiene el historial completo

---

## 🎨 DISEÑO DE INTERFAZ

### Colores Utilizados:
- **Amarillo (Warning)**: Botón de desvincular
- **Naranja (Warning)**: Alertas de advertencia
- **Rojo (Danger)**: Información de práctica que será cancelada
- **Azul (Primary)**: Información general
- **Gris (Secondary)**: Botón de volver

### Iconos FontAwesome:
- `fa-unlink`: Icono principal de desvincular
- `fa-exclamation-triangle`: Advertencias
- `fa-info-circle`: Información
- `fa-comment`: Motivo

---

## 📍 RUTAS Y URLs

### URL de Desvinculación:
```
/coordinacion/postulaciones/<postulacion_id>/desvincular/
```

### Ejemplo:
```
http://127.0.0.1:8000/coordinacion/postulaciones/15/desvincular/
```

---

## 🧪 CASOS DE USO

### Caso 1: Desvincular sin Práctica Activa
**Situación:** Postulación vinculada pero aún no se ha creado la práctica

**Proceso:**
1. Coordinación detecta un error en la vinculación
2. Hace clic en "Desvincular"
3. Ingresa motivo: "Error en la asignación, estudiante equivocado"
4. Confirma
5. ✅ Postulación vuelve a "SELECCIONADO"
6. ✅ Estudiante vuelve a "APTO"
7. ✅ Cupo liberado en la vacante

### Caso 2: Desvincular con Práctica Activa
**Situación:** Postulación vinculada Y práctica empresarial en curso

**Proceso:**
1. Coordinación identifica un problema grave
2. Hace clic en "Desvincular"
3. ⚠️ Ve advertencia roja: "Se cancelará la práctica activa"
4. Ingresa motivo: "Estudiante abandonó la práctica por motivos personales"
5. Confirma (doble confirmación)
6. ✅ Práctica cambia a "CANCELADA"
7. ✅ Postulación vuelve a "SELECCIONADO"
8. ✅ Estudiante vuelve a "APTO"
9. ✅ Cupo liberado
10. ✅ Todo registrado en observaciones

### Caso 3: Intentar Desvincular Estado Incorrecto
**Situación:** Intenta desvincular una postulación en estado "SELECCIONADO"

**Resultado:**
```
⚠️ Esta postulación está en estado "Seleccionado". 
Solo se pueden desvincular postulaciones vinculadas.
```
Redirige a la lista de postulaciones.

---

## 💾 IMPACTO EN BASE DE DATOS

### Tablas Afectadas:

1. **coordinacion_postulacion**
   - `estado`: "VINCULADO" → "SELECCIONADO"
   - `observaciones`: Se agrega registro del motivo

2. **coordinacion_practicaempresarial** (si existe)
   - `estado`: "EN_CURSO" → "CANCELADA"
   - `fecha_fin_real`: Fecha actual
   - `observaciones`: Se agrega motivo de cancelación

3. **coordinacion_estudiante**
   - `estado`: "EN_PRACTICA" → "APTO" (si no tiene otras prácticas)

4. **coordinacion_vacante**
   - `cupos_ocupados`: Se decrementa en 1

---

## 🔐 PERMISOS Y ACCESO

**Requerido:** Rol de Coordinador
- Decorador: `@coordinator_required`
- Solo usuarios con perfil de coordinador pueden acceder

---

## 📝 MENSAJES AL USUARIO

### Éxito:
```
✅ Postulación desvinculada exitosamente: [Nombre del Estudiante]
```

### Advertencia (Estado Incorrecto):
```
⚠️ Esta postulación está en estado "[Estado]". 
Solo se pueden desvincular postulaciones vinculadas.
```

### Error (Sin Motivo):
```
❌ Debes proporcionar un motivo para desvincular
```

---

## 🚀 PARA PROBAR

1. **Login como coordinador:**
   ```
   Usuario: coord001
   Contraseña: coord123
   ```

2. **Crear datos de prueba:**
   - Crear una postulación
   - Vincularla (cambiar estado a "VINCULADO")
   - Opcionalmente: crear una práctica asociada

3. **Probar desvinculación:**
   - Ir a `/coordinacion/postulaciones/`
   - Buscar postulación vinculada
   - Clic en botón amarillo de desvincular
   - Seguir el proceso

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] URL agregada en `urls.py`
- [x] Vista `postulacion_desvincular` creada
- [x] Template `desvincular.html` creado
- [x] Botón agregado en lista de postulaciones
- [x] Botón agregado en detalle de postulación
- [x] Validaciones implementadas
- [x] Manejo de práctica asociada
- [x] Actualización de estado de estudiante
- [x] Liberación de cupo en vacante
- [x] Registro en observaciones
- [x] Confirmación doble (checkbox + JavaScript)
- [x] Mensajes informativos
- [x] Diseño responsive

---

**Fecha de implementación:** 30 de Noviembre de 2025  
**Estado:** ✅ COMPLETADO Y FUNCIONAL

