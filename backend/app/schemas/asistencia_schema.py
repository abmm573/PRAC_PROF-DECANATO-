from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AsistenciaCreate(BaseModel):
    pasante_id: int
    latitud_entrada:  Optional[float] = Field(None)
    longitud_entrada: Optional[float] = Field(None)


class FichajePublicoEntrada(BaseModel):
    username: str


class FichajePublicoSalida(BaseModel):
    username: str


class AsistenciaUpdate(BaseModel):
    latitud_salida:  Optional[float] = None
    longitud_salida: Optional[float] = None


class AsistenciaResponse(BaseModel):
    id:               int
    pasante_id:       int
    fecha:            datetime
    hora_entrada:     datetime
    hora_salida:      Optional[datetime] = None
    horas_trabajadas: Optional[float]    = None
    esta_en_facultad: Optional[bool]     = None
    mensaje_alerta:   Optional[str]      = None

    class Config:
        from_attributes = True