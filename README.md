# AppAcademico

Sistema de gestión académica universitaria compuesto por una **API REST en Laravel** y una **aplicación móvil en React Native / Expo**. Permite administrar facultades, carreras, materias, docentes, estudiantes, períodos académicos, horarios, actividades y notificaciones, con acceso segmentado por roles.

---

## Tabla de contenidos

- [Arquitectura general](#arquitectura-general)
- [Tecnologías](#tecnologías)
- [Roles y permisos](#roles-y-permisos)
- [Modelos de datos](#modelos-de-datos)
- [API – Endpoints](#api--endpoints)
- [Autenticación](#autenticación)
- [Configuración del entorno](#configuración-del-entorno)
- [Instalación y puesta en marcha](#instalación-y-puesta-en-marcha)
  - [Backend](#backend-laravel)
  - [Frontend](#frontend-react-native--expo)
  - [Docker](#docker)
- [Deploy en Railway](#deploy-en-railway)
- [Comandos útiles](#comandos-útiles)
- [Colección Postman](#colección-postman)
- [Estructura del repositorio](#estructura-del-repositorio)

---

## Arquitectura general

```
app-main/
├── appAcademico/        ← Backend: API REST (Laravel 12 + PostgreSQL)
├── appAcademicoFront/   ← Frontend: App móvil (React Native 0.83 + Expo SDK 55)
├── Dockerfile           ← Imagen Docker del backend
└── railway.toml         ← Configuración de deploy en Railway
```

El frontend se comunica con el backend mediante HTTP/JSON. El token de autenticación se almacena en `AsyncStorage` (móvil) o `localStorage` (web).

**URL de producción:** `https://worthy-charisma-production-4572.up.railway.app`

---

## Tecnologías

### Backend

| Tecnología | Versión |
|---|---|
| PHP | ^8.2 |
| Laravel Framework | ^12.0 |
| Laravel Sanctum | ^4.3 |
| PostgreSQL | cualquier versión moderna |
| smalot/pdfparser | ^2.12 (verificación de matrícula vía PDF) |

### Frontend

| Tecnología | Versión |
|---|---|
| React Native | 0.83.6 |
| React | 19.2.0 |
| Expo SDK | ~55.0.26 |
| TypeScript | ~5.9.2 |
| React Navigation | ^7.x |
| Axios | ^1.15.2 |
| AsyncStorage | 2.2.0 |

---

## Roles y permisos

El sistema maneja **6 roles** con accesos diferenciados:

| Rol | Descripción | Alcance |
|---|---|---|
| `decano` | Administrador global de la institución | Facultades, carreras, materias, usuarios, períodos |
| `director` | Director de carrera | Horarios, inscripciones, ofertas de período dentro de su carrera |
| `docente` | Profesor asignado a materias | Visualiza sus materias, estudiantes y actividades |
| `estudiante` | Alumno matriculado | Inscripciones, horarios, actividades, notificaciones |
| `centro_estudiantes` | Centro de estudiantes de una carrera | Actividades, notificaciones, consultas de docentes y estudiantes |
| `centro_facultativo` | Centro facultativo de una facultad | Mismas capacidades que centro de estudiantes pero con alcance de facultad |

Un usuario puede tener **múltiples roles**. Al iniciar sesión con más de uno, se le solicita que elija el rol activo para esa sesión.

---

## Modelos de datos

### Diagrama de relaciones

```
Facultad (1) ──────── (N) Carrera
Carrera (1) ─────────── (N) Materia
Materia (1) ─────────── (N) MateriaPeriodo
Periodo (1) ─────────── (N) MateriaPeriodo
MateriaPeriodo (1) ────── (N) Horario
MateriaPeriodo (N) ──── (1) Usuario [docente]

Usuario (N) ── roles_usuario ── (M) roles
Usuario (N) ── EstudianteMateria ── (M) MateriaPeriodo
Actividad → creado_por → Usuario
Actividad → (opcional) Materia / Carrera
Notificacion → enviado_por → Usuario
NotificacionLeida → Notificacion + Usuario
ActividadCompletada → Actividad + Usuario
```

### Tablas principales

| Tabla | Campos destacados |
|---|---|
| `usuarios` | `nombre`, `email`, `registro_universitario`, `password`, `matricula_pdf`, `esta_verificado`, `carrera_id`, `facultad_id` |
| `roles_usuario` | `usuario_id`, `rol` (enum), `carrera_id`, `facultad_id` |
| `facultades` | `nombre` |
| `carreras` | `nombre`, `facultad_id`, `tipo` (anual/semestral), `secciones` |
| `materias` | `nombre`, `carrera_id`, `seccion` |
| `periodos` | `nombre`, `tipo` (semestre/temporada), `fecha_inicio`, `fecha_fin`, `activo` |
| `materia_periodo` | `periodo_id`, `materia_id`, `docente_id`, `paralelo`, `estado` (activa/cancelada/finalizada) |
| `horarios` | `materia_id`, `materia_periodo_id`, `dia`, `hora_inicio`, `hora_fin`, `aula` |
| `actividades` | `titulo`, `descripcion`, `categoria` (parcial/tarea/proyecto/evento/comunicado), `fecha_entrega`, `ruta_archivo`, `creado_por`, `materia_id`, `carrera_id`, `rol_destino` |
| `notificaciones` | `titulo`, `cuerpo`, `ruta_archivo`, `enviado_por`, `rol_destino`, `rol_destino_array` (JSON), `carrera_ids` (JSON), `carrera_id`, `facultad_id`, `actividad_id` |

Las tablas `usuarios`, `facultades`, `carreras`, `materias`, `materia_periodo`, `actividades` y `notificaciones` usan **soft deletes**.

---

## API – Endpoints

**Base URL:** `/api`

### Autenticación

| Método | Ruta | Descripción | Auth |
|---|---|---|---|
| `POST` | `/auth/login` | Inicia sesión. Devuelve token + roles. | ❌ |
| `POST` | `/auth/registro` | Registro de estudiante (con PDF de matrícula) | ❌ |
| `POST` | `/auth/seleccionar-rol` | Elige rol activo cuando hay múltiples | Token temporal |
| `POST` | `/auth/forgot-password` | Genera código de recuperación de 6 dígitos | ❌ |
| `POST` | `/auth/reset-password` | Restablece contraseña con código | ❌ |
| `POST` | `/auth/logout` | Cierra sesión e invalida el token | 🔒 |
| `GET` | `/auth/me` | Retorna usuario y rol activo | 🔒 |

### Públicas

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/publico/carreras` | Lista de carreras (para formulario de registro) |

### Solo Decano 🔒

| Ruta | Descripción |
|---|---|
| `CRUD /facultades` | Gestión de facultades |
| `CRUD /carreras` | Gestión de carreras |
| `CRUD /materias` | Gestión de materias |
| `CRUD /usuarios` | Gestión de usuarios |
| `CRUD /periodos` (sin index/show) | Creación, edición y eliminación de períodos |
| `PUT /periodos/{id}/activar` | Activa un período académico |
| `CRUD /materia-periodo` | Gestión de ofertas de materia por período |
| `PUT /materia-periodo/{id}/asignar-docente` | Asigna docente a una oferta |
| `GET /materia-periodo/periodo-activo` | Ofertas del período activo |
| `GET /materia-periodo/docente/{docenteId}` | Ofertas de un docente específico |
| `POST /usuarios/{usuario}/asignar-director` | Asigna director a una carrera |
| `GET /dashboard/stats` | Estadísticas globales del dashboard |

### Solo Director 🔒

| Ruta | Descripción |
|---|---|
| `GET/POST /director/horarios/oferta/{id}` | Horarios de una oferta |
| `PUT/DELETE /director/horarios/{id}` | Editar / eliminar horario |
| `GET/POST/DELETE /director/inscripciones` | Gestión de inscripciones |
| `GET /director/estudiantes-disponibles` | Estudiantes sin inscribir |
| `CRUD /director/materia-periodo` | Ofertas de período de su carrera |

### Solo Docente 🔒

| Ruta | Descripción |
|---|---|
| `GET /docente/materias` | Materias asignadas |
| `GET /docente/materias/{id}/estudiantes` | Estudiantes de una materia |
| `GET /docente/materias/{id}/actividades` | Actividades de una materia |
| `GET /docente/actividades` | Todas sus actividades |
| `GET /docente/historial` | Historial académico del docente |

### Todos los usuarios autenticados 🔒

| Ruta | Descripción |
|---|---|
| `GET /periodos`, `/periodos/activo`, `/periodos/{id}` | Consulta de períodos |
| `GET/POST /actividades`, `GET /actividades/{id}` | Actividades |
| `GET /notificaciones`, `/recibidas`, `/enviadas` | Notificaciones |
| `POST /notificaciones/{id}/leer` | Marcar notificación como leída |
| `GET /estudiante/materias-carrera` | Materias disponibles para inscribirse |
| `POST /estudiante/inscribirse` | Inscribirse a una materia |
| `POST /estudiante/desinscribirse` | Desinscribirse de una materia |
| `POST/DELETE /estudiante/actividades/{id}/completar` | Marcar/desmarcar actividad completada |
| `GET /estudiante/historial` | Historial académico del estudiante |
| `POST /usuarios/cambiar-password` | Cambiar contraseña propia |
| `GET /dashboard/director-stats` | Estadísticas del director |
| `GET /dashboard/centro-estudiantes-stats` | Estadísticas del centro de estudiantes |
| `GET /dashboard/centro-facultativo-stats` | Estadísticas del centro facultativo |

---

## Autenticación

El sistema usa **Laravel Sanctum** con tokens Bearer.

### Flujo de login

```
POST /auth/login
  └─ Un solo rol    → token con esa habilidad → acceso directo
  └─ Múltiples roles → token temporal (sin habilidades) + requiere_seleccion_rol: true
        └─ POST /auth/seleccionar-rol → token definitivo con rol elegido
```

El middleware personalizado `VerificarRol` comprueba que el token tenga la habilidad (`tokenCan`) del rol requerido por cada ruta.

### Verificación de estudiantes

Al registrarse, el estudiante sube su **PDF de matrícula oficial**. El backend usa `smalot/pdfparser` para extraer el texto y buscar su número de Registro Universitario (RU) mediante regex. Si se encuentra, `esta_verificado = true` y puede iniciar sesión de inmediato. Si no, su cuenta queda pendiente de verificación manual por parte del director.

---

## Configuración del entorno

### Backend (`.env`)

Copia `.env.example` a `.env` y ajusta los valores:

```dotenv
APP_NAME=AppAcademico
APP_ENV=local
APP_KEY=                        # Se genera con: php artisan key:generate
APP_DEBUG=true
APP_URL=http://localhost

# Base de datos PostgreSQL
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=appAcademico
DB_USERNAME=postgres
DB_PASSWORD=tu_password

SESSION_DRIVER=database
QUEUE_CONNECTION=database
CACHE_STORE=database

# Correo (en local usa el driver "log", revisa storage/logs/laravel.log)
MAIL_MAILER=log
```

### Frontend

El archivo `appAcademicoFront/src/api/axios.js` contiene la `baseURL`. Para desarrollo local, modifica la línea:

```js
// Producción (Railway)
const baseURL = 'https://worthy-charisma-production-4572.up.railway.app/api';

// Desarrollo local – emulador Android
const baseURL = 'http://10.0.2.2:8000/api';

// Desarrollo local – web / iOS simulador
const baseURL = 'http://localhost:8000/api';
```

---

## Instalación y puesta en marcha

### Backend (Laravel)

```bash
# 1. Entrar al directorio del backend
cd appAcademico

# 2. Instalar dependencias PHP
composer install

# 3. Copiar el archivo de entorno
cp .env.example .env

# 4. Editar .env con tus credenciales de PostgreSQL

# 5. Generar la clave de aplicación
php artisan key:generate

# 6. Ejecutar las migraciones
php artisan migrate

# 7. Iniciar el servidor de desarrollo
php artisan serve
# La API quedará disponible en http://localhost:8000/api
```

> **Atajo:** El script `composer run setup` ejecuta automáticamente los pasos 2, 5 (si no existe .env), key:generate y migrate.

### Frontend (React Native / Expo)

```bash
# 1. Entrar al directorio del frontend
cd appAcademicoFront

# 2. Instalar dependencias
npm install

# 3. Iniciar Expo
npx expo start

# Opciones específicas por plataforma:
npx expo run:android    # Android (requiere Android Studio / dispositivo físico)
npx expo run:ios        # iOS (requiere macOS + Xcode)
npx expo start --web    # Navegador web
```

Escanea el QR desde la app **Expo Go** en tu dispositivo para probar en físico.

### Docker

El `Dockerfile` incluido construye solo el backend.

```bash
# Desde la raíz del repositorio
docker build -t app-academico .

# Ejecutar contenedor apuntando a tu instancia PostgreSQL
docker run -p 8000:8000 \
  -e DB_HOST=host.docker.internal \
  -e DB_DATABASE=appAcademico \
  -e DB_USERNAME=postgres \
  -e DB_PASSWORD=tu_password \
  app-academico
```

---

## Deploy en Railway

El repositorio incluye `railway.toml` configurado con **Nixpacks** para el backend Laravel. El `Procfile` ejecuta las migraciones y levanta el servidor al desplegar:

```
php artisan migrate --force && php artisan serve --host=0.0.0.0 --port=$PORT
```

Para el frontend, la app Expo puede publicarse como una aplicación nativa (Play Store / App Store) o como PWA usando `npx expo export --platform web`.

---

## Comandos útiles

### Artisan (backend)

```bash
# Migraciones
php artisan migrate                        # Ejecutar migraciones pendientes
php artisan migrate:rollback               # Revertir la última migración
php artisan migrate:fresh                  # Borrar todo y re-migrar

# Rutas y caché
php artisan route:list                     # Listar todas las rutas de la API
php artisan config:clear                   # Limpiar caché de configuración
php artisan cache:clear                    # Limpiar caché de la aplicación

# Cola de trabajos
php artisan queue:listen --tries=1         # Procesar cola en desarrollo

# Herramientas de desarrollo
php artisan tinker                         # REPL interactivo con acceso a modelos

# Comando personalizado
php artisan fix:estudiante-materia-duplicates   # Corrige registros duplicados en estudiante_materia
```

### Tests (backend)

```bash
php artisan test           # Ejecutar suite de tests
composer run test          # Alias que limpia caché antes de correr
```

---

## Colección Postman

El archivo `appAcademico/AcademicoAPI.postman_collection.json` contiene una colección completa con todos los endpoints de la API listos para importar en Postman.

**Importar:**
1. Abre Postman → *Import*
2. Selecciona el archivo `AcademicoAPI.postman_collection.json`
3. Configura la variable de entorno `base_url` con `http://localhost:8000/api`

---

## Estructura del repositorio

```
app-main/
│
├── appAcademico/                        ← Backend Laravel
│   ├── app/
│   │   ├── Console/Commands/            ← Comandos Artisan personalizados
│   │   ├── Http/
│   │   │   ├── Controllers/Api/         ← Controllers de la API REST
│   │   │   └── Middleware/              ← VerificarRol (middleware de autorización)
│   │   ├── Models/                      ← Modelos Eloquent
│   │   └── Providers/
│   ├── bootstrap/
│   ├── config/                          ← Configuración Laravel (cors, auth, database…)
│   ├── database/
│   │   ├── factories/
│   │   ├── migrations/                  ← Historial completo de migraciones
│   │   └── seeders/
│   ├── routes/
│   │   └── api.php                      ← Definición de todas las rutas de la API
│   ├── .env.example                     ← Plantilla de variables de entorno
│   ├── composer.json
│   └── AcademicoAPI.postman_collection.json
│
├── appAcademicoFront/                   ← Frontend React Native / Expo
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js                 ← Cliente HTTP (baseURL + interceptors)
│   │   ├── context/
│   │   │   └── AuthContext.js           ← Estado global de autenticación
│   │   ├── navigation/
│   │   │   └── AppNavigator.js          ← Stacks de navegación por rol
│   │   ├── screens/
│   │   │   ├── auth/                    ← Login, registro, recuperar contraseña
│   │   │   ├── decano/                  ← Vistas del decano
│   │   │   ├── director/                ← Vistas del director de carrera
│   │   │   ├── docente/                 ← Vistas del docente
│   │   │   ├── estudiante/              ← Vistas del estudiante
│   │   │   ├── centroEstudiantes/       ← Vistas del centro de estudiantes
│   │   │   └── centroFacultativo/       ← Vistas del centro facultativo
│   │   └── services/                    ← Llamadas a la API por dominio
│   ├── app.json                         ← Configuración Expo
│   └── package.json
│
├── Dockerfile                           ← Imagen Docker del backend
├── railway.toml                         ← Configuración de deploy Railway
└── README.md                            ← Este archivo
```

---
## Datos de acceso iniciales

Al arrancar el backend, el sistema crea automáticamente un administrador (Decano) inicial si no existe uno:

- Email: `admin@academico.com`
- Password: `Admin1234!`

> Para el rol de estudiante, simplemente hacer el registro como nuevo.
> 
## Licencia

Este proyecto es de uso académico/institucional. Consulta con el equipo de desarrollo para permisos de uso o distribución.
