from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.base_datos.conexion import obtener_bd
from app.modelos.categoria import Categoria
from app.esquemas.categoria import CategoriaCrear, CategoriaRespuesta
from app.modelos.usuario import Usuario
from app.nucleo.seguridad import obtener_usuario_actual

enrutador = APIRouter()

@enrutador.get("/", response_model=List[CategoriaRespuesta])
def listar_categorias(bd: Session = Depends(obtener_bd)):
    """Público: Devuelve la lista de categorías para el formulario de subida."""
    return bd.query(Categoria).order_by(Categoria.nombre).all()

@enrutador.post("/", response_model=CategoriaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_categoria(datos: CategoriaCrear, bd: Session = Depends(obtener_bd), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Solo Admin: Crea una nueva categoría."""
    if usuario_actual.rol.value != "ADMINISTRADOR":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo administradores.")
    
    existe = bd.query(Categoria).filter(Categoria.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Esta categoría ya existe.")
        
    nueva = Categoria(nombre=datos.nombre, descripcion=datos.descripcion)
    bd.add(nueva)
    bd.commit()
    bd.refresh(nueva)
    return nueva

@enrutador.put("/{cat_id}", response_model=CategoriaRespuesta)
def editar_categoria(cat_id: int, datos: CategoriaCrear, bd: Session = Depends(obtener_bd), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    if usuario_actual.rol.value != "ADMINISTRADOR":
        raise HTTPException(status_code=403, detail="Acceso denegado.")
        
    cat = bd.query(Categoria).filter(Categoria.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
        
    cat.nombre = datos.nombre
    cat.descripcion = datos.descripcion
    bd.commit()
    bd.refresh(cat)
    return cat

@enrutador.delete("/{cat_id}")
def eliminar_categoria(cat_id: int, bd: Session = Depends(obtener_bd), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    if usuario_actual.rol.value != "ADMINISTRADOR":
        raise HTTPException(status_code=403, detail="Acceso denegado.")
        
    cat = bd.query(Categoria).filter(Categoria.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
        
    bd.delete(cat)
    bd.commit()
    return {"mensaje": "Categoría eliminada con éxito."}