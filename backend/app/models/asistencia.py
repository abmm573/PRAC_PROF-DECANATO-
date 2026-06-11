from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Asistencia(Base):
    __tablename__ = "asistencias"

    id = Column(Integer, primary_key=True, index=True)
    pasante_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    fecha = Column(DateTime, nullable=False)
    hora_entrada = Column(DateTime(timezone=True), nullable=False)

    # ✅ GPS opcional — puede ser None si se ficha desde la pantalla pública
    latitud_entrada  = Column(DECIMAL(10, 8), nullable=True)
    longitud_entrada = Column(DECIMAL(11, 8), nullable=True)

    hora_salida      = Column(DateTime(timezone=True), nullable=True)
    latitud_salida   = Column(DECIMAL(10, 8), nullable=True)
    longitud_salida  = Column(DECIMAL(11, 8), nullable=True)
    horas_trabajadas = Column(DECIMAL(5, 2), nullable=True)

    pasante = relationship("Usuario", back_populates="asistencias")
    reporte = relationship("Reporte", back_populates="asistencia", uselist=False)


class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    asistencia_id        = Column(Integer, ForeignKey("asistencias.id", ondelete="CASCADE"), unique=True)
    actividades_realizadas = Column(Text, nullable=False)
    archivo_adjunto_url  = Column(String(255), nullable=True)
    comentarios_director = Column(Text, nullable=True)
    # Flujo de 2 niveles:
    # - Encargado: VERIFICADO / RECHAZADO
    # - Admin: APROBADO / RECHAZADO
    estado_encargado = Column(String(20), nullable=True, default=None)  # VERIFICADO or RECHAZADO
    estado_admin = Column(String(20), nullable=True, default=None)      # APROBADO or RECHAZADO
    verificado_por       = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    verificado_en        = Column(DateTime(timezone=True), nullable=True)
    aprobado_por         = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    aprobado_en          = Column(DateTime(timezone=True), nullable=True)
    creado_en            = Column(DateTime(timezone=True), server_default=func.now())

    asistencia = relationship("Asistencia", back_populates="reporte")