from pydantic import BaseModel
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCrear(CategoriaBase):
    pass

class CategoriaRespuesta(CategoriaBase):
    id: int

    class Config:
        from_attributes = True