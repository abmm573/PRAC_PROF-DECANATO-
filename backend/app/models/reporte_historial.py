from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class ReporteEstadoHistorial(Base):
    __tablename__ = "reporte_estado_historial"

    id = Column(Integer, primary_key=True, index=True)
    reporte_id = Column(Integer, ForeignKey("reportes.id", ondelete="CASCADE"), nullable=False, index=True)
    estado_anterior = Column(String(20), nullable=True)
    estado_nuevo = Column(String(20), nullable=False)
    comentarios = Column(Text, nullable=False)
    actor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    reporte = relationship("Reporte")
    actor = relationship("Usuario")

