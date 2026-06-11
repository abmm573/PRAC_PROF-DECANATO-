from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.models.asistencia import Asistencia
from app.schemas.asistencia_schema import AsistenciaCreate, AsistenciaUpdate

# Zona horaria de Bolivia (UTC-4)
BOLIVIA_TZ = timezone(timedelta(hours=-4))


def crear_entrada(db: Session, asistencia_data: AsistenciaCreate):
    hoy = datetime.now(timezone.utc).date()
    if db.query(Asistencia).filter(
        Asistencia.pasante_id == asistencia_data.pasante_id,
        Asistencia.fecha == hoy
    ).first():
        return None

    nueva = Asistencia(
        pasante_id       = asistencia_data.pasante_id,
        fecha            = hoy,
        hora_entrada     = datetime.now(timezone.utc),
        latitud_entrada  = asistencia_data.latitud_entrada,
        longitud_entrada = asistencia_data.longitud_entrada,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def formatear_horas_legibles(horas_decimales: float) -> str:
    """Convierte horas decimales a formato legible HH:MM:SS."""
    if horas_decimales == 0:
        return "0 horas"
    
    horas_enteras = int(horas_decimales)
    minutos_decimales = (horas_decimales - horas_enteras) * 60
    minutos_enteros = int(minutos_decimales)
    segundos_decimales = (minutos_decimales - minutos_enteros) * 60
    segundos_enteros = round(segundos_decimales)
    
    # Construir mensaje legible
    partes = []
    
    if horas_enteras > 0:
        if horas_enteras == 1:
            partes.append(f"{horas_enteras} hora")
        else:
            partes.append(f"{horas_enteras} horas")
    
    if minutos_enteros > 0:
        if minutos_enteros == 1:
            partes.append(f"{minutos_enteros} minuto")
        else:
            partes.append(f"{minutos_enteros} minutos")
    
    if segundos_enteros > 0 and len(partes) < 3:
        if segundos_enteros == 1:
            partes.append(f"{segundos_enteros} segundo")
        else:
            partes.append(f"{segundos_enteros} segundos")
    
    return " ".join(partes) if partes else "menos de 1 segundo"


def crear_entrada_por_pasante_id(db: Session, pasante_id: int):
    """Para fichaje público sin GPS."""
    from datetime import timezone, timedelta
    # Usar zona horaria de Bolivia (UTC-4)
    tz_bolivia = timezone(timedelta(hours=-4))
    hoy = datetime.now(tz_bolivia).date()
    
    if db.query(Asistencia).filter(
        Asistencia.pasante_id == pasante_id,
        Asistencia.fecha == hoy
    ).first():
        return None

    nueva = Asistencia(
        pasante_id       = pasante_id,
        fecha            = hoy,
        hora_entrada     = datetime.now(timezone.utc),
        latitud_entrada  = None,
        longitud_entrada = None,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    print(f"[crud_asistencia] Entrada creada: ID {nueva.id}, Hora: {nueva.hora_entrada}")
    return nueva


def registrar_salida(db: Session, asistencia_id: int, datos_salida: AsistenciaUpdate):
    registro = db.query(Asistencia).filter(Asistencia.id == asistencia_id).first()
    if not registro or registro.hora_salida is not None:
        return None

    hora_actual = datetime.now(timezone.utc)
    registro.hora_salida     = hora_actual
    registro.latitud_salida  = datos_salida.latitud_salida
    registro.longitud_salida = datos_salida.longitud_salida
    horas = round((hora_actual - registro.hora_entrada).total_seconds() / 3600, 2)
    registro.horas_trabajadas = horas if horas > 0 else 0.01
    db.commit()
    db.refresh(registro)
    return registro


def registrar_salida_por_pasante_id(db: Session, pasante_id: int):
    """Para fichaje público sin GPS. Retorna (registro, estado)."""
    from datetime import timezone, timedelta
    # Usar zona horaria de Bolivia (UTC-4)
    tz_bolivia = timezone(timedelta(hours=-4))
    hoy = datetime.now(tz_bolivia).date()
    
    registro = db.query(Asistencia).filter(
        Asistencia.pasante_id == pasante_id,
        Asistencia.fecha == hoy
    ).first()

    if not registro:
        return None, "no_entrada"
    if registro.hora_salida is not None:
        return None, "ya_salio"

    hora_actual = datetime.now(timezone.utc)
    registro.hora_salida      = hora_actual
    registro.latitud_salida   = None
    registro.longitud_salida  = None
    
    # Cálculo detallado de horas
    segundos_totales = (hora_actual - registro.hora_entrada).total_seconds()
    horas_brutas = segundos_totales / 3600
    horas_redondeadas = round(horas_brutas, 2)
    horas_legibles = formatear_horas_legibles(horas_brutas)
    
    print(f"[crud_asistencia] Cálculo de horas:")
    print(f"  Entrada: {registro.hora_entrada.strftime('%H:%M:%S')}")
    print(f"  Salida:  {hora_actual.strftime('%H:%M:%S')}")
    print(f"  Tiempo trabajado: {horas_legibles}")
    print(f"  Segundos totales: {segundos_totales}")
    print(f"  Horas brutas: {horas_brutas}")
    print(f"  Horas redondeadas: {horas_redondeadas}")
    
    registro.horas_trabajadas = horas_redondeadas if horas_redondeadas > 0 else 0.01
    db.commit()
    db.refresh(registro)
    
    print(f"[crud_asistencia] Salida registrada: ID {registro.id}, Horas: {registro.horas_trabajadas}")
    return registro, "ok"


def obtener_asistencia_hoy(db: Session, pasante_id: int):
    hoy = datetime.now(timezone.utc).date()
    return db.query(Asistencia).filter(
        Asistencia.pasante_id == pasante_id,
        Asistencia.fecha == hoy
    ).first()


def obtener_asistencias_por_pasante(db: Session, pasante_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Asistencia)
        .filter(Asistencia.pasante_id == pasante_id)
        .order_by(Asistencia.fecha.desc())
        .offset(skip).limit(limit).all()
    )


def obtener_todas_asistencias(db: Session, carrera_id: int = None):
    query = db.query(Asistencia)
    if carrera_id:
        from app.models.usuario import Usuario
        query = query.join(Usuario).filter(Usuario.carrera_id == carrera_id)
    return query.order_by(Asistencia.fecha.desc()).all()
