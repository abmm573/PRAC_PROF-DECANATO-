from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.base_datos.conexion import Base

class EstadisticaLectura(Base):
    __tablename__ = "estadisticas_lectura"

    id = Column(Integer, primary_key=True, index=True)
    revista_id = Column(Integer, ForeignKey("revistas.id", ondelete="CASCADE"))
    ip_lector = Column(String(50), nullable=True)
    tiempo_lectura_segundos = Column(Integer, default=0)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con Revista
    revista = relationship("Revista", backref="estadisticas")