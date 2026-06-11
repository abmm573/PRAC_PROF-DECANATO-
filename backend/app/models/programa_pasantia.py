from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.database import Base


class ProgramaPasantia(Base):
    __tablename__ = "programas_pasantia"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    gestion = Column(String(20), nullable=True)
    estado = Column(Boolean, default=True)
    documento_url = Column(String(255), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

