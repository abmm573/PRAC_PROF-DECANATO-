from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.modelos.usuario import RolUsuario

# 1. Esquema para recibir datos desde el frontend (Registro)
class UsuarioCrear(BaseModel):
    nombre: str
    correo: EmailStr # Pydantic valida automáticamente que sea un correo real
    contrasena: str

# 2. Esquema para devolver datos al frontend (Lectura segura)
class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: RolUsuario
    fecha_creacion: datetime

    class Config:
        # Esto permite que Pydantic lea los datos directamente de SQLAlchemy
        from_attributes = True