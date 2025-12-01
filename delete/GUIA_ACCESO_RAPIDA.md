# 🔐 GUÍA RÁPIDA DE ACCESO - SISTEMA DE PRÁCTICAS

## ¿Cómo funciona el Login Unificado?

El sistema tiene **UN SOLO LOGIN** en `http://127.0.0.1:8000/login/` que **detecta automáticamente** tu rol según el usuario con el que ingresas.

**No necesitas seleccionar el rol antes de entrar**, el sistema lo hace por ti.

---

## 👥 USUARIOS DE PRUEBA DISPONIBLES

### 1️⃣ COORDINADOR
```
URL: http://127.0.0.1:8000/login/
Usuario: coord1
Contraseña: coord123
```
**Después de ingresar:** Te redirige automáticamente a `/coordinacion/dashboard/`

---

### 2️⃣ ESTUDIANTE
```
URL: http://127.0.0.1:8000/login/
Usuario: EST001 (o cualquier estudiante que hayas creado)
Contraseña: (la que hayas definido al registrar)
```
**Después de ingresar:** Te redirige automáticamente a `/estudiante/dashboard/`

**Para registrar un nuevo estudiante:**
- Ve a: `http://127.0.0.1:8000/estudiante/registro/`
- Completa el formulario
- Inicia sesión con tus credenciales

---

### 3️⃣ DOCENTE ASESOR ⭐ NUEVO
```
URL: http://127.0.0.1:8000/login/
Usuario: docente1
Contraseña: docente123
```
**Después de ingresar:** Te redirige automáticamente a `/docente/dashboard/`

#### Otros docentes disponibles:
- **Usuario:** `docente2` | **Contraseña:** `docente123` (Especialidad: Ingeniería Industrial)
- **Usuario:** `docente3` | **Contraseña:** `docente123` (Especialidad: Administración)

---

## 🔄 ¿Qué pasa si un usuario tiene MÚLTIPLES ROLES?

Si un usuario tiene más de un rol (por ejemplo, es Coordinador Y Estudiante), después de hacer login verá una pantalla de **selección de rol** donde podrá elegir con cuál quiere ingresar.

---

## 📋 PASOS PARA PROBAR EL ROL DE DOCENTE ASESOR

### Paso 1: Login como Docente
1. Ve a: `http://127.0.0.1:8000/login/`
2. Ingresa:
   - **Usuario:** `docente1`
   - **Contraseña:** `docente123`
3. Click en "Iniciar Sesión"
4. ✅ Serás redirigido a `/docente/dashboard/`

### Paso 2: Asignar Estudiantes al Docente (Usando Admin)
Para que el docente pueda ver estudiantes y seguimientos, primero debes asignarle prácticas:

1. Ve a: `http://127.0.0.1:8000/admin/`
2. Inicia sesión con tu superusuario
3. Ve a **Coordinacion > Prácticas Empresariales**
4. Edita una práctica existente (o crea una nueva)
5. En el campo **"Docente asesor"**, selecciona a `Carlos Rodríguez Pérez`
6. Guarda
7. Ahora cuando entres como `docente1`, verás esa práctica en tu dashboard

### Paso 3: Crear Seguimientos como Estudiante
1. Logout del docente
2. Login como un estudiante que tenga una práctica activa (estado `EN_PRACTICA`)
3. En el sidebar, click en **"Seguimientos Semanales"**
4. Click en **"Crear Nuevo Seguimiento"**
5. Completa el formulario
6. Guarda

### Paso 4: Revisar como Docente
1. Logout del estudiante
2. Login nuevamente como `docente1`
3. En el dashboard verás los **Seguimientos Pendientes**
4. Click en **"Revisar"**
5. Podrás **Aprobar** o **Rechazar** el seguimiento
6. Deja observaciones para el estudiante

---

## 🎨 NAVEGACIÓN DEL DOCENTE ASESOR

Una vez dentro como docente, tendrás estas opciones en el sidebar:

- 🏠 **Dashboard** - Vista general con estadísticas
- 👥 **Mis Estudiantes** - Lista de estudiantes asignados (máx. 5)
- ⏰ **Seguimientos Pendientes** - Seguimientos por revisar
- 👤 **Mi Perfil** - Información y estadísticas personales
- 🚪 **Cerrar Sesión**

---

## 🎨 NAVEGACIÓN DEL ESTUDIANTE (EN PRÁCTICA)

Si estás en práctica, verás:

- 🏠 **Dashboard** - Vista general
- 👤 **Mi Perfil** - Información personal
- 💼 **Vacantes Disponibles** - Ver vacantes
- 📋 **Mis Postulaciones** - Ver postulaciones
- ✅ **Mi Práctica** - Información de la práctica actual
- 📅 **Seguimientos Semanales** ⭐ NUEVO - Gestionar evidencias semanales

---

## 🆘 TROUBLESHOOTING

### "No veo la opción de docente en el login"
✅ **Es normal.** No hay opción para seleccionar rol antes de entrar. Solo ingresa con las credenciales del docente (`docente1` / `docente123`) y el sistema te redirigirá automáticamente.

### "El docente no ve ningún estudiante"
✅ Debes **asignar prácticas** al docente desde el admin de Django. Ve a la sección "Paso 2" arriba.

### "El estudiante no puede crear seguimientos"
✅ El estudiante debe estar en estado `EN_PRACTICA` con una práctica activa asignada.

### "No puedo acceder al admin"
✅ Necesitas crear un superusuario:
```bash
python manage.py createsuperuser
```

---

## 🚀 COMANDOS ÚTILES

### Iniciar servidor
```bash
python manage.py runserver
```

### Crear más docentes
```bash
python crear_docente_asesor.py
```

### Ver todos los usuarios
En el admin: `http://127.0.0.1:8000/admin/auth/user/`

---

## 📞 RESUMEN RÁPIDO

| Rol | Usuario | Contraseña | Dashboard |
|-----|---------|------------|-----------|
| Coordinador | `coord1` | `coord123` | `/coordinacion/dashboard/` |
| Docente Asesor | `docente1` | `docente123` | `/docente/dashboard/` |
| Docente Asesor | `docente2` | `docente123` | `/docente/dashboard/` |
| Docente Asesor | `docente3` | `docente123` | `/docente/dashboard/` |
| Estudiante | (código estudiante) | (tu contraseña) | `/estudiante/dashboard/` |

**URL de Login:** `http://127.0.0.1:8000/login/`
**URL de Registro (Estudiantes):** `http://127.0.0.1:8000/estudiante/registro/`

---

✨ **El sistema detecta automáticamente tu rol al hacer login. ¡Solo ingresa tus credenciales!**

