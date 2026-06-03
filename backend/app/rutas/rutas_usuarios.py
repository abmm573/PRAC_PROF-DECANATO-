from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.base_datos.conexion import obtener_bd
from app.modelos.usuario import Usuario, RolUsuario
from app.nucleo.seguridad import obtener_usuario_actual, obtener_hash_contrasena 

enrutador = APIRouter()

# --- ESQUEMAS ADAPTADOS ---
class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str  
    correo: str
    rol: RolUsuario 
    activo: bool # <--- Agregado para el Toggle de Vue

    class Config:
        from_attributes = True

class UsuarioCrearAdmin(BaseModel):
    nombre: str
    correo: str
    contrasena: str
    rol: str

class UsuarioActualizar(BaseModel):
    nombre: str
    correo: str
    rol: str

# <--- NUEVO ESQUEMA PARA RECIBIR EL ESTADO --->
class EstadoActualizar(BaseModel):
    activo: bool


# --- RUTAS DE ADMINISTRACIÓN ---

def verificar_admin(usuario: Usuario = Depends(obtener_usuario_actual)):
    """Middleware para asegurar que solo el ADMIN entra aquí"""
    if usuario.rol.value != "ADMINISTRADOR":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo administradores.")
    return usuario

@enrutador.get("/", response_model=List[UsuarioRespuesta])
def listar_usuarios(bd: Session = Depends(obtener_bd), admin: Usuario = Depends(verificar_admin)):
    """Obtiene todos los usuarios del sistema."""
    return bd.query(Usuario).order_by(Usuario.id.desc()).all()

@enrutador.post("/", response_model=UsuarioRespuesta)
def crear_usuario_desde_admin(datos: UsuarioCrearAdmin, bd: Session = Depends(obtener_bd), admin: Usuario = Depends(verificar_admin)):
    """Permite al admin crear un usuario directamente."""
    usuario_existente = bd.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        contrasena_hash=obtener_hash_contrasena(datos.contrasena), 
        rol=datos.rol,
        activo=True # <--- Por defecto los creamos activos
    )
    bd.add(nuevo_usuario)
    bd.commit()
    bd.refresh(nuevo_usuario)
    return nuevo_usuario

@enrutador.put("/{usuario_id}", response_model=UsuarioRespuesta)
def actualizar_usuario(usuario_id: int, datos: UsuarioActualizar, bd: Session = Depends(obtener_bd), admin: Usuario = Depends(verificar_admin)):
    """Edita los datos de un usuario."""
    usuario = bd.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    usuario.nombre = datos.nombre
    usuario.correo = datos.correo
    usuario.rol = datos.rol
    
    bd.commit()
    bd.refresh(usuario)
    return usuario


# <--- NUEVA RUTA PARA EL TOGGLE (ACTIVAR/DESACTIVAR) --->
@enrutador.put("/{usuario_id}/estado")
def cambiar_estado_usuario(usuario_id: int, datos: EstadoActualizar, bd: Session = Depends(obtener_bd), admin: Usuario = Depends(verificar_admin)):
    """Activa o suspende a un usuario"""
    if usuario_id == admin.id and not datos.activo:
        raise HTTPException(status_code=400, detail="No puedes desactivar tu propia cuenta de Administrador.")
        
    usuario = bd.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    usuario.activo = datos.activo
    bd.commit()
    
    estado_texto = "habilitado" if datos.activo else "suspendido"
    return {"mensaje": f"Usuario {estado_texto} exitosamente."}


@enrutador.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, bd: Session = Depends(obtener_bd), admin: Usuario = Depends(verificar_admin)):
    """Elimina permanentemente a un usuario. (Precaución)"""
    if usuario_id == admin.id:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo.")
        
    usuario = bd.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    bd.delete(usuario)
    bd.commit()
    return {"mensaje": "Usuario eliminado correctamente."}