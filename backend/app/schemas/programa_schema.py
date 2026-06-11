from pydantic import BaseModel, Field
from typing import Optional


class ProgramaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    gestion: Optional[str] = Field(default=None, max_length=20)
    estado: Optional[bool] = True


class ProgramaCreate(ProgramaBase):
    pass


class ProgramaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    gestion: Optional[str] = Field(default=None, max_length=20)
    estado: Optional[bool] = None
    documento_url: Optional[str] = Field(default=None, max_length=255)


class ProgramaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    gestion: Optional[str] = None
    estado: bool
    documento_url: Optional[str] = None

    class Config:
        from_attributes = True

