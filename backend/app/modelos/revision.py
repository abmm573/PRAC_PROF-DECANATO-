from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.base_datos.conexion import Base

class HistorialRevision(Base):
    __tablename__ = "historial_revisiones"

    id = Column(Integer, primary_key=True, index=True)
    
    # Claves Foráneas
    revista_id = Column(Integer, ForeignKey("revistas.id", ondelete="CASCADE"))
    moderador_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    
    observaciones = Column(Text, nullable=False)
    fecha_revision = Column(DateTime(timezone=True), server_default=func.now())

    # --- RELACIONES CORRECTAS ---
    # Conecta con la revista
    revista = relationship("Revista", back_populates="revisiones")
    
    # Conecta con el usuario que moderó (Sin usar backref="revistas")
    moderador = relationship("Usuario")