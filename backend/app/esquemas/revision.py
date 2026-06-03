from pydantic import BaseModel
from app.modelos.revista import EstadoRevista

class RevisionCrear(BaseModel):
    estado_nuevo: EstadoRevista # Solo aceptará "APROBADA" o "RECHAZADA"
    observaciones: str          # El feedback para el autor