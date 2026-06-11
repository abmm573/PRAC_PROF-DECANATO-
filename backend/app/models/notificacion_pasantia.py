from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.sql import func

from app.db.database import Base


class NotificacionPasantia(Base):
    __tablename__ = "notificaciones_pasantia"

    id = Column(Integer, primary_key=True, index=True)
    pasante_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    carrera_id = Column(Integer, ForeignKey("carreras.id"), nullable=True, index=True)
    total_horas = Column(Numeric(6, 2), nullable=False)
    enviado_a = Column(String(255), nullable=True)
    tipo_notificacion = Column(String(20), nullable=True, default="COMPLETADA")  # COMPLETADA, CERCA_COMPLETAR
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("pasante_id", "tipo_notificacion", name="uq_notif_pasantia_pasante_tipo"),
    )