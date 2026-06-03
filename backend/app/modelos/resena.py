from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.base_datos.conexion import Base

class Resena(Base):
    __tablename__ = "resenas"

    id = Column(Integer, primary_key=True, index=True)
    calificacion = Column(Integer, nullable=False) # Aquí irán las estrellas (1 al 5)
    comentario = Column(Text, nullable=True)
    
    # Claves foráneas para saber a qué revista pertenece y quién la comentó
    revista_id = Column(Integer, ForeignKey("revistas.id", ondelete="CASCADE"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))

    # Fecha automática
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones para que la magia de SQLAlchemy funcione
    revista = relationship("Revista", back_populates="resenas")
    usuario = relationship("Usuario")