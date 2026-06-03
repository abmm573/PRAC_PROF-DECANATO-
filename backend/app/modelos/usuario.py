from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime, Boolean
from sqlalchemy.sql import func
from app.base_datos.conexion import Base
import enum

# Definimos los roles usando un Enum de Python
class RolUsuario(str, enum.Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    MODERADOR = "MODERADOR"
    AUTOR = "AUTOR"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, index=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(SQLEnum(RolUsuario), default=RolUsuario.AUTOR)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # --- NUEVA COLUMNA ---
    activo = Column(Boolean, default=True)