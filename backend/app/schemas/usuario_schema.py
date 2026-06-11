from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    carnet_identidad: str
    ru: Optional[str] = None
    unidad_asignada: Optional[str] = None
    email: EmailStr
    celular: str = Field(..., max_length=20)
    password: str
    rol_id: int
    carrera_id: Optional[int] = None
    programa_id: Optional[int] = None
    meta_horas_pasantia: Optional[float] = None
    proyecto_nombre: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    nombres: str
    apellidos: str
    carnet_identidad: str
    ru: Optional[str] = None
    unidad_asignada: Optional[str] = None
    username: str
    email: EmailStr
    celular: Optional[str] = None
    rol_id: int
    carrera_id: Optional[int]
    estado: bool
    rol: Optional[str] = None
    carrera_nombre: Optional[str] = None
    carrera_logo_url: Optional[str] = None
    programa_id: Optional[int] = None
    programa_nombre: Optional[str] = None
    programa_gestion: Optional[str] = None
    programa_documento_url: Optional[str] = None
    proyecto_nombre: Optional[str] = None
    proyecto_documento_url: Optional[str] = None
    meta_horas_pasantia: Optional[float] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    carnet_identidad: Optional[str] = None
    ru: Optional[str] = None
    unidad_asignada: Optional[str] = None
    email: Optional[EmailStr] = None
    celular: Optional[str] = Field(default=None, max_length=20)
    carrera_id: Optional[int] = None
    programa_id: Optional[int] = None
    estado: Optional[bool] = None
    proyecto_nombre: Optional[str] = None
    proyecto_documento_url: Optional[str] = None
    meta_horas_pasantia: Optional[float] = None


class MiPerfilUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    celular: Optional[str] = Field(default=None, max_length=20)
    ru: Optional[str] = None

    password_actual: Optional[str] = None
    nueva_password: Optional[str] = None
