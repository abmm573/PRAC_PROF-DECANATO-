# Sistema de Revistas Digitales - Facultad de Ciencias Sociales

Plataforma web para la gestión, publicación y visualización de la producción intelectual académica de la Facultad de Ciencias Sociales. Arquitectura dividida en API REST y Single Page Application (SPA).

### Stack Tecnológico

| Componente | Tecnología Principal | Herramientas Adicionales |
| :--- | :--- | :--- |
| **Backend** | FastAPI (Python 3.11+) | SQLAlchemy (ORM), Uvicorn |
| **Frontend** | Vue 3 (Composition API) | Vite, Tailwind CSS, Pinia |
| **Base de Datos** | PostgreSQL | Archivo `revistas.sql` (Migraciones) |
| **Seguridad** | JWT (JSON Web Tokens) | Bcrypt (Hashing de contraseñas) |

### Características del Sistema

| Módulo | Descripción Concreta |
| :--- | :--- |
| **Gestión de Archivos** | Carga, almacenamiento y visualización optimizada de documentos PDF y portadas. |
| **Clasificación** | Organización por carreras: *Antropología, Arqueología, Sociología, Trabajo Social, Comunicación Social*. |
| **Buscador Académico**| Filtros por título, autor, palabras clave y año de publicación. |
| **Metadatos** | Registro indexable de resúmenes (abstracts) y detalles bibliográficos. |

### Roles y Permisos

| Rol | Nivel de Acceso | Capacidades Principales |
| :--- | :--- | :--- |
| **ADMINISTRADOR** | Control Total | Gestión de cuentas de Editores, configuración del sistema, supervisión global de todas las publicaciones. |
| **EDITOR** | Nivel Carrera | Creación de revistas, subida de PDF y registro de metadatos exclusivamente para su área o carrera asignada. |
| **PÚBLICO** | Solo Lectura | Búsqueda, visualización y descarga de revistas en la interfaz pública (no requiere inicio de sesión). |

---

### Guía de Instalación y Ejecución

#### 1. Requisitos Previos
* Python 3.11+
* Node.js 18+ y npm
* PostgreSQL instalado y en ejecución.

#### 2. Configuración de Base de Datos
1. Crea una base de datos en PostgreSQL llamada `revistas_db`.
2. Ejecuta el script inicial: `psql -d revistas_db -f revistas.sql`
3. Configura el archivo `.env` en la carpeta `backend/`:
    ```env
    DATABASE_URL=postgresql://postgres:tu_password@localhost/revistas_db
    SECRET_KEY=clave_secreta_jwt_para_produccion
    ```

#### 3. Levantar el Backend (API)
Abre una terminal en la ruta `/backend`:

    ```bash
    # 1. Crear y activar entorno virtual
    python -m venv venv
    venv\Scripts\activate      # En Windows
    # source venv/bin/activate # En Linux/Mac
    
    # 2. Instalar dependencias
    pip install -r requirements.txt
    
    # 3. Ejecutar servidor
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
> **Endpoints disponibles en:** `http://127.0.0.1:8000/docs` (Swagger UI)

#### 4. Levantar el Frontend (Cliente)
Abre una nueva terminal en la ruta `/frontend`:

    ```bash
    # 1. Instalar paquetes
    npm install
    
    # 2. Ejecutar servidor de desarrollo
    npm run dev
    ```
> **Aplicación disponible en:** `http://localhost:5173`

---

### Credenciales Iniciales (Administrador)

El sistema genera una cuenta maestra por defecto al inicializar la base de datos:

* **Username:** `admin_revistas`
* **Email:** `admin@facultad.edu.bo`
* **Password:** `Admin1234`

*(Cambiar estas credenciales inmediatamente tras el primer despliegue en producción).*
