import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# Cargar variables desde .env si existe (desarrollo)
from pathlib import Path


def _load_simple_env(env_path: Path) -> None:
    """Carga KEY=VALUE sin depender de python-dotenv."""
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().lstrip("\ufeff")
        os.environ[key] = value.strip().strip('"').strip("'")


try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

here = Path(__file__).resolve()
repo_root = here.parents[2]
backend_dir = here.parents[1]

if load_dotenv is not None:
    load_dotenv(dotenv_path=repo_root / '.env', override=True)
    load_dotenv(dotenv_path=backend_dir / '.env', override=True)

# Fallback y refuerzo: siempre intentar carga manual.
_load_simple_env(repo_root / '.env')
_load_simple_env(backend_dir / '.env')



from app.api.v1 import rutas_usuarios, rutas_asistencias, rutas_reportes, rutas_carreras, rutas_programas, rutas_notificaciones
from app.db.database import engine, Base, SessionLocal
from app.db.bootstrap import ensure_schema
from app.models.usuario import Usuario
from app.models.carrera import Rol
from app.models.programa_pasantia import ProgramaPasantia  # noqa: F401
from app.models.notificacion_pasantia import NotificacionPasantia  # noqa: F401
from app.models.reporte_historial import ReporteEstadoHistorial  # noqa: F401
from app.models.password_reset_token import PasswordResetToken  # noqa: F401
from app.core.security import obtener_password_hash

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Control de Asistencia - Facultad de Ciencias Sociales",
    description="API con FastAPI, PostgreSQL y JWT para la gestiÃ³n de pasantes.",
    version="2.0.0"
)

# Archivos est?ticos (logos de carreras)
static_dir = Path(__file__).resolve().parent / "static"
static_dir.joinpath("proyecto_docs").mkdir(parents=True, exist_ok=True)
static_dir.joinpath("programas_docs").mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:5174", 
        "http://127.0.0.1:5174",
        "http://localhost:5175", 
        "http://127.0.0.1:5175",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(rutas_usuarios.router,   prefix="/api/v1/usuarios",    tags=["Usuarios y AutenticaciÃ³n"])
app.include_router(rutas_asistencias.router, prefix="/api/v1/asistencias", tags=["Control de Asistencia"])
app.include_router(rutas_reportes.router,   prefix="/api/v1/reportes",    tags=["Reportes Diarios"])
app.include_router(rutas_carreras.router,   prefix="/api/v1/carreras",    tags=["Carreras"])
app.include_router(rutas_programas.router,  prefix="/api/v1/programas",   tags=["Programas de Pasantia"])
app.include_router(rutas_notificaciones.router, prefix="/api/v1/notificaciones", tags=["Notificaciones AutomÃ¡ticas"])


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Al arrancar: garantizar que existan los 3 roles y un admin por defecto
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.on_event("startup")
def inicializar_datos():
    print(f"[startup] SMTP_HOST configurado: {bool(os.getenv('SMTP_HOST'))}; SMTP2_HOST configurado: {bool(os.getenv('SMTP2_HOST'))}")
    db: Session = SessionLocal()
    try:
        ensure_schema(db)
        _crear_roles_si_no_existen(db)
        _crear_admin_por_defecto(db)
    finally:
        db.close()


def _crear_roles_si_no_existen(db: Session):
    """Inserta los 3 roles del sistema si todavÃ­a no estÃ¡n en la BD."""
    roles_requeridos = ["ADMINISTRADOR", "ENCARGADO", "PASANTE"]
    for nombre in roles_requeridos:
        if not db.query(Rol).filter(Rol.nombre == nombre).first():
            db.add(Rol(nombre=nombre))
    db.commit()


def _crear_admin_por_defecto(db: Session):
    """
    Crea un ADMINISTRADOR inicial solo si no existe ninguno en la BD.
    Credenciales por defecto (Â¡cÃ¡mbialas en producciÃ³n!):
        email    : admin@facultad.edu.bo
        password : Admin1234
        username : aa00000000  (generado de 'Admin' + 'Admin' + '00000000')
    """
    rol_admin = db.query(Rol).filter(Rol.nombre == "ADMINISTRADOR").first()
    if not rol_admin:
        return  # No deberÃ­a pasar tras _crear_roles_si_no_existen

    ya_existe_admin = (
        db.query(Usuario)
        .filter(Usuario.rol_id == rol_admin.id)
        .first()
    )
    if ya_existe_admin:
        return  # Ya hay al menos un admin, no hacemos nada

    admin = Usuario(
        nombres         = "Admin",
        apellidos       = "Sistema",
        carnet_identidad= "00000000",
        username        = "as00000000",   # a(Admin) + s(Sistema) + 00000000
        email           = "admin@facultad.edu.bo",
        celular         = "00000000",
        password_hash   = obtener_password_hash("Admin1234"),
        rol_id          = rol_admin.id,
        carrera_id      = None,
        estado          = True,
    )
    db.add(admin)
    db.commit()
    print("=" * 55)
    print("  ✅… Admin por defecto creado:")
    print("     Email    : admin@facultad.edu.bo")
    print("     Password : Admin1234")
    print("     âš ï¸  Â¡CÃ¡mbiala en producciÃ³n!")
    print("=" * 55)


@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "estado": "Online",
        "mensaje": "Bienvenido al Sistema de Control de Asistencia. Visita /docs para la documentaciÃ³n."
    }





