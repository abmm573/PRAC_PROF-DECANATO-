from sqlalchemy import Column, Integer, String, Boolean, Text, text
from app.db.database import Base

class Carrera(Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    logo_url = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=False, server_default=text('true'), default=True)

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
