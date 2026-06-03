from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.base_datos.conexion import Base
import enum

# Definimos los estados por los que pasará una revista
class EstadoRevista(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"

class Revista(Base):
    __tablename__ = "revistas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    # Las rutas donde guardamos los archivos físicos
    ruta_portada = Column(String(255), nullable=True)
    ruta_pdf = Column(String(255), nullable=True)
    
    categoria = Column(String(100), nullable=True)
    estado = Column(SQLEnum(EstadoRevista), default=EstadoRevista.PENDIENTE)
    
    # Clave foránea: Conecta la revista con el ID del usuario que la subió
    autor_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))

    # Fechas automáticas
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Magia de SQLAlchemy: Relaciones
    autor = relationship("Usuario", backref="revistas")
    
    # Conecta la revista con el feedback de los moderadores y las reseñas de los lectores
    # Usamos cascade para que si borras una revista, se borren sus comentarios automáticamente
    revisiones = relationship("HistorialRevision", back_populates="revista", cascade="all, delete-orphan")
    resenas = relationship("Resena", back_populates="revista", cascade="all, delete-orphan")