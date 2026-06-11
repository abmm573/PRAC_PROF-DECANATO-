from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.usuario import Usuario
from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/usuarios/login")

# ──────────────────────────────────────────────
# Roles disponibles en el sistema:
#   ADMINISTRADOR → acceso total, CRUD completo
#   ENCARGADO     → ve solo los pasantes de su carrera
#   PASANTE       → gestiona su propia asistencia y reportes
# ──────────────────────────────────────────────


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credenciales_exception
        email = str(email).strip().lower()
    except JWTError:
        raise credenciales_exception

    usuario = db.query(Usuario).filter(func.lower(Usuario.email) == email).first()
    if usuario is None:
        raise credenciales_exception
    return usuario


def rol_requerido(roles_permitidos: list[str]):
    """
    Decorador de seguridad.
    Uso: Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
    """
    def verificador_roles(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
        nombre_rol = getattr(usuario_actual.rol, "nombre", None)
        if nombre_rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para realizar esta acción"
            )
        return usuario_actual
    return verificador_roles