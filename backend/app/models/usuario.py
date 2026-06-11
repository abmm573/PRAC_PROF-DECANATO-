from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

from app.models.carrera import Rol, Carrera


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    carnet_identidad = Column(String(20), unique=True, index=True, nullable=False)
    ru = Column(String(30), index=True, nullable=True)  # Registro Universitario (RU)
    unidad_asignada = Column(String(150), nullable=True)
    # ✅ NUEVO: username generado automáticamente (1ra inicial nombre + 1ra inicial apellido + CI)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    celular = Column(String(20), nullable=False, index=True)

    proyecto_nombre = Column(String(255), nullable=True)
    proyecto_documento_url = Column(String(255), nullable=True)
    meta_horas_pasantia = Column(Numeric(6, 2), nullable=False, default=240)

    programa_id = Column(Integer, ForeignKey("programas_pasantia.id"), nullable=True)

    password_hash = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    carrera_id = Column(Integer, ForeignKey("carreras.id"), nullable=True)
    estado = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    rol = relationship("Rol")
    carrera = relationship("Carrera")
    programa = relationship("ProgramaPasantia")
    asistencias = relationship("Asistencia", back_populates="pasante")
