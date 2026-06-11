from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import case
from typing import List
from datetime import datetime, date, timedelta
import calendar
import io

from app.db.database import get_db
from app.schemas.reporte_schema import ReporteCreate, ReporteResponse, ReporteEvaluar, ReporteHistorialItem
from app.crud import crud_reporte
from app.models.usuario import Usuario
from app.models.asistencia import Reporte, Asistencia, Asistencia as AsistenciaModel
from app.models.reporte_historial import ReporteEstadoHistorial
from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.utils.generador_pdf import generar_comprobante_pdf
from app.utils.pasantia_completion import check_and_notify_completion
from app.utils.generador_reporte_pdf import generar_reporte_semanal, generar_reporte_mensual

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────
# POST /subir  —  solo el PASANTE puede subir o actualizar su reporte
# ─────────────────────────────────────────────────────────────────────────
@router.post("/subir", response_model=ReporteResponse, status_code=status.HTTP_201_CREATED)
def subir_reporte(
    reporte: ReporteCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    reporte_existente = db.query(Reporte).filter(Reporte.asistencia_id == reporte.asistencia_id).first()

    if reporte_existente:
        reporte_existente.actividades_realizadas = reporte.actividades_realizadas
        db.commit()
        db.refresh(reporte_existente)
        return reporte_existente
    else:
        return crud_reporte.crear_reporte(db=db, reporte=reporte)

# ─────────────────────────────────────────────────────────────────────────
# POST /publico/crear — Sin token — el pasante crea su reporte
# ─────────────────────────────────────────────────────────────────────────
@router.post("/publico/crear", response_model=ReporteResponse, status_code=status.HTTP_201_CREATED)
def crear_reporte_publico(
    reporte: ReporteCreate,
    db: Session = Depends(get_db)
):
    asistencia = db.query(Asistencia).filter(Asistencia.id == reporte.asistencia_id).first()
    if not asistencia:
        raise HTTPException(404, detail="Asistencia no encontrada.")

    if not asistencia.hora_salida:
        raise HTTPException(400, detail="No puedes crear el reporte antes de registrar tu salida.")

    existente = db.query(Reporte).filter(Reporte.asistencia_id == reporte.asistencia_id).first()
    if existente:
        existente.actividades_realizadas = reporte.actividades_realizadas
        db.commit()
        db.refresh(existente)
        return existente

    return crud_reporte.crear_reporte(db=db, reporte=reporte)

# ─────────────────────────────────────────────────────────────────────────
# GET /listar — ADMINISTRADOR y ENCARGADO
# ─────────────────────────────────────────────────────────────────────────
@router.get("/listar")
def listar_reportes(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    # TEMPORAL: Versión ultra simplificada para depurar
    print("[DEBUG] Iniciando listar_reportes ultra simplificado")
    
    try:
        # Consulta con joins para obtener datos completos
        from sqlalchemy.orm import joinedload
        
        reportes_db = (
            db.query(Reporte)
            .options(
                joinedload(Reporte.asistencia).joinedload(Asistencia.pasante).joinedload(Usuario.carrera)
            )
            .limit(10)
            .all()
        )
        print(f"[DEBUG] Cargados {len(reportes_db)} reportes")
        
        resultado = []
        for r in reportes_db:
            pasante = r.asistencia.pasante if r.asistencia else None
            resultado.append({
                "id": r.id,
                "asistencia_id": r.asistencia_id,
                "pasante_id": r.asistencia.pasante_id if r.asistencia else None,
                "actividades_realizadas": r.actividades_realizadas,
                "estado_encargado": r.estado_encargado,
                "estado_admin": r.estado_admin,
                "comentarios_director": r.comentarios_director,
                "creado_en": r.creado_en,
                "nombre_pasante": f"{pasante.nombres} {pasante.apellidos}" if pasante else "Desconocido",
                "carrera_nombre": pasante.unidad_asignada if pasante and pasante.unidad_asignada else "—",
                "carrera_id": pasante.carrera_id if pasante else None,
                "horas_trabajadas": float(r.asistencia.horas_trabajadas) if r.asistencia and r.asistencia.horas_trabajadas else 0,
                "fecha": r.asistencia.fecha if r.asistencia else None,
            })
        
        print(f"[DEBUG] Retornando {len(resultado)} resultados")
        return resultado
        
    except Exception as e:
        print(f"[DEBUG] Error en listar_reportes: {e}")
        raise HTTPException(500, detail=f"Error interno: {str(e)}")

# ─────────────────────────────────────────────────────────────────────────
# PUT /evaluar/{reporte_id} — ENCARGADO y ADMINISTRADOR
# ─────────────────────────────────────────────────────────────────────────
@router.put("/evaluar/{reporte_id}", response_model=ReporteResponse)
def evaluar_reporte(
    reporte_id: int,
    evaluacion: ReporteEvaluar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ENCARGADO", "ADMINISTRADOR"]))
):
    rol_nombre = (getattr(getattr(usuario_actual, "rol", None), "nombre", "") or "").upper()
    estado_req = (evaluacion.estado or "").strip().upper()
    comentarios = (evaluacion.comentarios_director or "").strip()
    es_rectificacion = evaluacion.es_rectificacion or False
    rep = None

    if not comentarios:
        raise HTTPException(status_code=400, detail="Debes dejar un comentario obligatoriamente.")

    # Obtener el reporte actual
    rep = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not rep:
        raise HTTPException(404, detail="Reporte no encontrado.")
    
    # Lógica de una sola modificación para encargados
    if rol_nombre == "ENCARGADO":
        # Si ya fue evaluado por encargado y no es rectificación, no permitir
        if rep.estado_encargado is not None and not es_rectificacion:
            raise HTTPException(400, detail="Este reporte ya fue evaluado anteriormente. Solo puedes modificarlo una vez seleccionando 'Rectificado'.")
        
        # Si es rectificación, solo permitir estado RECTIFICADO
        if es_rectificacion:
            if estado_req != "RECTIFICADO":
                raise HTTPException(400, detail="Para rectificar, el estado debe ser 'RECTIFICADO'.")
        else:
            # Primera evaluación - permitir solo VERIFICADO
            if estado_req != "VERIFICADO":
                raise HTTPException(400, detail="Estado inválido para ENCARGADO. Usa: VERIFICADO.")
    else:
        # ADMINISTRADOR puede aprobar/rechazar
        if estado_req not in ("APROBADO", "RECHAZADO"):
            raise HTTPException(400, detail="Estado inválido para ADMINISTRADOR. Usa: APROBADO o RECHAZADO.")

        if estado_req == "APROBADO":
            # El administrador puede aprobar cualquier reporte, no requiere verificación previa
            pass

    reporte_actualizado = crud_reporte.evaluar_reporte(
        db=db,
        reporte_id=reporte_id,
        estado=estado_req,
        comentarios=comentarios,
        revisado_por=usuario_actual.id,
        rol_usuario=rol_nombre
    )
    print(f"[DEBUG] CRUD ejecutado, resultado: {reporte_actualizado}")
    if not reporte_actualizado:
        print(f"[DEBUG] Error: CRUD retornó None")
        raise HTTPException(500, detail="Error al actualizar el reporte.")
    
    print(f"[DEBUG] Evaluación exitosa - ID: {reporte_actualizado.id}, estado_encargado: {reporte_actualizado.estado_encargado}")
    if rol_nombre != "ENCARGADO" and estado_req == "APROBADO":
        try:
            if rep and rep.asistencia and rep.asistencia.pasante_id:
                check_and_notify_completion(db, int(rep.asistencia.pasante_id))
        except Exception as e:
            print(f"[reportes] Error en notificacion de pasantia completada: {e}")
            
    return reporte_actualizado

# ─────────────────────────────────────────────────────────────────────────
# GET /historial/{reporte_id} — Historial y Auditoría
# ─────────────────────────────────────────────────────────────────────────
@router.get("/historial/{reporte_id}", response_model=List[ReporteHistorialItem])
def historial_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene el historial de cambios de estado de un reporte específico.
    Accesible para: PASANTE (sus propios reportes), ENCARGADO, ADMINISTRADOR"""
    from sqlalchemy.orm import joinedload
    
    print(f"[DEBUG] Solicitando historial para reporte_id: {reporte_id}")
    print(f"[DEBUG] Usuario actual: {usuario_actual.id}")
    
    # Verificar que el reporte existe
    reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not reporte:
        print(f"[DEBUG] Reporte {reporte_id} no encontrado")
        raise HTTPException(404, detail="Reporte no encontrado.")
    
    print(f"[DEBUG] Reporte encontrado: {reporte.id}")
    
    # Verificar permisos de acceso
    rol_nombre = (getattr(getattr(usuario_actual, "rol", None), "nombre", "") or "").upper()
    print(f"[DEBUG] Rol del usuario: {rol_nombre}")
    
    if rol_nombre == "PASANTE":
        # Pasante solo puede ver sus propios reportes
        if not reporte.asistencia or reporte.asistencia.pasante_id != usuario_actual.id:
            print(f"[DEBUG] Pasante no tiene permiso para ver este reporte")
            raise HTTPException(403, detail="No tienes permiso para ver este historial.")
    
    # Obtener el historial con información del actor
    historial = (
        db.query(ReporteEstadoHistorial)
        .options(joinedload(ReporteEstadoHistorial.actor))
        .filter(ReporteEstadoHistorial.reporte_id == reporte_id)
        .order_by(ReporteEstadoHistorial.creado_en.desc())
        .all()
    )
    
    print(f"[DEBUG] Historial encontrado: {len(historial)} items")
    
    # Formatear respuesta
    resultado = []
    for item in historial:
        resultado.append({
            "id": item.id,
            "reporte_id": item.reporte_id,
            "estado_anterior": item.estado_anterior,
            "estado_nuevo": item.estado_nuevo,
            "comentarios": item.comentarios,
            "actor_id": item.actor_id,
            "actor_nombre": f"{item.actor.nombres} {item.actor.apellidos}" if item.actor else "Desconocido",
            "actor_rol": getattr(item.actor.rol, "nombre", "Desconocido") if item.actor else "Desconocido",
            "creado_en": item.creado_en
        })
    
    print(f"[DEBUG] Retornando {len(resultado)} items de historial")
    return resultado

# ─────────────────────────────────────────────────────────────────────────
# GET /descargar/{reporte_id} — PASANTE, ENCARGADO, ADMINISTRADOR
# ─────────────────────────────────────────────────────────────────────────
@router.get("/descargar/{reporte_id}")
def descargar_reporte_pdf(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE", "ENCARGADO", "ADMINISTRADOR"]))
):
    print(f"[DEBUG] Solicitando descarga para reporte_id: {reporte_id}")
    print(f"[DEBUG] Usuario actual: {usuario_actual.id}")
    
    reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not reporte:
        print(f"[DEBUG] Reporte {reporte_id} no encontrado para descarga")
        raise HTTPException(404, detail="Reporte no encontrado.")

    print(f"[DEBUG] Reporte encontrado para descarga: {reporte.id}")

    asistencia = reporte.asistencia
    pasante = asistencia.pasante if asistencia else None
    carrera = pasante.carrera if pasante else None

    print(f"[DEBUG] Pasante: {pasante.nombres if pasante else 'No encontrado'}")
    print(f"[DEBUG] Asistencia: {asistencia.id if asistencia else 'No encontrada'}")

    datos_pdf = {
        "pasante_nombre": f"{pasante.nombres} {pasante.apellidos}" if pasante else "Pasante",
        "carrera_nombre": carrera.nombre if carrera else "No asignada",
        "fecha": asistencia.fecha.strftime("%d/%m/%Y") if asistencia and asistencia.fecha else "",
        "hora_entrada": asistencia.hora_entrada.strftime("%H:%M") if asistencia and asistencia.hora_entrada else "",
        "hora_salida": asistencia.hora_salida.strftime("%H:%M") if asistencia and asistencia.hora_salida else "Pendiente",
        "horas_trabajadas": float(asistencia.horas_trabajadas) if asistencia and asistencia.horas_trabajadas is not None else 0,
        "actividades": reporte.actividades_realizadas,
    }

    print(f"[DEBUG] Generando PDF con datos: {datos_pdf}")
    pdf_buffer = generar_comprobante_pdf(datos_pdf)
    print(f"[DEBUG] PDF generado exitosamente")
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=reporte_{reporte_id}.pdf"}
    )

# ─────────────────────────────────────────────────────────────────────────
# GET /ver/{asistencia_id} — PASANTE
# ─────────────────────────────────────────────────────────────────────────
@router.get("/ver/{asistencia_id}")
def ver_reporte_por_asistencia(
    asistencia_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    reporte = db.query(Reporte).filter(Reporte.asistencia_id == asistencia_id).first()
    if not reporte:
        raise HTTPException(404, detail="No hay reporte para esta asistencia.")
    return reporte

# ─────────────────────────────────────────────────────────────────────────
# GET /pdf/semanal — PASANTE (compatibilidad) - REACTIVADO
# ─────────────────────────────────────────────────────────────────────────
@router.get("/pdf/semanal")
def descargar_pdf_semanal_compat(
    anio: int,
    semana: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    """Endpoint de compatibilidad para el frontend del pasante."""
    try:
        # Llamar a la función correcta del generador
        from app.utils.generador_reporte_pdf import generar_reporte_semanal
        
        # Obtener datos del pasante
        pasante_data = {
            "nombres": usuario_actual.nombres,
            "apellidos": usuario_actual.apellidos,
            "carnet_identidad": usuario_actual.carnet_identidad,
            "ru": usuario_actual.carnet_identidad,  # Agregar campo RU
            "carrera": getattr(getattr(usuario_actual, "carrera", None), "nombre", None),
            "proyecto": getattr(usuario_actual, "proyecto_nombre", None)
        }
        
        # Obtener asistencias de la semana
        from datetime import datetime, timedelta
        from app.models.asistencia import Asistencia
        
        # Calcular rango de fechas para la semana
        fecha_inicio = datetime.strptime(f"{anio}-01-01", "%Y-%m-%d")
        if semana > 1:
            fecha_inicio += timedelta(weeks=semana-1)
        
        # Ajustar al lunes de esa semana
        dias_lunes = fecha_inicio.weekday()
        if dias_lunes != 0:
            fecha_inicio -= timedelta(days=dias_lunes)
        
        fecha_fin = fecha_inicio + timedelta(days=6)
        
        asistencias = db.query(Asistencia).filter(
            Asistencia.pasante_id == usuario_actual.id,
            Asistencia.fecha >= fecha_inicio.date(),
            Asistencia.fecha <= fecha_fin.date()
        ).all()
        
        # Formatear filas para el PDF
        filas = []
        for asist in asistencias:
            try:
                # Obtener reporte si existe
                from app.models.asistencia import Reporte
                from app.models.reporte_historial import ReporteEstadoHistorial
                
                reporte = db.query(Reporte).filter(Reporte.asistencia_id == asist.id).first()
                
                # Obtener historial de estados si existe el reporte
                historial_estados = []
                if reporte:
                    historial = db.query(ReporteEstadoHistorial).filter(
                        ReporteEstadoHistorial.reporte_id == reporte.id
                    ).order_by(ReporteEstadoHistorial.creado_en.asc()).all()
                    
                    for h in historial:
                        historial_estados.append(f"{h.estado_nuevo} ({h.creado_en.strftime('%d/%m %H:%M')})")
                
                # Determinar estado actual con historial
                estado = "SIN REGISTRO"
                if reporte:
                    estado = reporte.estado_admin or reporte.estado_encargado or "PENDIENTE"
                    if historial_estados:
                        estado = f"{estado} → {' → '.join(historial_estados)}"
                
                filas.append({
                    "fecha": asist.fecha.strftime("%d/%m/%Y"),
                    "hora_entrada": asist.hora_entrada.strftime("%H:%M") if asist.hora_entrada else "—",
                    "hora_salida": asist.hora_salida.strftime("%H:%M") if asist.hora_salida else "—",
                    "horas_trabajadas": str(asist.horas_trabajadas) if asist.horas_trabajadas else "—",
                    "horas_acumuladas": 0,  # Se calculará después
                    "estado_admin": estado.split(' →')[0] if ' →' in estado else estado,
                    "estado_encargado": reporte.estado_encargado if reporte else "",
                    "detalle": estado,
                    "comentario": reporte.actividades_realizadas if reporte else "",
                    "comentarios_director": reporte.comentarios_director if reporte else ""
                })
            except Exception as e:
                print(f"[reportes] Error procesando asistencia {asist.id}: {e}")
                # Agregar fila básica si hay error
                filas.append({
                    "fecha": asist.fecha.strftime("%d/%m/%Y"),
                    "hora_entrada": asist.hora_entrada.strftime("%H:%M") if asist.hora_entrada else "—",
                    "hora_salida": asist.hora_salida.strftime("%H:%M") if asist.hora_salida else "—",
                    "horas_trabajadas": str(asist.horas_trabajadas) if asist.horas_trabajadas else "—",
                    "horas_acumuladas": 0,
                    "estado_admin": "ERROR",
                    "estado_encargado": "",
                    "detalle": "ERROR",
                    "comentario": "",
                    "comentarios_director": ""
                })
        
        titulo = f"Reporte Semanal - ({anio})"
        
        pdf_buffer = generar_reporte_semanal(pasante_data, filas, titulo, anio=anio, semana=semana)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=reporte_semanal_{anio}_s{semana}.pdf"}
        )
    except Exception as e:
        print(f"[reportes] Error generando PDF semanal: {e}")
        raise HTTPException(500, detail="Error al generar el PDF semanal.")


# ─────────────────────────────────────────────────────────────────────────
# GET /pdf/mensual — PASANTE (compatibilidad) - REACTIVADO
# ─────────────────────────────────────────────────────────────────────────
@router.get("/pdf/mensual")
def descargar_pdf_mensual_compat(
    anio: int,
    mes: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    """Endpoint de compatibilidad para el frontend del pasante."""
    try:
        # Llamar a la función correcta del generador
        from app.utils.generador_reporte_pdf import generar_reporte_mensual
        
        # Obtener datos del pasante
        pasante_data = {
            "nombres": usuario_actual.nombres,
            "apellidos": usuario_actual.apellidos,
            "carnet_identidad": usuario_actual.carnet_identidad,
            "carrera": getattr(getattr(usuario_actual, "carrera", None), "nombre", None),
            "proyecto": getattr(usuario_actual, "proyecto_nombre", None)
        }
        
        # Obtener asistencias del mes
        from datetime import datetime, timedelta
        from app.models.asistencia import Asistencia
        
        # Calcular rango de fechas para el mes
        fecha_inicio = datetime(anio, mes, 1)
        if mes == 12:
            fecha_fin = datetime(anio + 1, 1, 1) - timedelta(days=1)
        else:
            fecha_fin = datetime(anio, mes + 1, 1) - timedelta(days=1)
        
        asistencias = db.query(Asistencia).filter(
            Asistencia.pasante_id == usuario_actual.id,
            Asistencia.fecha >= fecha_inicio.date(),
            Asistencia.fecha <= fecha_fin.date()
        ).all()
        
        # Formatear filas para el PDF
        filas = []
        for asist in asistencias:
            try:
                # Obtener reporte si existe
                from app.models.asistencia import Reporte
                reporte = db.query(Reporte).filter(Reporte.asistencia_id == asist.id).first()
                
                # Determinar estado
                estado = "SIN REGISTRO"
                if reporte:
                    estado = reporte.estado_admin or reporte.estado_encargado or "PENDIENTE"
                
                filas.append({
                    "fecha": asist.fecha.strftime("%d/%m/%Y"),
                    "hora_entrada": asist.hora_entrada.strftime("%H:%M") if asist.hora_entrada else "—",
                    "hora_salida": asist.hora_salida.strftime("%H:%M") if asist.hora_salida else "—",
                    "horas_trabajadas": str(asist.horas_trabajadas) if asist.horas_trabajadas else "—",
                    "horas_acumuladas": 0,  # Se calculará después
                    "detalle": estado,
                    "comentario": reporte.actividades_realizadas if reporte else "",
                    "comentarios_director": reporte.comentarios_director if reporte else ""
                })
            except Exception as e:
                print(f"[reportes] Error procesando asistencia mensual {asist.id}: {e}")
                # Agregar fila básica si hay error
                filas.append({
                    "fecha": asist.fecha.strftime("%d/%m/%Y"),
                    "hora_entrada": asist.hora_entrada.strftime("%H:%M") if asist.hora_entrada else "—",
                    "hora_salida": asist.hora_salida.strftime("%H:%M") if asist.hora_salida else "—",
                    "horas_trabajadas": str(asist.horas_trabajadas) if asist.horas_trabajadas else "—",
                    "horas_acumuladas": 0,
                    "detalle": "ERROR",
                    "comentario": "",
                    "comentarios_director": ""
                })
        
        titulo = f"Reporte Mensual - {mes:02d}/{anio}"
        
        pdf_buffer = generar_reporte_mensual(pasante_data, filas, titulo)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=reporte_mensual_{anio}_{mes}.pdf"}
        )
    except Exception as e:
        print(f"[reportes] Error generando PDF mensual: {e}")
        raise HTTPException(500, detail="Error al generar el PDF mensual.")


# ─────────────────────────────────────────────────────────────────────────
# GET /pdf/semanal — PASANTE
# ─────────────────────────────────────────────────────────────────────────
@router.get("/pdf/semanal")
def descargar_pdf_semanal(
    anio: int,
    semana: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    primer_dia = date.fromisocalendar(anio, semana, 1)   # lunes
    ultimo_dia = primer_dia + timedelta(days=4)          # <-- MODIFICADO: viernes (solo días hábiles)

    asistencias = (
        db.query(AsistenciaModel)
        .filter(
            AsistenciaModel.pasante_id == usuario_actual.id,
            AsistenciaModel.fecha >= primer_dia,
            AsistenciaModel.fecha <= ultimo_dia,
        )
        .order_by(AsistenciaModel.fecha)
        .all()
    )

    if not asistencias:
        raise HTTPException(404, detail="No hay asistencias registradas para esa semana.")

    carrera_nombre = "—"
    if hasattr(usuario_actual, "carrera") and usuario_actual.carrera:
        carrera_nombre = usuario_actual.carrera.nombre

    pasante = {
        "nombres":  usuario_actual.nombres,
        "apellidos": usuario_actual.apellidos,
        "ci":       getattr(usuario_actual, "carnet_identidad", "—"),
        "ru":       getattr(usuario_actual, "ru", "—"),
        "unidad_asignada": getattr(usuario_actual, "unidad_asignada", "—"),
        "username": usuario_actual.username,
        "carrera":  carrera_nombre,
        "proyecto": getattr(usuario_actual, "proyecto_nombre", None),
    }

    asistencias_por_fecha = {}
    for a in asistencias:
        f = a.fecha.date() if hasattr(a.fecha, "date") else a.fecha
        asistencias_por_fecha[f] = a

    filas = []
    acumulado = 0.0
    textos_semana = []
    cur = primer_dia
    
    while cur <= ultimo_dia:
        a = asistencias_por_fecha.get(cur)
        if not a:
            filas.append({
                "fecha": cur,
                "hora_entrada": None,
                "hora_salida": None,
                "horas_trabajadas": None,
                "horas_acumuladas": round(acumulado, 2),
                "detalle": "Sin asistencia",
            })
            cur = cur + timedelta(days=1)
            continue

        reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
        horas_dia = float(a.horas_trabajadas) if a.horas_trabajadas else 0.0
        acumulado = acumulado + horas_dia
        
        filas.append({
            "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
            "hora_entrada": a.hora_entrada,
            "hora_salida": a.hora_salida,
            "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas else None,
            "horas_acumuladas": round(acumulado, 2) if a.horas_trabajadas else round(acumulado, 2),
            "detalle": "Con reporte" if reporte else "Sin reporte",
        })
        
        if reporte and reporte.actividades_realizadas:
            dia_str = cur.strftime("%d/%m")
            textos_semana.append(f"• [{dia_str}]: {reporte.actividades_realizadas}")
            
        cur = cur + timedelta(days=1)

    titulo = f"Reporte semanal · Semana {semana}: {primer_dia.strftime('%d/%m')} al {ultimo_dia.strftime('%d/%m/%Y')}"
    
    texto_consolidado = "\n".join(textos_semana) if textos_semana else "No se registraron reportes de actividades en esta semana."
    
    buf = generar_reporte_semanal(pasante, filas, titulo, texto_reporte=texto_consolidado)

    nombre_archivo = (
        f"Reporte_Semanal_Sem{semana}_{anio}_"
        f"{usuario_actual.nombres.split()[0]}{usuario_actual.apellidos.split()[0]}.pdf"
    )
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'}
    )

# ─────────────────────────────────────────────────────────────────────────
# GET /pdf/mensual — PASANTE
# ─────────────────────────────────────────────────────────────────────────
@router.get("/pdf/mensual")
def descargar_pdf_mensual(
    anio: int,
    mes: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    primer_dia = date(anio, mes, 1)
    ultimo_dia = date(anio, mes, calendar.monthrange(anio, mes)[1])

    asistencias = (
        db.query(AsistenciaModel)
        .filter(
            AsistenciaModel.pasante_id == usuario_actual.id,
            AsistenciaModel.fecha >= primer_dia,
            AsistenciaModel.fecha <= ultimo_dia,
        )
        .order_by(AsistenciaModel.fecha)
        .all()
    )

    if not asistencias:
        raise HTTPException(404, detail="No hay asistencias registradas para ese mes.")

    carrera_nombre = "—"
    if hasattr(usuario_actual, "carrera") and usuario_actual.carrera:
        carrera_nombre = usuario_actual.carrera.nombre

    pasante = {
        "nombres":  usuario_actual.nombres,
        "apellidos": usuario_actual.apellidos,
        "ci":       getattr(usuario_actual, "carnet_identidad", "—"),
        "ru":       getattr(usuario_actual, "ru", "—"),
        "unidad_asignada": getattr(usuario_actual, "unidad_asignada", "—"),
        "username": usuario_actual.username,
        "carrera":  carrera_nombre,
        "proyecto": getattr(usuario_actual, "proyecto_nombre", None),
    }

    asistencias_por_fecha = {}
    for a in asistencias:
        f = a.fecha.date() if hasattr(a.fecha, "date") else a.fecha
        asistencias_por_fecha[f] = a

    filas = []
    acumulado = 0.0      # <-- NUEVO
    textos_mes = []      # <-- NUEVO
    cur = primer_dia
    
    while cur <= ultimo_dia:
        if cur.weekday() < 5:  # Solo de lunes (0) a viernes (4)
            a = asistencias_por_fecha.get(cur)
            if not a:
                filas.append({
                    "fecha": cur,
                    "hora_entrada": None,
                    "hora_salida": None,
                    "horas_trabajadas": None,
                    "horas_acumuladas": round(acumulado, 2), # <-- NUEVO
                    "detalle": "Sin asistencia",             # <-- NUEVO
                })
            else:
                reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
                horas_dia = float(a.horas_trabajadas) if a.horas_trabajadas else 0.0
                acumulado = acumulado + horas_dia
                
                filas.append({
                    "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
                    "hora_entrada": a.hora_entrada,
                    "hora_salida": a.hora_salida,
                    "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas else None,
                    "horas_acumuladas": round(acumulado, 2) if a.horas_trabajadas else round(acumulado, 2), # <-- NUEVO
                    "detalle": "Con reporte" if reporte else "Sin reporte", # <-- NUEVO
                })
                
                # <-- NUEVO: Recopilar textos
                if reporte and reporte.actividades_realizadas:
                    dia_str = cur.strftime("%d/%m")
                    textos_mes.append(f"• [{dia_str}]: {reporte.actividades_realizadas}")

        cur = cur + timedelta(days=1)

    meses_es = ["","Enero","Febrero","Marzo","Abril","Mayo","Junio",
                "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    titulo = f"{meses_es[mes]} {anio}"
    
    # <-- NUEVO: Consolidar texto
    texto_consolidado = "\n".join(textos_mes) if textos_mes else "No se registraron reportes de actividades en este mes."
    
    # <-- NUEVO: Pasar el texto_reporte a la función
    buf = generar_reporte_mensual(pasante, filas, titulo, texto_reporte=texto_consolidado)

    nombre_archivo = (
        f"Reporte_Mensual_{meses_es[mes]}{anio}_"
        f"{usuario_actual.nombres.split()[0]}{usuario_actual.apellidos.split()[0]}.pdf"
    )
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'}
    )

# ─────────────────────────────────────────────────────────────────────────
# GET /admin/pdf/semanal/{pasante_id} — ADMINISTRADOR y ENCARGADO
# ─────────────────────────────────────────────────────────────────────────
@router.get("/admin/pdf/semanal/{pasante_id}")
def admin_descargar_pdf_semanal(
    pasante_id: int,
    anio: int,
    semana: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    pasante_db = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante_db:
        raise HTTPException(404, detail="Pasante no encontrado.")

    primer_dia = date.fromisocalendar(anio, semana, 1)   # lunes
    ultimo_dia = primer_dia + timedelta(days=4)          # viernes (solo días hábiles)

    asistencias = (
        db.query(AsistenciaModel)
        .filter(
            AsistenciaModel.pasante_id == pasante_db.id,
            AsistenciaModel.fecha >= primer_dia,
            AsistenciaModel.fecha <= ultimo_dia,
        )
        .order_by(AsistenciaModel.fecha)
        .all()
    )

    carrera_nombre = pasante_db.carrera.nombre if hasattr(pasante_db, "carrera") and pasante_db.carrera else "—"

    pasante_data = {
        "nombres":  pasante_db.nombres,
        "apellidos": pasante_db.apellidos,
        "ci":       getattr(pasante_db, "carnet_identidad", "—"),
        "ru":       getattr(pasante_db, "ru", "—"),
        "unidad_asignada": getattr(pasante_db, "unidad_asignada", "—"),
        "username": pasante_db.username,
        "carrera":  carrera_nombre,
        "proyecto": getattr(pasante_db, "proyecto_nombre", None),
    }

    asistencias_por_fecha = {}
    for a in asistencias:
        f = a.fecha.date() if hasattr(a.fecha, "date") else a.fecha
        asistencias_por_fecha[f] = a

    filas = []
    acumulado = 0.0
    textos_semana = []
    cur = primer_dia
    
    while cur <= ultimo_dia:
        a = asistencias_por_fecha.get(cur)
        if not a:
            filas.append({
                "fecha": cur,
                "hora_entrada": "—",
                "hora_salida": "—",
                "horas_trabajadas": "—",
                "horas_acumuladas": round(acumulado, 2),
                "estado_admin": "Sin asistencia",
                "estado_encargado": "",
                "detalle": "Sin asistencia",
            })
            cur = cur + timedelta(days=1)
            continue

        reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
        horas_dia = float(a.horas_trabajadas) if a.horas_trabajadas else 0.0
        acumulado = acumulado + horas_dia
        
        # Convertir tiempo a string
        hora_entrada_str = a.hora_entrada.strftime("%H:%M") if a.hora_entrada else "—"
        hora_salida_str = a.hora_salida.strftime("%H:%M") if a.hora_salida else "—"
        horas_str = f"{horas_dia:.2f}" if horas_dia > 0 else "—"
        
        # Determinar estados
        estado_admin = reporte.estado_admin if reporte else ""
        estado_encargado = reporte.estado_encargado if reporte else ""
        detalle = "Con reporte" if reporte else "Sin reporte"
        
        filas.append({
            "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
            "hora_entrada": hora_entrada_str,
            "hora_salida": hora_salida_str,
            "horas_trabajadas": horas_str,
            "horas_acumuladas": round(acumulado, 2),
            "estado_admin": estado_admin,
            "estado_encargado": estado_encargado,
            "detalle": detalle,
            "comentarios_director": reporte.comentarios_director if reporte else "",
            "actividades": reporte.actividades_realizadas if reporte else ""
        })
        
        if reporte and reporte.actividades_realizadas:
            dia_str = cur.strftime("%d/%m")
            textos_semana.append(f"• [{dia_str}]: {reporte.actividades_realizadas}")
            
        cur = cur + timedelta(days=1)

    titulo = f"Reporte semanal · Semana {semana}: {primer_dia.strftime('%d/%m')} al {ultimo_dia.strftime('%d/%m/%Y')}"
    texto_consolidado = "\n".join(textos_semana) if textos_semana else "No se registraron reportes de actividades en esta semana."
    
    buf = generar_reporte_semanal(pasante_data, filas, titulo, texto_reporte=texto_consolidado)

    nombre_archivo = f"Reporte_Semanal_Sem{semana}_{anio}_{pasante_data['nombres'].split()[0]}.pdf"
    
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'}
    )


# ─────────────────────────────────────────────────────────────────────────
# GET /admin/pdf/mensual/{pasante_id} — ADMINISTRADOR y ENCARGADO
# ─────────────────────────────────────────────────────────────────────────
@router.get("/admin/pdf/mensual/{pasante_id}")
def admin_descargar_pdf_mensual(
    pasante_id: int,
    anio: int,
    mes: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    pasante_db = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante_db:
        raise HTTPException(404, detail="Pasante no encontrado.")

    primer_dia = date(anio, mes, 1)
    ultimo_dia = date(anio, mes, calendar.monthrange(anio, mes)[1])

    asistencias = (
        db.query(AsistenciaModel)
        .filter(
            AsistenciaModel.pasante_id == pasante_db.id,
            AsistenciaModel.fecha >= primer_dia,
            AsistenciaModel.fecha <= ultimo_dia,
        )
        .order_by(AsistenciaModel.fecha)
        .all()
    )

    carrera_nombre = pasante_db.carrera.nombre if hasattr(pasante_db, "carrera") and pasante_db.carrera else "—"

    pasante_data = {
        "nombres":  pasante_db.nombres,
        "apellidos": pasante_db.apellidos,
        "ci":       getattr(pasante_db, "carnet_identidad", "—"),
        "ru":       getattr(pasante_db, "ru", "—"),
        "unidad_asignada": getattr(pasante_db, "unidad_asignada", "—"),
        "username": pasante_db.username,
        "carrera":  carrera_nombre,
        "proyecto": getattr(pasante_db, "proyecto_nombre", None),
    }

    asistencias_por_fecha = {}
    for a in asistencias:
        f = a.fecha.date() if hasattr(a.fecha, "date") else a.fecha
        asistencias_por_fecha[f] = a

    filas = []
    acumulado = 0.0
    textos_mes = []
    cur = primer_dia
    
    while cur <= ultimo_dia:
        if cur.weekday() < 5:  # Lunes a Viernes
            a = asistencias_por_fecha.get(cur)
            if not a:
                filas.append({
                    "fecha": cur,
                    "hora_entrada": "—",
                    "hora_salida": "—",
                    "horas_trabajadas": "—",
                    "horas_acumuladas": round(acumulado, 2),
                    "estado_admin": "Sin asistencia",
                    "estado_encargado": "",
                    "detalle": "Sin asistencia",
                })
            else:
                reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
                horas_dia = float(a.horas_trabajadas) if a.horas_trabajadas else 0.0
                acumulado = acumulado + horas_dia
                
                # Convertir tiempo a string
                hora_entrada_str = a.hora_entrada.strftime("%H:%M") if a.hora_entrada else "—"
                hora_salida_str = a.hora_salida.strftime("%H:%M") if a.hora_salida else "—"
                horas_str = f"{horas_dia:.2f}" if horas_dia > 0 else "—"
                
                # Determinar estados
                estado_admin = reporte.estado_admin if reporte else ""
                estado_encargado = reporte.estado_encargado if reporte else ""
                detalle = "Con reporte" if reporte else "Sin reporte"
                
                filas.append({
                    "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
                    "hora_entrada": hora_entrada_str,
                    "hora_salida": hora_salida_str,
                    "horas_trabajadas": horas_str,
                    "horas_acumuladas": round(acumulado, 2),
                    "estado_admin": estado_admin,
                    "estado_encargado": estado_encargado,
                    "detalle": detalle,
                    "comentarios_director": reporte.comentarios_director if reporte else "",
                    "actividades": reporte.actividades_realizadas if reporte else ""
                })
                
                if reporte and reporte.actividades_realizadas:
                    dia_str = cur.strftime("%d/%m")
                    textos_mes.append(f"• [{dia_str}]: {reporte.actividades_realizadas}")

        cur = cur + timedelta(days=1)

    meses_es = ["","Enero","Febrero","Marzo","Abril","Mayo","Junio",
                "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    titulo = f"{meses_es[mes]} {anio}"
    texto_consolidado = "\n".join(textos_mes) if textos_mes else "No se registraron reportes de actividades en este mes."
    
    buf = generar_reporte_mensual(pasante_data, filas, titulo, texto_reporte=texto_consolidado)

    nombre_archivo = f"Reporte_Mensual_{meses_es[mes]}{anio}_{pasante_data['nombres'].split()[0]}.pdf"
    
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'}
    )