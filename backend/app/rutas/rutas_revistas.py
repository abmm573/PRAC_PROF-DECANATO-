from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.base_datos.conexion import obtener_bd
from app.modelos.revista import Revista, EstadoRevista
from app.modelos.usuario import Usuario
from app.esquemas.revista import RevistaCrear, RevistaRespuesta, EstadoActualizar, ResenaCrear, TiempoLectura
from app.nucleo.seguridad import obtener_usuario_actual

from app.modelos.revision import HistorialRevision
from app.modelos.resena import Resena
from app.modelos.estadistica_lectura import EstadisticaLectura

enrutador = APIRouter()

def enriquecer_estadisticas_revista(revista, bd: Session):
    estadisticas = bd.query(EstadisticaLectura).filter(EstadisticaLectura.revista_id == revista.id).all()
    revista.vistas = len(estadisticas)
    revista.tiempo_lectura_total_segundos = sum(est.tiempo_lectura_segundos or 0 for est in estadisticas)
    return revista

# --- 1. CREAR REVISTA (Autor) ---
@enrutador.post("/", response_model=RevistaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_revista(
    datos_revista: RevistaCrear, 
    bd: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Guarda los datos de la revista en PostgreSQL. Requiere Token JWT."""
    nueva_revista = Revista(
        titulo=datos_revista.titulo,
        descripcion=datos_revista.descripcion,
        categoria=datos_revista.categoria,
        ruta_portada=datos_revista.ruta_portada, 
        ruta_pdf=datos_revista.ruta_pdf,        
        autor_id=usuario_actual.id,             
        estado=EstadoRevista.PENDIENTE          
    )
    
    bd.add(nueva_revista)
    bd.commit()
    bd.refresh(nueva_revista)
    
    return nueva_revista

# --- 2. LISTAR REVISTAS PÚBLICAS (Portal Público) ---
@enrutador.get("/publicas", response_model=List[RevistaRespuesta])
def listar_revistas_publicas(bd: Session = Depends(obtener_bd)):
    """Devuelve todas las revistas aprobadas. Ruta pública sin Token."""
    revistas = bd.query(Revista).filter(Revista.estado == EstadoRevista.APROBADA).order_by(Revista.fecha_creacion.desc()).all()
    return [enriquecer_estadisticas_revista(revista, bd) for revista in revistas]

# --- 3. LISTAR TODAS LAS REVISTAS (Panel Moderador) ---
@enrutador.get("/admin/todas", response_model=List[RevistaRespuesta])
def listar_todas_admin(
    bd: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Devuelve todas las revistas (Pendientes, Aprobadas, Rechazadas) para el moderador."""
    if usuario_actual.rol.value not in ["ADMINISTRADOR", "MODERADOR"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos.")
    
    revistas = bd.query(Revista).order_by(Revista.fecha_creacion.desc()).all()
    return [enriquecer_estadisticas_revista(revista, bd) for revista in revistas]

# --- 4. ACTUALIZAR ESTADO Y FEEDBACK (Panel Moderador) ---
@enrutador.put("/{revista_id}/estado", response_model=RevistaRespuesta)
def actualizar_estado_revista(
    revista_id: int, 
    datos: EstadoActualizar, 
    bd: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Permite a un Moderador aprobar/rechazar una revista y dejar feedback."""
    if usuario_actual.rol.value not in ["ADMINISTRADOR", "MODERADOR"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos.")

    revista = bd.query(Revista).filter(Revista.id == revista_id).first()
    if not revista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La revista no existe.")

    # 1. Cambiamos el estado de la revista
    if datos.estado == "APROBADA":
        revista.estado = EstadoRevista.APROBADA
    elif datos.estado == "RECHAZADA":
        revista.estado = EstadoRevista.RECHAZADA
    elif datos.estado == "PENDIENTE":
        revista.estado = EstadoRevista.PENDIENTE

    # 2. Siempre creamos un registro de auditoría si se aprueba o rechaza
    if datos.estado in ["APROBADA", "RECHAZADA"]:
        # Si la aprobaron y no hay motivo, ponemos un texto por defecto
        texto_observacion = datos.observaciones if datos.observaciones else f"Revista {datos.estado.lower()} por moderación."
        
        nueva_revision = HistorialRevision(
            revista_id=revista.id,
            moderador_id=usuario_actual.id, # ¡Aquí atrapamos al responsable!
            observaciones=texto_observacion
        )
        bd.add(nueva_revision)
        
    bd.commit()
    bd.refresh(revista)
    
    # Retornamos la revista completa para que el frontend vea los cambios al instante
    return revista

# --- 5. LISTAR MIS REVISTAS (Panel Autor) ---
@enrutador.get("/mis-revistas", response_model=List[RevistaRespuesta])
def listar_mis_revistas(
    bd: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Devuelve el historial de revistas subidas por el usuario logueado."""
    revistas = bd.query(Revista).filter(Revista.autor_id == usuario_actual.id).order_by(Revista.fecha_creacion.desc()).all()
    return [enriquecer_estadisticas_revista(revista, bd) for revista in revistas]

# --- 6. ESTADÍSTICAS DEL AUTOR ---
@enrutador.get("/mis-revistas/estadisticas")
def obtener_estadisticas_autor(
    bd: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Devuelve un resumen de visualizaciones y tiempo de lectura de todas las revistas del autor."""
    revistas = bd.query(Revista).filter(Revista.autor_id == usuario_actual.id).all()
    
    total_vistas = 0
    total_tiempo_segundos = 0
    total_resenas = 0
    promedio_estrellas = 0
    
    for revista in revistas:
        estadisticas = bd.query(EstadisticaLectura).filter(EstadisticaLectura.revista_id == revista.id).all()
        total_vistas += len(estadisticas)
        for est in estadisticas:
            total_tiempo_segundos += est.tiempo_lectura_segundos or 0
        
        resenas = bd.query(Resena).filter(Resena.revista_id == revista.id).all()
        total_resenas += len(resenas)
        if resenas:
            suma = sum(r.calificacion for r in resenas)
            promedio_estrellas += suma / len(resenas)
            
    revistas_con_resenas = len([r for r in revistas if bd.query(Resena).filter(Resena.revista_id == r.id).count() > 0])
    promedio_estrellas = (promedio_estrellas / revistas_con_resenas) if revistas_con_resenas > 0 else 0
    
    return {
        "total_revistas": len(revistas),
        "total_vistas": total_vistas,
        "total_tiempo_segundos": total_tiempo_segundos,
        "total_tiempo_formateado": f"{total_tiempo_segundos // 3600}h {(total_tiempo_segundos % 3600) // 60}m",
        "total_resenas": total_resenas,
        "promedio_estrellas": round(promedio_estrellas, 1)
    }

# --- 7. OBTENER DETALLE DE UNA REVISTA ---
@enrutador.get("/{revista_id}", response_model=RevistaRespuesta)
def obtener_revista_por_id(revista_id: int, bd: Session = Depends(obtener_bd)):
    """Devuelve los detalles de una revista específica (solo si está aprobada)."""
    revista = bd.query(Revista).filter(
        Revista.id == revista_id, 
        Revista.estado == EstadoRevista.APROBADA
    ).first()
    
    if not revista:
        raise HTTPException(status_code=404, detail="Revista no encontrada o no disponible.")
    return enriquecer_estadisticas_revista(revista, bd)

# --- 8. REGISTRAR VISTA ---
@enrutador.post("/{revista_id}/vista")
def registrar_vista(revista_id: int, bd: Session = Depends(obtener_bd)):
    """Registra una nueva visualización de la revista."""
    revista = bd.query(Revista).filter(Revista.id == revista_id).first()
    if not revista:
        raise HTTPException(status_code=404, detail="Revista no encontrada")
    
    nueva_estadistica = EstadisticaLectura(revista_id=revista_id, tiempo_lectura_segundos=0)
    bd.add(nueva_estadistica)
    bd.commit()
    return {"mensaje": "Vista registrada correctamente"}

# --- 9. REGISTRAR TIEMPO LECTURA ---
@enrutador.post("/{revista_id}/tiempo")
def registrar_tiempo(revista_id: int, datos: TiempoLectura, bd: Session = Depends(obtener_bd)):
    """Registra el tiempo que el usuario pasó leyendo el PDF."""
    revista = bd.query(Revista).filter(Revista.id == revista_id).first()
    if not revista:
        raise HTTPException(status_code=404, detail="Revista no encontrada")
    
    nueva_estadistica = EstadisticaLectura(revista_id=revista_id, tiempo_lectura_segundos=datos.segundos)
    bd.add(nueva_estadistica)
    bd.commit()
    return {"mensaje": "Tiempo de lectura registrado correctamente"}

# --- 10. CREAR RESEÑA ---
@enrutador.post("/{revista_id}/resenas")
def crear_resena(
    revista_id: int,
    datos: ResenaCrear,
    bd: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Permite a un usuario logueado dejar una calificación y comentario."""
    nueva_resena = Resena(
        calificacion=datos.calificacion,
        comentario=datos.comentario,
        revista_id=revista_id,
        usuario_id=usuario_actual.id
    )
    bd.add(nueva_resena)
    bd.commit()
    return {"mensaje": "¡Gracias por tu reseña!"}

# --- 11. OBTENER RESEÑAS ---
@enrutador.get("/{revista_id}/resenas")
def obtener_resenas(revista_id: int, bd: Session = Depends(obtener_bd)):
    """Devuelve los comentarios y estrellas para mostrarlos en el portal."""
    resenas = bd.query(Resena).filter(Resena.revista_id == revista_id).order_by(Resena.fecha.desc()).all()
    
    resultado = []
    for r in resenas:
        resultado.append({
            "id": r.id,
            "calificacion": r.calificacion,
            "comentario": r.comentario,
            "fecha": r.fecha,
            "usuario_correo": r.usuario.correo 
        })
    return resultado

# --- 12. ELIMINAR REVISTA (Solo Administrador) ---
@enrutador.delete("/{revista_id}")
def eliminar_revista(
    revista_id: int, 
    bd: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Permite exclusivamente a un ADMINISTRADOR eliminar una revista del sistema."""
    
    # 1. Verificamos que sea el administrador supremo
    if usuario_actual.rol.value != "ADMINISTRADOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acceso denegado. Solo los administradores pueden eliminar revistas publicadas."
        )

    # 2. Buscamos la revista
    revista = bd.query(Revista).filter(Revista.id == revista_id).first()
    if not revista:
        raise HTTPException(status_code=404, detail="La revista no existe.")

    # 3. La eliminamos de la base de datos
    bd.delete(revista)
    bd.commit()
    
    return {"mensaje": "Revista eliminada exitosamente del sistema."}