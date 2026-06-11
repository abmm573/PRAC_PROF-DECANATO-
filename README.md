# Sistema de Control de Asistencia - Facultad de Ciencias Sociales

Proyecto de gestión de asistencia para pasantes de la Facultad de Ciencias Sociales, con backend en FastAPI y frontend en Vue 3 + Vite.

## Qué incluye

- Backend en `backend/` con FastAPI, PostgreSQL y JWT.
- Frontend en `frontend/` con Vue 3, Pinia y Vite.
- Modelo de datos con usuarios, roles, carreras, asistencias y reportes.
- Autenticación de usuario con token JWT.
- Roles: `ADMINISTRADOR`, `ENCARGADO`, `PASANTE`.
- Carreras predefinidas: `Antropologia`, `Arqueologia`, `Sociologia`, `Trabajo Social`, `Comunicacion Social`.

## Requisitos

- Python 3.11+ (o Python 3.10 compatible)
- PostgreSQL
- Node.js 18+ / npm

## Configuración de la base de datos

1. Crea una base de datos PostgreSQL llamada `asistencia`.
2. Ajusta la variable `DATABASE_URL` si usas otra credencial o nombre de host.
3. Puedes usar el `.env` en la raíz o en `backend/`.

Ejemplo mínimo de `.env`:

```env
DATABASE_URL=postgresql://postgres:abmm@localhost/asistencia
SECRET_KEY=super_secreta_clave_para_jwt_cambiar_en_produccion
```

## Ejecutar el backend

Desde la carpeta `backend/`:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend quedará disponible en `http://127.0.0.1:8000`.

- Documentación Swagger: `http://127.0.0.1:8000/docs`
- CORS permite el frontend en `http://localhost:5173` (y puertos 5174/5175).

## Ejecutar el frontend

Desde la carpeta `frontend/`:

```bash
npm install
npm run dev
```

Luego abre el navegador en `http://localhost:5173`.

## Datos de acceso iniciales

Al arrancar el backend, el sistema crea automáticamente un administrador inicial si no existe uno:

- Email: `admin@facultad.edu.bo`
- Username: `as00000000`
- Password: `Admin1234`

> El formulario de login usa el campo `username` en la petición, pero puedes ingresar el email del administrador en ese campo.

## Información importante

- Las carreras definidas en el sistema son:
  - `Antropologia`
  - `Arqueologia`
  - `Sociologia`
  - `Trabajo Social`
  - `Comunicacion Social`
- El login inicial está pensado para el administrador. Desde el panel de administración se pueden crear encargados y pasantes.
- Cambia la contraseña `Admin1234` en producción.

## Uso del script `asistencia.sql`

El archivo `asistencia.sql` contiene un esquema de ejemplo y las inserciones iniciales de roles y carreras.

Para cargarlo directamente en PostgreSQL:

```bash
psql -d asistencia -f asistencia.sql
```

Asegúrate de que la base de datos exista antes de ejecutar el script.
