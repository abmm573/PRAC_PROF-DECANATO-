from pydantic import BaseModel
from typing import Optional


class CarreraCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    logo_url: Optional[str] = None
    estado: bool = True


class CarreraResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    logo_url: Optional[str] = None
    estado: bool

    class Config:
        from_attributes = True


class CarreraUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    logo_url: Optional[str] = None
    estado: Optional[bool] = None
