from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

class ReporteCreate(BaseModel):
    asistencia_id: int
    actividades_realizadas: str
    archivo_adjunto_url: Optional[str] = None 
    
class ReporteEvaluar(BaseModel):
    estado: str
    comentarios_director: str
    es_rectificacion: Optional[bool] = False  # Para saber si es una rectificación

    @field_validator("comentarios_director")
    @classmethod
    def validar_comentario_obligatorio(cls, v):
        if not v or not str(v).strip():
            raise ValueError("El comentario es obligatorio para evaluar el reporte.")
        return str(v).strip()

class ReporteResponse(BaseModel):
    id: int
    asistencia_id: int
    actividades_realizadas: str
    estado_encargado: Optional[str] = None
    estado_admin: Optional[str] = None
    comentarios_director: Optional[str] = None
    creado_en: datetime
    verificado_por: Optional[int] = None
    verificado_en: Optional[datetime] = None
    aprobado_por: Optional[int] = None
    aprobado_en: Optional[datetime] = None

    nombre_pasante: Optional[str] = None

    class Config:
        from_attributes = True


class ReporteHistorialItem(BaseModel):
    id: int
    reporte_id: int
    estado_anterior: Optional[str] = None
    estado_nuevo: str
    comentarios: str
    actor_id: int
    # Añadimos esto para que el frontend sepa quién hizo el cambio
    actor_nombre: Optional[str] = None 
    creado_en: datetime

    class Config:
        from_attributes = True
