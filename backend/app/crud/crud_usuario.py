from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.usuario import Usuario
from app.models.carrera import Rol
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from app.core.security import obtener_password_hash
import unicodedata


# ──────────────────────────────────────────────
# Utilidad: generar username único
# Formato: (1ra inicial nombre) + (1ra inicial apellido) + CI
# Ej: "Juan Pérez", CI "1234567" → "jp1234567"
# ──────────────────────────────────────────────
def _limpiar_letra(letra: str) -> str:
    """Normaliza una letra: quita tildes y pasa a minúscula."""
    normalizada = unicodedata.normalize("NFD", letra)
    solo_ascii = "".join(c for c in normalizada if unicodedata.category(c) != "Mn")
    return solo_ascii.lower()


def generar_username(nombres: str, apellidos: str, carnet_identidad: str) -> str:
    """
    Genera el username con la primera inicial del nombre,
    primera inicial del apellido y el número de carnet.
    """
    inicial_nombre = _limpiar_letra(nombres.strip()[0]) if nombres.strip() else "x"
    inicial_apellido = _limpiar_letra(apellidos.strip()[0]) if apellidos.strip() else "x"
    ci_limpio = carnet_identidad.strip().replace("-", "").replace(" ", "")
    return f"{inicial_nombre}{inicial_apellido}{ci_limpio}"


def obtener_usuario_por_email(db: Session, email: str):
    email_norm = (email or "").strip().lower()
    if not email_norm:
        return None
    return db.query(Usuario).filter(func.lower(Usuario.email) == email_norm).first()


def obtener_usuario_por_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()


def crear_usuario(db: Session, usuario: UsuarioCreate):
    password_encriptada = obtener_password_hash(usuario.password)

    # ✅ Generamos el username automáticamente
    username = generar_username(usuario.nombres, usuario.apellidos, usuario.carnet_identidad)

    db_usuario = Usuario(
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        carnet_identidad=usuario.carnet_identidad,
        ru=usuario.ru,
        unidad_asignada=usuario.unidad_asignada,
        username=username,
        email=str(usuario.email).strip().lower(),
        celular=usuario.celular,
        proyecto_nombre=(usuario.proyecto_nombre.strip() if usuario.proyecto_nombre else None),
        meta_horas_pasantia=(usuario.meta_horas_pasantia if usuario.meta_horas_pasantia is not None else 240),
        programa_id=(usuario.programa_id if getattr(usuario, "programa_id", None) is not None else None),
        password_hash=password_encriptada,
        rol_id=usuario.rol_id,
        carrera_id=usuario.carrera_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100, carrera_id: int = None):
    query = db.query(Usuario)
    if carrera_id:
        # ENCARGADO: solo ve los PASANTES de su carrera
        from app.models.carrera import Rol as RolModel
        query = (
            query
            .join(RolModel, Usuario.rol_id == RolModel.id)
            .filter(RolModel.nombre == "PASANTE", Usuario.carrera_id == carrera_id)
        )
    return query.offset(skip).limit(limit).all()


def desactivar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.estado = False
        db.commit()
    return usuario


def actualizar_usuario(db: Session, usuario_id: int, datos_actualizar: UsuarioUpdate):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        return None

    update_data = datos_actualizar.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "email" and value is not None:
            value = str(value).strip().lower()
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario
