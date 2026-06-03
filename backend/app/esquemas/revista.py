from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.modelos.revista import EstadoRevista

# ==========================================
# ESQUEMAS AUXILIARES (Para anidamiento)
# ==========================================

class UsuarioBasico(BaseModel):
    """Esquema ligero para enviar datos del moderador o autor sin revelar su contraseña"""
    id: int
    nombre: str
    correo: str
    
    class Config:
        from_attributes = True


# ==========================================
# ESQUEMAS DE ENTRADA (Frontend -> Backend)
# ==========================================

class RevistaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None

class RevistaCrear(RevistaBase):
    ruta_portada: Optional[str] = None
    ruta_pdf: Optional[str] = None

class ResenaCrear(BaseModel):
    calificacion: int  # Del 1 al 5
    comentario: Optional[str] = None

class TiempoLectura(BaseModel):
    segundos: int

class EstadoActualizar(BaseModel):
    estado: str
    observaciones: Optional[str] = None


# ==========================================
# ESQUEMAS DE SALIDA (Backend -> Frontend)
# ==========================================

class RevisionRespuesta(BaseModel):
    observaciones: str
    fecha_revision: datetime
    
    # --- NUEVO: Datos del Moderador ---
    moderador_id: Optional[int] = None
    moderador: Optional[UsuarioBasico] = None  # <-- Esto permite que Vue lea moderador.nombre
    
    class Config:
        from_attributes = True


class ResenaRespuesta(BaseModel):
    id: int
    calificacion: int
    comentario: Optional[str]
    fecha: datetime
    usuario_id: int
    usuario_correo: Optional[str] = None # Útil para mostrar quién comentó
    
    class Config:
        from_attributes = True

class RevistaRespuesta(RevistaBase):
    id: int
    ruta_portada: Optional[str]
    ruta_pdf: Optional[str]
    estado: EstadoRevista
    autor_id: int
    
    # --- NUEVO: Agregamos el autor para verlo en el panel ---
    autor: Optional[UsuarioBasico] = None 
    
    fecha_creacion: datetime
    
    # --- Estadísticas ---
    vistas: int = 0
    tiempo_lectura_total_segundos: int = 0
    
    # --- Listas relacionadas ---
    revisiones: List[RevisionRespuesta] = []
    resenas: List[ResenaRespuesta] = []

    class Config:
        from_attributes = True