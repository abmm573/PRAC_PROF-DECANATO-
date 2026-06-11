from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import io
from datetime import date, timedelta

from app.db.database import get_db
from app.schemas.asistencia_schema import (
    AsistenciaCreate, AsistenciaResponse, AsistenciaUpdate,
    FichajePublicoEntrada, FichajePublicoSalida,
)
from app.crud import crud_asistencia
from app.utils.geofencing import validar_ubicacion
from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.models.usuario import Usuario
from app.models.asistencia import Asistencia, Reporte
from app.utils.pasantia_completion import check_and_notify_completion, check_and_notify_near_completion

router = APIRouter()

LAT_FACULTAD = -16.5048
LON_FACULTAD = -68.1299
RADIO_METROS = 500


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /publico/entrada  â€”  sin token, solo username
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.post("/publico/entrada")
def fichaje_publico_entrada(datos: FichajePublicoEntrada, db: Session = Depends(get_db)):
    print(f"[asistencias] Intentando registrar entrada para: {datos.username}")
    
    try:
        pasante = db.query(Usuario).filter(
            Usuario.username == datos.username.strip().lower()
        ).first()

        if not pasante:
            print(f"[asistencias] Username no encontrado: {datos.username}")
            raise HTTPException(404, detail="Username no encontrado. Verifica tus datos.")

        print(f"[asistencias] Pasante encontrado: {pasante.nombres} {pasante.apellidos}")
        
        nombre_rol = getattr(pasante.rol, "nombre", "")
        print(f"[asistencias] Rol del pasante: {nombre_rol}")
        
        if nombre_rol != "PASANTE":
            print(f"[asistencias] Rol no válido: {nombre_rol}")
            raise HTTPException(
                403,
                detail=f"Esta pantalla es solo para Pasantes. Tu rol es: {nombre_rol}."
            )

        if not pasante.estado:
            print(f"[asistencias] Cuenta desactivada")
            raise HTTPException(403, detail="Tu cuenta estÃ¡ desactivada. Contacta al encargado.")

        print(f"[asistencias] Llamando a crud_asistencia.crear_entrada_por_pasante_id")
        nuevo = crud_asistencia.crear_entrada_por_pasante_id(db=db, pasante_id=pasante.id)
        
        if not nuevo:
            print(f"[asistencias] Ya existe entrada para hoy")
            raise HTTPException(400, detail="Ya tienes registrada una entrada para el dÃ­a de hoy.")

        print(f"[asistencias] Entrada registrada exitosamente: ID {nuevo.id}")
        return {
            "mensaje":       f"Â¡Buen dÃ­a, {pasante.nombres}! Entrada registrada.",
            "nombre":        pasante.nombres,
            "hora_entrada":  nuevo.hora_entrada.strftime("%H:%M:%S"),
            "fecha":         str(nuevo.fecha),
            "asistencia_id": nuevo.id,
        }
    except HTTPException as http_exc:
        # Dejar pasar las HTTPException sin modificar
        print(f"[asistencias] Error HTTP: {http_exc.status_code} - {http_exc.detail}")
        raise http_exc
    except Exception as e:
        # Solo capturar errores no HTTP
        print(f"[asistencias] Error inesperado en registro de entrada: {e}")
        raise HTTPException(500, detail="Error al registrar entrada. Contacte al administrador.")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /publico/salida  â€”  sin token, solo username
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.post("/publico/salida")
def fichaje_publico_salida(datos: FichajePublicoSalida, db: Session = Depends(get_db)):
    pasante = db.query(Usuario).filter(
        Usuario.username == datos.username.strip().lower()
    ).first()

    if not pasante:
        raise HTTPException(404, detail="Username no encontrado. Verifica tus datos.")

    nombre_rol = getattr(pasante.rol, "nombre", "")
    if nombre_rol != "PASANTE":
        raise HTTPException(
            403,
            detail=f"Esta pantalla es solo para Pasantes. Tu rol es: {nombre_rol}."
        )

    if not pasante.estado:
        raise HTTPException(403, detail="Tu cuenta estÃ¡ desactivada. Contacta al encargado.")

    registro, estado = crud_asistencia.registrar_salida_por_pasante_id(
        db=db, pasante_id=pasante.id
    )

    if estado == "no_entrada":
        raise HTTPException(400, detail="No tienes entrada registrada hoy. Ficha tu entrada primero.")
    if estado == "ya_salio":
        raise HTTPException(400, detail="Ya registraste tu salida de hoy.")

    # Notificar si está cerca de completar (faltan ≤20 horas)
    try:
        total_horas, esta_cerca, notificado_cerca = check_and_notify_near_completion(db, pasante.id, horas_faltantes_threshold=20)
    except Exception as e:
        print(f"[asistencias] Error en notificación de cercano: {e}")
        total_horas, esta_cerca, notificado_cerca = 0, False, False

    # Notificar al encargado si el pasante completó 240h (async para no bloquear)
    try:
        total_horas, cumplio, _notificado = check_and_notify_completion(db, pasante.id)
    except Exception as e:
        print(f"[asistencias] Error en notificación de completado: {e}")
        # Si falla la notificación, continuamos con el registro
        total_horas = 0
        cumplio = False


    return {
        "mensaje":          f"¡Hasta luego, {pasante.nombres}! Salida registrada.",
        "nombre":           pasante.nombres,
        "hora_entrada":     registro.hora_entrada.strftime("%H:%M:%S"),
        "hora_salida":      registro.hora_salida.strftime("%H:%M:%S"),
        "horas_trabajadas": float(registro.horas_trabajadas),
        "asistencia_id":    registro.id,
        "total_horas_acumuladas": float(total_horas),
        "cumplio_pasantia": bool(cumplio),
        "notificacion_enviada": bool(_notificado),
        "esta_cerca_completar": bool(esta_cerca),
        "notificacion_cercano_enviada": bool(notificado_cerca),
    }


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /entrada  â€”  pasante logueado, con GPS opcional
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.post("/entrada", response_model=AsistenciaResponse, status_code=status.HTTP_201_CREATED)
def marcar_entrada(
    asistencia: AsistenciaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    esta_en_facultad = False
    if asistencia.latitud_entrada and asistencia.longitud_entrada:
        esta_en_facultad = validar_ubicacion(
            lat_pasante=asistencia.latitud_entrada,
            lon_pasante=asistencia.longitud_entrada,
            lat_facultad=LAT_FACULTAD,
            lon_facultad=LON_FACULTAD,
            radio_permitido=RADIO_METROS
        )

    nuevo = crud_asistencia.crear_entrada(db=db, asistencia_data=asistencia)
    if not nuevo:
        raise HTTPException(400, detail="El pasante ya tiene un registro de entrada para el dÃ­a de hoy.")

    mensaje = (
        "Asistencia registrada correctamente dentro de la Facultad."
        if esta_en_facultad
        else " Asistencia registrada, pero tu GPS indica que NO estabas en la Facultad."
    )

    return {
        "id": nuevo.id, "pasante_id": nuevo.pasante_id,
        "fecha": nuevo.fecha, "hora_entrada": nuevo.hora_entrada,
        "hora_salida": nuevo.hora_salida, "horas_trabajadas": nuevo.horas_trabajadas,
        "esta_en_facultad": esta_en_facultad, "mensaje_alerta": mensaje,
    }


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# PUT /salida/{asistencia_id}  â€”  pasante logueado
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.put("/salida/{asistencia_id}", response_model=AsistenciaResponse)
def marcar_salida(
    asistencia_id: int,
    datos_salida: AsistenciaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    registro = crud_asistencia.registrar_salida(
        db=db, asistencia_id=asistencia_id, datos_salida=datos_salida
    )
    if not registro:
        raise HTTPException(404, detail="Registro no encontrado o salida ya marcada.")
    # Notificar si está cerca de completar (faltan 20 horas o menos)
    check_and_notify_near_completion(db, registro.pasante_id, horas_faltantes_threshold=20)
    # Notificar al encargado si el pasante completó su meta de horas
    check_and_notify_completion(db, registro.pasante_id)

    return registro


# AÃ‘ADIDOâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /mis-asistencias  â€”  historial del pasante con reporte incluido
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
from typing import Optional
from datetime import date, timedelta

@router.get("/mis-asistencias")
def mis_asistencias(
    pasante_id: Optional[int] = None,
    mes: Optional[int] = None,
    anio: Optional[int] = None,
    semana: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Devuelve el historial de asistencias con filtros opcionales.

    - Si el usuario es pasante retorna sus propias asistencias.
    - Si se proporciona *pasante_id* y el usuario tiene rol de encargado/admin
      permite ver el historial de aquel pasante.
    
    Filtros opcionales:
      - mes: 1-12 (requiere anio)
      - anio: año (ej. 2026)
      - semana: número de semana ISO (requiere anio)
    """

    # si solicitan otro id, sÃ³lo lo permitimos para roles 1 (admin) o 2 (encargado)
    if pasante_id is not None and usuario_actual.rol_id not in (1, 2):
        raise HTTPException(403, detail="No autorizado para ver ese historial.")
    # Si es ENCARGADO, solo puede ver asistencias de PASANTES de su misma carrera
    if pasante_id is not None and usuario_actual.rol_id == 2:
        objetivo = db.query(Usuario).filter(Usuario.id == pasante_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Pasante no encontrado.")
        rol_objetivo = getattr(objetivo.rol, "nombre", "")
        if rol_objetivo != "PASANTE" or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes ver asistencias de pasantes de tu carrera.")


    target_id = pasante_id or usuario_actual.id
    
    # Construir consulta con filtros
    query = db.query(Asistencia).filter(Asistencia.pasante_id == target_id)
    
    # Filtro por mes y año
    if mes is not None and anio is not None:
        try:
            mes = int(mes)
            anio = int(anio)
            if not (1 <= mes <= 12):
                raise HTTPException(400, detail="Mes debe estar entre 1 y 12")
            # Primera y última fecha del mes
            fecha_inicio = date(anio, mes, 1)
            if mes == 12:
                fecha_fin = date(anio + 1, 1, 1) - timedelta(days=1)
            else:
                fecha_fin = date(anio, mes + 1, 1) - timedelta(days=1)
            query = query.filter(Asistencia.fecha >= fecha_inicio, Asistencia.fecha <= fecha_fin)
        except (ValueError, TypeError):
            raise HTTPException(400, detail="mes y anio deben ser números válidos")
    
    # Filtro por semana ISO y año
    elif semana is not None and anio is not None:
        try:
            semana = int(semana)
            anio = int(anio)
            # Calcular primer y último día de la semana ISO
            # La semana ISO comienza el lunes (1) y termina el domingo (7)
            primera_fecha = date(anio, 1, 4)  # Una fecha en la semana 1
            inicio_año = primera_fecha - timedelta(days=primera_fecha.isoweekday() - 1)
            inicio_semana = inicio_año + timedelta(weeks=semana - 1)
            fin_semana = inicio_semana + timedelta(days=6)
            query = query.filter(Asistencia.fecha >= inicio_semana, Asistencia.fecha <= fin_semana)
        except (ValueError, TypeError):
            raise HTTPException(400, detail="semana y anio deben ser números válidos")
    
    asistencias = query.order_by(Asistencia.fecha.asc()).all()
    
    resultado = []
    for a in asistencias:
        reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
        resultado.append({
            "id":               a.id,
            "pasante_id":       a.pasante_id,
            "fecha":            a.fecha,
            "hora_entrada":     a.hora_entrada,
            "hora_salida":      a.hora_salida,
            "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas else None,
            "reporte": {
                "id":                     reporte.id,
                "actividades_realizadas": reporte.actividades_realizadas,
                "estado_admin":            reporte.estado_admin,
                "estado_encargado":        reporte.estado_encargado,
                "comentarios_director":   reporte.comentarios_director,
                "creado_en":              reporte.creado_en,
            } if reporte else None,
        })
    return resultado
# GET /reporte-pdf — descarga PDF por día/semana/mes
@router.get("/reporte-pdf")
def descargar_reporte_periodo_pdf(
    tipo: str,
    fecha: str,
    pasante_id: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE", "ENCARGADO", "ADMINISTRADOR"]))
):
    """Descarga un PDF de asistencias+reportes por día/semana/mes.

    Query params:
      - tipo: dia | semana | mes
      - fecha: YYYY-MM-DD (para mes también sirve, toma el mes de esa fecha)
      - pasante_id (opcional): solo ADMIN/ENCARGADO
    """
    from datetime import date, timedelta
    from fastapi.responses import StreamingResponse
    from sqlalchemy.orm import joinedload

    from app.models.asistencia import Asistencia
    from app.utils.generador_reporte_pdf import (
        generar_reporte_diario,
        generar_reporte_semanal,
        generar_reporte_mensual,
    )

    tipo = (tipo or '').strip().lower()
    if tipo not in ('dia', 'semana', 'mes'):
        raise HTTPException(400, detail="tipo inválido. Usa: dia, semana, mes")

    try:
        base_date = date.fromisoformat(str(fecha))
    except Exception:
        raise HTTPException(400, detail="fecha inválida. Usa formato YYYY-MM-DD")

    # Resolver objetivo según rol
    if pasante_id is not None and usuario_actual.rol_id not in (1, 2):
        raise HTTPException(403, detail="No autorizado para descargar ese reporte.")

    target_id = pasante_id or usuario_actual.id

    # Validación ENCARGADO: solo pasantes de su carrera
    if pasante_id is not None and usuario_actual.rol_id == 2:
        objetivo = db.query(Usuario).filter(Usuario.id == pasante_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Pasante no encontrado.")
        rol_objetivo = getattr(objetivo.rol, 'nombre', '')
        if rol_objetivo != 'PASANTE' or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes descargar reportes de pasantes de tu carrera.")

    pasante = db.query(Usuario).filter(Usuario.id == target_id).first()
    if not pasante:
        raise HTTPException(404, detail="Pasante no encontrado.")

    # Rango y título
    if tipo == 'dia':
        start = base_date
        end = base_date
        titulo = f"Reporte diario · {base_date.strftime('%d/%m/%Y')}"
        filename = f"reporte_diario_{pasante.username}_{base_date.isoformat()}.pdf"
    elif tipo == 'semana':
        start = base_date - timedelta(days=base_date.weekday())
        end = start + timedelta(days=6)
        titulo = f"Reporte semanal · {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}"
        filename = f"reporte_semanal_{pasante.username}_{start.isoformat()}.pdf"
    else:
        start = date(base_date.year, base_date.month, 1)
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(days=1)
        titulo = f"Reporte mensual · {start.strftime('%m/%Y')}"
        filename = f"reporte_mensual_{pasante.username}_{start.strftime('%Y-%m')}.pdf"

    asistencias = (
        db.query(Asistencia)
        .options(joinedload(Asistencia.reporte))
        .filter(Asistencia.pasante_id == pasante.id)
        .filter(Asistencia.fecha >= start)
        .filter(Asistencia.fecha <= end)
        .order_by(Asistencia.fecha.asc())
        .all()
    )

    # PASANTE: solo puede descargar si TODO el periodo está APROBADO por admin
    # (si falta reporte o está PENDIENTE/RECHAZADO, se bloquea).
    if usuario_actual.rol_id == 3:
        for a in asistencias:
            rep = getattr(a, 'reporte', None)
            if not rep or (rep.estado_admin or '').upper() != 'APROBADO':
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    detail='Solo puedes descargar el PDF cuando todos los reportes del periodo estén APROBADOS por el administrador.',
                )


    asistencias_por_fecha = {}
    for a in asistencias:
        f = a.fecha.date() if hasattr(a.fecha, "date") else a.fecha
        asistencias_por_fecha[f] = a

    filas = []
    if tipo == "semana":
        acumulado = 0.0
        cur = start
        while cur <= end:
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

            rep = getattr(a, "reporte", None)
            horas_dia = float(a.horas_trabajadas) if a.horas_trabajadas is not None else 0.0
            acumulado = acumulado + horas_dia

            detalle = "Sin reporte"
            if rep and rep.actividades_realizadas:
                detalle = rep.actividades_realizadas
            elif rep:
                detalle = "Con reporte"

            filas.append({
                "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
                "hora_entrada": a.hora_entrada,
                "hora_salida": a.hora_salida,
                "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas is not None else None,
                "horas_acumuladas": round(acumulado, 2),
                "detalle": detalle,
            })
            cur = cur + timedelta(days=1)
    elif tipo == "mes":
        cur = start
        while cur <= end:
            a = asistencias_por_fecha.get(cur)
            if not a:
                filas.append({
                    "fecha": cur,
                    "hora_entrada": None,
                    "hora_salida": None,
                    "horas_trabajadas": None,
                    "actividades": "Sin asistencia",
                    "estado": "SIN ASISTENCIA",
                })
                cur = cur + timedelta(days=1)
                continue

            rep = getattr(a, "reporte", None)
            filas.append({
                "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
                "hora_entrada": a.hora_entrada,
                "hora_salida": a.hora_salida,
                "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas is not None else None,
                "actividades": rep.actividades_realizadas if rep else None,
                "estado": rep.estado_admin or rep.estado_encargado or "PENDIENTE",
            })
            cur = cur + timedelta(days=1)
    else:
        for a in asistencias:
            rep = getattr(a, "reporte", None)
            filas.append({
                "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
                "hora_entrada": a.hora_entrada,
                "hora_salida": a.hora_salida,
                "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas is not None else None,
                "actividades": rep.actividades_realizadas if rep else None,
                "estado": rep.estado_admin or rep.estado_encargado or "PENDIENTE",
            })

    carrera_nombre = getattr(getattr(pasante, 'carrera', None), 'nombre', None)
    pasante_info = {
        'nombres': pasante.nombres,
        'apellidos': pasante.apellidos,
        'ci': pasante.carnet_identidad,
        'proyecto': getattr(pasante, 'proyecto_nombre', None),
        'carrera': carrera_nombre or (str(pasante.carrera_id) if pasante.carrera_id is not None else '—'),
    }

    if tipo == 'mes':
        buf = generar_reporte_mensual(pasante_info, filas, titulo)
    elif tipo == 'dia':
        buf = generar_reporte_diario(pasante_info, filas, titulo)
    else:
        buf = generar_reporte_semanal(pasante_info, filas, titulo)

    return StreamingResponse(
        buf,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename={filename}'},
    )

# GET /reporte-pdf/pasante — endpoint específico para ENCARGADO que descarga PDF como el PasanteReportePdf.vue
@router.get("/reporte-pdf/pasante")
def descargar_pdf_pasante_como_encargado(
    tipo: str,
    fecha: str,
    pasante_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ENCARGADO", "ADMINISTRADOR"]))
):
    """Descarga PDF de pasante usando el mismo formato que PasanteReportePdf.vue.
    
    Solo para ENCARGADO y ADMINISTRADOR.
    """
    from datetime import date, timedelta
    from fastapi.responses import StreamingResponse
    from sqlalchemy.orm import joinedload
    
    from app.models.asistencia import Asistencia
    from app.models.usuario import Usuario
    from app.utils.generador_reporte_pdf import (
        generar_reporte_diario,
        generar_reporte_semanal,
        generar_reporte_mensual,
    )
    
    # Validar parámetros
    tipo = (tipo or '').strip().lower()
    if tipo not in ('dia', 'semana', 'mes'):
        raise HTTPException(400, detail="tipo inválido. Usa: dia, semana, mes")
    
    try:
        base_date = date.fromisoformat(str(fecha))
    except Exception:
        raise HTTPException(400, detail="fecha inválida. Usa formato YYYY-MM-DD")
    
    # Validar permisos para ENCARGADO
    if usuario_actual.rol_id == 2:  # ENCARGADO
        objetivo = db.query(Usuario).filter(Usuario.id == pasante_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Pasante no encontrado.")
        if objetivo.rol.nombre != 'PASANTE' or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes descargar reportes de pasantes de tu carrera.")
    
    # Obtener datos del pasante
    pasante = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante:
        raise HTTPException(404, detail="Pasante no encontrado.")
    
    # Preparar datos del pasante en formato UMSA
    pasante_info = {
        'nombres': pasante.nombres,
        'apellidos': pasante.apellidos,
        'carnet_identidad': pasante.carnet_identidad,
        'ru': pasante.ru,
        'unidad_asignada': pasante.unidad_asignada,
        'carrera': getattr(pasante.carrera, 'nombre', '—') if pasante.carrera else '—',
        'username': pasante.username,
    }
    
    # Determinar rango de fechas
    if tipo == 'dia':
        start = base_date
        end = base_date
        titulo = f"Reporte Diario - {base_date.strftime('%d/%m/%Y')}"
        filename = f"reporte_diario_{pasante.username}_{base_date.isoformat()}.pdf"
    elif tipo == 'semana':
        start = base_date - timedelta(days=base_date.weekday())
        end = start + timedelta(days=4)  # Lunes a Viernes
        titulo = f"Reporte Semanal - {start.strftime('%d/%m/%Y')} al {end.strftime('%d/%m/%Y')}"
        filename = f"reporte_semanal_{pasante.username}_{start.isoformat()}.pdf"
    else:  # mes
        start = date(base_date.year, base_date.month, 1)
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(days=1)
        titulo = f"Reporte Mensual - {start.strftime('%m/%Y')}"
        filename = f"reporte_mensual_{pasante.username}_{start.strftime('%Y-%m')}.pdf"
    
    # Obtener asistencias
    asistencias = (
        db.query(Asistencia)
        .options(joinedload(Asistencia.reporte))
        .filter(Asistencia.pasante_id == pasante_id)
        .filter(Asistencia.fecha >= start)
        .filter(Asistencia.fecha <= end)
        .order_by(Asistencia.fecha.asc())
        .all()
    )
    
    # Preparar filas para el PDF
    filas = []
    asistencias_por_fecha = {}
    for a in asistencias:
        f = a.fecha.date() if hasattr(a.fecha, "date") else a.fecha
        asistencias_por_fecha[f] = a
    
    if tipo == "semana":
        cur = start
        while cur <= end:
            a = asistencias_por_fecha.get(cur)
            if not a:
                filas.append({
                    "fecha": cur,
                    "hora_entrada": None,
                    "hora_salida": None,
                    "horas_trabajadas": None,
                    "actividades": "Sin asistencia",
                    "estado": "SIN ASISTENCIA",
                })
            else:
                rep = getattr(a, "reporte", None)
                filas.append({
                    "fecha": cur,
                    "hora_entrada": a.hora_entrada,
                    "hora_salida": a.hora_salida,
                    "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas is not None else None,
                    "actividades": rep.actividades_realizadas if rep else None,
                    "estado": rep.estado_admin or rep.estado_encargado or "PENDIENTE",
                })
            cur = cur + timedelta(days=1)
    elif tipo == "mes":
        cur = start
        while cur <= end:
            a = asistencias_por_fecha.get(cur)
            if not a:
                filas.append({
                    "fecha": cur,
                    "hora_entrada": None,
                    "hora_salida": None,
                    "horas_trabajadas": None,
                    "actividades": "Sin asistencia",
                    "estado": "SIN ASISTENCIA",
                })
            else:
                rep = getattr(a, "reporte", None)
                filas.append({
                    "fecha": cur,
                    "hora_entrada": a.hora_entrada,
                    "hora_salida": a.hora_salida,
                    "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas is not None else None,
                    "actividades": rep.actividades_realizadas if rep else None,
                    "estado": rep.estado_admin or rep.estado_encargado or "PENDIENTE",
                })
            cur = cur + timedelta(days=1)
    else:  # dia
        for a in asistencias:
            rep = getattr(a, "reporte", None)
            filas.append({
                "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
                "hora_entrada": a.hora_entrada,
                "hora_salida": a.hora_salida,
                "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas is not None else None,
                "actividades": rep.actividades_realizadas if rep else None,
                "estado": rep.estado_admin or rep.estado_encargado or "PENDIENTE",
            })
    
    # Generar PDF
    try:
        if tipo == 'mes':
            buf = generar_reporte_mensual(pasante_info, filas, titulo)
        elif tipo == 'dia':
            buf = generar_reporte_diario(pasante_info, filas, titulo)
        else:  # semana
            # Calcular año y semana para el reporte semanal
            from datetime import timedelta
            dia_sem = base_date.weekday()  # 0=lunes, 6=domingo
            lunes = base_date - timedelta(days=dia_sem)
            
            # Calcular número de semana ISO usando método estándar
            semana_num = base_date.isocalendar()[1]
            
            buf = generar_reporte_semanal(pasante_info, filas, titulo, anio=base_date.year, semana=semana_num)
    except Exception as e:
        print(f"[ERROR] Error generando PDF: {str(e)}")
        print(f"[ERROR] pasante_info: {pasante_info}")
        print(f"[ERROR] filas: {filas}")
        print(f"[ERROR] titulo: {titulo}")
        raise HTTPException(500, detail=f"Error generando PDF: {str(e)}")
    
    return StreamingResponse(
        buf,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename={filename}'},
    )


# GET /descargar-pdf-historial ? descarga PDF completo del historial de un pasante
@router.get("/descargar-pdf-historial")
def descargar_pdf_historial_completo(
    pasante_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    """Descarga un PDF con el historial completo de asistencias de un pasante.
    
    Solo disponible para ADMINISTRADOR y ENCARGADO.
    """
    from datetime import date
    from fastapi.responses import StreamingResponse
    from sqlalchemy.orm import joinedload

    from app.models.asistencia import Asistencia
    from app.utils.generador_reporte_pdf import generar_reporte_historial_completo

    # Validar que el pasante exista
    pasante = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante:
        raise HTTPException(404, detail="Pasante no encontrado.")
    
    # Validar que sea un pasante
    if pasante.rol.nombre != 'PASANTE':
        raise HTTPException(400, detail="El usuario especificado no es un pasante.")
    
    # Validar permisos del ENCARGADO
    if usuario_actual.rol.nombre == 'ENCARGADO':
        if pasante.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes descargar historiales de pasantes de tu carrera.")
    
    # Obtener todas las asistencias del pasante
    asistencias = (
        db.query(Asistencia)
        .options(joinedload(Asistencia.reporte))
        .filter(Asistencia.pasante_id == pasante.id)
        .order_by(Asistencia.fecha.desc())
        .all()
    )
    
    if not asistencias:
        raise HTTPException(404, detail="El pasante no tiene registros de asistencia.")
    
    # Preparar datos para el PDF
    filas = []
    for a in asistencias:
        rep = getattr(a, "reporte", None)
        filas.append({
            "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
            "hora_entrada": a.hora_entrada,
            "hora_salida": a.hora_salida,
            "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas is not None else None,
            "actividades": rep.actividades_realizadas if rep else None,
            "estado": rep.estado_admin or rep.estado_encargado or "PENDIENTE",
            "comentarios_director": rep.comentarios_director if rep else None,
        })
    
    # Información del pasante
    carrera_nombre = getattr(getattr(pasante, 'carrera', None), 'nombre', None)
    pasante_info = {
        'nombres': pasante.nombres,
        'apellidos': pasante.apellidos,
        'ci': pasante.carnet_identidad,
        'username': pasante.username,
        'email': pasante.email,
        'carrera': carrera_nombre or (str(pasante.carrera_id) if pasante.carrera_id is not None else '—'),
        'total_asistencias': len(asistencias),
        'fecha_generacion': date.today().strftime('%d/%m/%Y')
    }
    
    # Generar título y nombre de archivo
    titulo = f"Historial Completo de Asistencias · {pasante.nombres} {pasante.apellidos}"
    filename = f"historial_completo_{pasante.username}_{date.today().isoformat()}.pdf"
    
    # Generar PDF
    try:
        buf = generar_reporte_historial_completo(pasante_info, filas, titulo)
    except Exception as e:
        print(f"Error generando PDF: {e}")
        raise HTTPException(500, detail="Error al generar el PDF. Contacta al administrador.")
    
    # Configurar headers para CORS
    headers = {
        'Content-Disposition': f'attachment; filename={filename}',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': '*'
    }
    
    return StreamingResponse(
        buf,
        media_type='application/pdf',
        headers=headers
    )


# GET /resumen-horas ? resumen de horas por pasante (Encargado/Admin)
@router.get("/resumen-horas")
def resumen_horas_pasantes(
    tipo: str = "semana",
    fecha: Optional[str] = None,
    carrera_id: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    """Resumen de horas trabajadas por pasante.

    - ENCARGADO: solo su carrera (usa su carrera_id)
    - ADMIN: puede enviar carrera_id (opcional). Si no env?a, devuelve todas.
    - PASANTE: solo su propio resumen (ignora carrera_id)

    Query params:
      - tipo: dia | semana | mes | total
      - fecha: YYYY-MM-DD (opcional; si no se manda usa hoy)
      - carrera_id: solo ADMIN (opcional)
    """
    from datetime import date, datetime, time, timedelta

    from sqlalchemy import case, func

    from app.models.asistencia import Asistencia

    tipo = (tipo or "").strip().lower()
    if tipo not in ("dia", "semana", "mes", "total"):
        raise HTTPException(400, detail="tipo inv?lido. Usa: dia, semana, mes, total")

    base_date = date.today()
    if fecha:
        try:
            base_date = date.fromisoformat(str(fecha))
        except Exception:
            raise HTTPException(400, detail="fecha inv?lida. Usa formato YYYY-MM-DD")

    # Permisos / alcance
    if usuario_actual.rol_id == 2:
        if usuario_actual.carrera_id is None:
            raise HTTPException(400, detail="Tu usuario no tiene carrera asignada. Contacta al administrador.")
        carrera_filtro = usuario_actual.carrera_id
        pasante_unico = None
    elif usuario_actual.rol_id == 1:
        carrera_filtro = carrera_id
        pasante_unico = None
    elif usuario_actual.rol_id == 3:
        carrera_filtro = None
        pasante_unico = usuario_actual.id
    else:
        raise HTTPException(403, detail="No autorizado.")

    # Rango
    start_dt = None
    end_dt = None
    if tipo == "dia":
        start = base_date
        end = base_date
    elif tipo == "semana":
        start = base_date - timedelta(days=base_date.weekday())
        end = start + timedelta(days=6)
    elif tipo == "mes":
        start = date(base_date.year, base_date.month, 1)
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(days=1)
    else:
        start = None
        end = None

    if start is not None and end is not None:
        start_dt = datetime.combine(start, time.min)
        end_dt = datetime.combine(end + timedelta(days=1), time.min)

    # Query agregada
    q = (
        db.query(
            Usuario.id.label("pasante_id"),
            Usuario.nombres.label("nombres"),
            Usuario.apellidos.label("apellidos"),
            Usuario.username.label("username"),
            func.count(Asistencia.id).label("registros"),
            func.coalesce(func.sum(Asistencia.horas_trabajadas), 0).label("horas"),
            func.coalesce(
                func.sum(case((Asistencia.horas_trabajadas.is_(None), 1), else_=0)),
                0,
            ).label("sin_salida"),
        )
        .join(Asistencia, Asistencia.pasante_id == Usuario.id)
        .filter(Usuario.rol_id == 3)
    )

    if carrera_filtro is not None:
        q = q.filter(Usuario.carrera_id == carrera_filtro)

    if pasante_unico is not None:
        q = q.filter(Usuario.id == pasante_unico)

    if start_dt is not None and end_dt is not None:
        q = q.filter(Asistencia.fecha >= start_dt).filter(Asistencia.fecha < end_dt)

    q = q.group_by(Usuario.id, Usuario.nombres, Usuario.apellidos, Usuario.username)
    q = q.order_by(func.coalesce(func.sum(Asistencia.horas_trabajadas), 0).desc())

    items = []
    for row in q.all():
        horas = float(row.horas or 0)
        items.append(
            {
                "pasante_id": int(row.pasante_id),
                "nombres": row.nombres,
                "apellidos": row.apellidos,
                "username": row.username,
                "registros": int(row.registros or 0),
                "horas": horas,
                "sin_salida": int(row.sin_salida or 0),
            }
        )

    periodo = {"tipo": tipo}
    if start_dt is not None and end_dt is not None:
        periodo.update({"inicio": start.isoformat(), "fin": end.isoformat()})

    return {"periodo": periodo, "items": items}


@router.get("/mi-progreso")
def mi_progreso(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    from decimal import Decimal
    from sqlalchemy import case, func

    from app.models.asistencia import Asistencia, Reporte

    meta = getattr(usuario_actual, "meta_horas_pasantia", None) or 240
    try:
        meta = float(meta)
    except Exception:
        meta = 240

    total, verificadas, validadas = (
        db.query(
            func.coalesce(func.sum(Asistencia.horas_trabajadas), 0),
            func.coalesce(
                func.sum(
                    case(
                        (
                            func.upper(Reporte.estado_admin).in_(["VERIFICADO", "APROBADO"]) | 
                            func.upper(Reporte.estado_encargado).in_(["VERIFICADO", "APROBADO"]),
                            Asistencia.horas_trabajadas,
                        ),
                        else_=0,
                    )
                ),
                0,
            ),
            func.coalesce(
                func.sum(
                    case(
                        (func.upper(Reporte.estado_admin) == "APROBADO", Asistencia.horas_trabajadas),
                        else_=0,
                    )
                ),
                0,
            ),
        )
        .outerjoin(Reporte, Reporte.asistencia_id == Asistencia.id)
        .filter(Asistencia.pasante_id == usuario_actual.id)
        .first()
    )

    def _to_float(v) -> float:
        try:
            return float(Decimal(str(v)))
        except Exception:
            try:
                return float(v or 0)
            except Exception:
                return 0.0

    total_f = _to_float(total)
    verificadas_f = _to_float(verificadas)
    validadas_f = _to_float(validadas)

    restante = max(meta - total_f, 0)

    return {
        "meta_horas": meta,
        "total_horas": round(total_f, 2),
        "horas_verificadas": round(verificadas_f, 2),
        "horas_validadas": round(validadas_f, 2),
        "horas_restantes": round(restante, 2),
    }

# GET /reporte-pdf/diario — descarga PDF diario específico por reporte_id
@router.get("/reporte-pdf/diario")
def descargar_reporte_diario_especifico(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ENCARGADO", "ADMINISTRADOR"]))
):
    """Descarga un PDF diario específico por ID de reporte.
    
    Solo para ENCARGADO y ADMINISTRADOR.
    """
    from fastapi.responses import StreamingResponse
    from sqlalchemy.orm import joinedload
    
    from app.models.reporte import Reporte
    from app.models.asistencia import Asistencia
    from app.models.usuario import Usuario
    from app.utils.generador_reporte_pdf import generar_reporte_diario
    
    # Buscar el reporte
    reporte = db.query(Reporte).options(
        joinedload(Reporte.asistencia).joinedload(Asistencia.pasante)
    ).filter(Reporte.id == reporte_id).first()
    
    if not reporte:
        raise HTTPException(404, detail="Reporte no encontrado.")
    
    # Validar permisos
    if usuario_actual.rol_id == 2:  # ENCARGADO
        # El encargado solo puede ver reportes de pasantes de su carrera
        pasante = reporte.asistencia.pasante
        if pasante.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="No autorizado para descargar este reporte.")
    
    # Generar PDF
    pdf_buffer = generar_reporte_diario(
        pasante={
            "nombres": reporte.asistencia.pasante.nombres,
            "apellidos": reporte.asistencia.pasante.apellidos,
            "carnet_identidad": reporte.asistencia.pasante.carnet_identidad,
            "ru": reporte.asistencia.pasante.ru,
            "unidad_asignada": reporte.asistencia.pasante.unidad_asignada,
            "carrera": reporte.asistencia.pasante.carrera.nombre if reporte.asistencia.pasante.carrera else "—",
            "username": reporte.asistencia.pasante.username,
        },
        asistencia=reporte.asistencia,
        reporte=reporte,
        texto_reporte=f"Reporte Diario #{reporte.id}"
    )
    
    # Preparar respuesta
    pdf_buffer.seek(0)
    filename = f"reporte_diario_{reporte.id}_{reporte.asistencia.fecha}.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_buffer.read()),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

