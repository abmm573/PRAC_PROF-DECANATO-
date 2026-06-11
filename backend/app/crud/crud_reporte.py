from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.asistencia import Reporte, Asistencia
from app.models.usuario import Usuario
from app.models.reporte_historial import ReporteEstadoHistorial
from app.schemas.reporte_schema import ReporteCreate, ReporteEvaluar

def crear_reporte(db: Session, reporte: ReporteCreate):
    db_reporte = Reporte(
        asistencia_id=reporte.asistencia_id,
        actividades_realizadas=reporte.actividades_realizadas,
        archivo_adjunto_url=reporte.archivo_adjunto_url
    )
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte

# def obtener_reportes(db: Session, carrera_id: int = None):
#     query = db.query(Reporte)
#     if carrera_id:
#         query = query.join(Asistencia).join(Usuario).filter(Usuario.carrera_id == carrera_id)
#     return query.all()

# def evaluar_reporte(db: Session, reporte_id: int, evaluacion: ReporteEvaluar, revisado_por_id: int):
#     db_reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
#     if db_reporte:
#         db_reporte.estado = evaluacion.estado
#         db_reporte.comentarios_director = evaluacion.comentarios_director
#         db_reporte.revisado_por = revisado_por_id
#         db.commit()
#         db.refresh(db_reporte)
#     return db_reporte


# MODIFICADO ------------
def obtener_reportes(db: Session, carrera_id: int = None):
    query = (
        db.query(Reporte)
        .join(Asistencia, Reporte.asistencia_id == Asistencia.id)
        .join(Usuario,    Asistencia.pasante_id  == Usuario.id)
    )

    if carrera_id is not None:
        query = query.filter(Usuario.carrera_id == carrera_id)

    return query.order_by(Reporte.creado_en.desc()).all()


# MODIFICADO --------------
def evaluar_reporte(db: Session, reporte_id: int, estado: str, comentarios: str, revisado_por: int, rol_usuario: str):
    db_reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if db_reporte:
        estado_norm = (estado or "").strip().upper()
        now = datetime.now(timezone.utc)
        
        # Determinar qué campo actualizar basado en el rol
        if rol_usuario == "ENCARGADO":
            estado_anterior = (db_reporte.estado_encargado or "").strip().upper() if db_reporte.estado_encargado else None
            db_reporte.estado_encargado = estado_norm
            db_reporte.verificado_por = revisado_por
            db_reporte.verificado_en = now
        elif rol_usuario == "ADMINISTRADOR":
            estado_anterior = (db_reporte.estado_admin or "").strip().upper() if db_reporte.estado_admin else None
            db_reporte.estado_admin = estado_norm
            db_reporte.aprobado_por = revisado_por
            db_reporte.aprobado_en = now
        
        # Acumular comentarios en lugar de sobrescribir
        comentario_existente = db_reporte.comentarios_director or ""
        if comentarios and comentarios.strip():
            # Agregar información de quién hace el comentario
            prefijo = f"[{rol_usuario}] " if rol_usuario else ""
            nuevo_comentario = f"{prefijo}{comentarios.strip()}"
            
            # Si ya hay comentarios, agregar el nuevo con separador
            if comentario_existente.strip():
                db_reporte.comentarios_director = f"{comentario_existente}\n\n{nuevo_comentario}"
            else:
                db_reporte.comentarios_director = nuevo_comentario
        elif rol_usuario == "ADMINISTRADOR":
            # Si el admin no envía comentario pero hay uno existente, mantenerlo
            pass  # No modificar el campo comentarios_director
        
        # No actualizar el campo legacy 'estado' - usar solo los campos separados

        # GUARDAR EN EL HISTORIAL (Siempre que haya un cambio de estado)
        historial_entry = ReporteEstadoHistorial(
            reporte_id=db_reporte.id,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_norm,
            comentarios=str(comentarios),
            actor_id=revisado_por,
        )
        db.add(historial_entry)

        db.commit()
        db.refresh(db_reporte)
    return db_reporte

# NUEVA FUNCIÓN: Para que el Superusuario vea la auditoría
def obtener_historial_reporte(db: Session, reporte_id: int):
    # Hacemos un join con Usuario para obtener el nombre de quien hizo la acción
    historial = (
        db.query(ReporteEstadoHistorial, Usuario.nombres, Usuario.apellidos)
        .join(Usuario, ReporteEstadoHistorial.actor_id == Usuario.id)
        .filter(ReporteEstadoHistorial.reporte_id == reporte_id)
        .order_by(ReporteEstadoHistorial.creado_en.desc())
        .all()
    )
    
    # Formateamos la respuesta
    resultado = []
    for reg, nombres, apellidos in historial:
        item = reg.__dict__
        item["actor_nombre"] = f"{nombres} {apellidos}"
        resultado.append(item)
        
    return resultado