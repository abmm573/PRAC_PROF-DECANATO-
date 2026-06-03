from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Importamos la conexión a BD y nuestros enrutadores
from app.base_datos.conexion import motor, Base
from app.rutas import rutas_archivos, rutas_autenticacion

# Importamos la conexión a BD y nuestros enrutadores
from app.base_datos.conexion import motor, Base

# ¡IMPORTANTE! Importar los modelos para que SQLAlchemy los detecte al crear las tablas
from app.modelos.usuario import Usuario
from app.modelos.revista import Revista
from app.modelos.revision import HistorialRevision
from app.modelos.resena import Resena
from app.modelos.estadistica_lectura import EstadisticaLectura

from app.rutas import rutas_archivos, rutas_autenticacion, rutas_revistas, rutas_usuarios # <-- Agregar rutas_revistas

from app.modelos import categoria # Esto hace que SQLAlchemy cree la tabla
from app.rutas import rutas_categorias

# Creamos las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=motor)

app = FastAPI(
    title="API - Biblioteca Digital de Revistas (UMSA)",
    description="Backend para la Facultad de Ciencias Sociales",
    version="1.0.0"
)

# Configurar CORS (Para permitir que el frontend Vue.js se comunique con esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambiar por la URL de tu frontend, ej: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar la carpeta local para servir las portadas y PDFs al público
app.mount("/archivos_subidos", StaticFiles(directory="archivos_subidos"), name="archivos")

# Registrar las rutas
app.include_router(rutas_autenticacion.enrutador, prefix="/api/auth", tags=["Autenticación"])
app.include_router(rutas_archivos.enrutador, prefix="/api", tags=["Gestión de Archivos"])
# Busca donde tienes tus app.include_router() y agrega este:
app.include_router(rutas_categorias.enrutador, prefix="/api/categorias", tags=["Categorías"])

@app.get("/")
def estado_servidor():
    return {"mensaje": "Servidor de Biblioteca Digital UMSA en línea 🚀"}


# Registrar las rutas
app.include_router(rutas_autenticacion.enrutador, prefix="/api/auth", tags=["Autenticación"])
app.include_router(rutas_archivos.enrutador, prefix="/api", tags=["Archivos"])
# ¡Agregamos el enrutador de revistas!
app.include_router(rutas_revistas.enrutador, prefix="/api/revistas", tags=["Revistas"])
app.include_router(rutas_usuarios.enrutador, prefix="/api/usuarios", tags=["Usuarios"])
