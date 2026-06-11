from __future__ import annotations

from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.usuario import Usuario
from app.models.carrera import Rol
from app.models.asistencia import Asistencia
from app.models.notificacion_pasantia import NotificacionPasantia
from app.utils.emailer import send_email, email_service_configured
from app.crud.crud_asistencia import formatear_horas_legibles
from datetime import datetime, timedelta


def total_horas_pasante(db: Session, pasante_id: int) -> Decimal:
    """Calcula el total de horas de un pasante con diagnóstico de precisión."""
    # Obtener todas las asistencias individuales para diagnóstico
    asistencias = (
        db.query(Asistencia.horas_trabajadas)
        .filter(Asistencia.pasante_id == pasante_id)
        .filter(Asistencia.horas_trabajadas.isnot(None))
        .all()
    )
    
    # Calcular suma manual para diagnóstico
    suma_manual = sum(float(a.horas_trabajadas) for a in asistencias)
    
    # Calcular suma con SQL (puede tener diferencias de redondeo)
    total_sql = (
        db.query(func.coalesce(func.sum(Asistencia.horas_trabajadas), 0))
        .filter(Asistencia.pasante_id == pasante_id)
        .scalar()
    )
    
    print(f"[total_horas] Diagnóstico para pasante {pasante_id}:")
    print(f"  Total registros: {len(asistencias)}")
    print(f"  Suma manual: {suma_manual}")
    print(f"  Suma SQL: {total_sql}")
    print(f"  Diferencia: {abs(suma_manual - float(total_sql))}")
    
    # Usar la suma manual para mayor precisión
    total_preciso = Decimal(str(suma_manual))
    
    try:
        return total_preciso
    except Exception:
        return Decimal("0")


def horas_validadas_pasante(db: Session, pasante_id: int) -> Decimal:
    from sqlalchemy import case
    from app.models.asistencia import Reporte

    total = (
        db.query(
            func.coalesce(
                func.sum(
                    case(
                        (func.upper(Reporte.estado_admin) == "APROBADO", Asistencia.horas_trabajadas),
                        else_=0,
                    )
                ),
                0,
            )
        )
        .outerjoin(Reporte, Reporte.asistencia_id == Asistencia.id)
        .filter(Asistencia.pasante_id == pasante_id)
        .scalar()
    )
    try:
        return Decimal(str(total))
    except Exception:
        return Decimal("0")


def _encargados_de_carrera(db: Session, carrera_id: Optional[int]) -> List[Usuario]:
    if carrera_id is None:
        return []

    return (
        db.query(Usuario)
        .outerjoin(Rol, Usuario.rol_id == Rol.id)
        .filter(Usuario.carrera_id == carrera_id)
        .filter(Usuario.estado.is_(True))
        .filter(or_(Usuario.rol_id == 2, func.upper(Rol.nombre) == "ENCARGADO"))
        .all()
    )


def check_and_notify_completion(db: Session, pasante_id: int) -> Tuple[Decimal, bool, bool]:
    """Returns: (total_horas, cumplio, notificado_ahora)."""
    pasante = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante:
        return Decimal("0"), False, False

    meta_raw = getattr(pasante, "meta_horas_pasantia", None) or Decimal("240")
    try:
        meta = Decimal(str(meta_raw))
    except Exception:
        meta = Decimal("240")

    total = total_horas_pasante(db, pasante_id)
    validadas = horas_validadas_pasante(db, pasante_id)

    # Diagnóstico
    print(f"[pasantia_completion] Verificando pasante {pasante_id}:")
    print(f"  Pasante: {pasante.nombres} {pasante.apellidos}")
    print(f"  Meta horas: {meta}")
    print(f"  Total horas: {total}")
    print(f"  Horas validadas: {validadas}")
    print(f"  Cumplió meta: {total >= meta}")
    print(f"  Email pasante: {pasante.email}")
    
    # Calcular y mostrar horas faltantes
    if total < meta:
        horas_faltantes = meta - total
        minutos_faltantes = horas_faltantes * 60
        print(f"  Horas faltantes: {horas_faltantes} ({minutos_faltantes:.1f} minutos)")
    else:
        horas_excedentes = total - meta
        minutos_excedentes = horas_excedentes * 60
        print(f"  Horas excedentes: {horas_excedentes} ({minutos_excedentes:.1f} minutos)")

    cumplio = total >= meta
    if not cumplio:
        print(f"  ❌ No ha cumplido la meta aún")
        return total, False, False

    ya = (
        db.query(NotificacionPasantia)
        .filter(NotificacionPasantia.pasante_id == pasante_id)
        .first()
    )
    if ya:
        print(f"  ⚠️ Ya se envió notificación anteriormente el {ya.creado_en}")
        print(f"  Enviado a: {ya.enviado_a}")
        return total, True, False

    print(f"  ✅ Enviando notificación de completado...")
    encargados = _encargados_de_carrera(db, pasante.carrera_id)
    emails_encargados = [e.email for e in encargados if e.email]
    email_pasante = pasante.email if pasante.email else None
    
    print(f"  Encargados encontrados: {len(encargados)}")
    print(f"  Emails encargados: {emails_encargados}")
    print(f"  Email pasante: {email_pasante}")

    # Si no hay destinatarios, igual registramos el hito para no reintentar indefinidamente.
    if not emails_encargados and not email_pasante:
        notif = NotificacionPasantia(
            pasante_id=pasante_id,
            carrera_id=pasante.carrera_id,
            total_horas=total,
            enviado_a=None,
        )
        db.add(notif)
        db.commit()
        return total, True, True

    carrera_nombre = getattr(getattr(pasante, "carrera", None), "nombre", None)
    if pasante.carrera_id is None:
        carrera_linea = "?"
    elif carrera_nombre:
        carrera_linea = f"{pasante.carrera_id} - {carrera_nombre}"
    else:
        carrera_linea = str(pasante.carrera_id)

    programa_nombre = getattr(getattr(pasante, "programa", None), "nombre", None)
    programa_linea = programa_nombre or "No asignado"

    subject_encargado = "Pasantia completada: meta de horas cumplida"
    
    # Formatear horas en formato legible
    total_legible = formatear_horas_legibles(float(total))
    validadas_legible = formatear_horas_legibles(float(validadas))
    
    body_encargado = f"""Estimado/a Encargado/a:

Se informa que el/la pasante ha cumplido su meta de horas de pasantia registrada en el sistema.

Datos del pasante
- Nombre: {pasante.nombres} {pasante.apellidos}
- Usuario: {pasante.username}
- CI: {pasante.carnet_identidad}
- Carrera: {carrera_linea}
- Programa: {programa_linea}
- Meta horas: {meta} horas
- Horas acumuladas: {total_legible}
- Horas validadas (APROBADO): {validadas_legible}

Quedamos atentos a cualquier verificacion o tramite correspondiente.

Atentamente,
Sistema de Control de Asistencia
"""

    subject_pasante = "Felicitaciones: cumpliste tu meta de horas de pasantia"
    body_pasante = f"""Estimado/a {pasante.nombres}:

Felicitaciones. Te confirmamos que has cumplido tu meta de horas de pasantia registrada en el sistema.

Detalle
- Carrera: {carrera_linea}
- Programa: {programa_linea}
- Meta horas: {meta} horas
- Horas acumuladas: {total_legible}
- Horas validadas (APROBADO): {validadas_legible}

¡Excelente trabajo! Ahora puedes proceder con los tramites correspondientes.

Atentamente,
Sistema de Control de Asistencia
"""

    sent_to: List[str] = []
    failed_to: List[str] = []

    for correo_encargado in emails_encargados:
        try:
            enviado = send_email(subject=subject_encargado, body=body_encargado, to=[correo_encargado])
            if enviado:
                sent_to.append(correo_encargado)
            else:
                failed_to.append(correo_encargado)
        except Exception as e:
            print(f"[pasantia_completion] Error enviando al encargado {correo_encargado}: {e}")
            failed_to.append(correo_encargado)

    if email_pasante:
        try:
            enviado = send_email(subject=subject_pasante, body=body_pasante, to=[email_pasante])
            if enviado:
                sent_to.append(email_pasante)
            else:
                failed_to.append(email_pasante)
        except Exception as e:
            print(f"[pasantia_completion] Error enviando al pasante {email_pasante}: {e}")
            failed_to.append(email_pasante)

    pasante_ok = (email_pasante is None) or (email_pasante in sent_to)
    encargado_ok = (not emails_encargados) or any(c in sent_to for c in emails_encargados)

    if not (pasante_ok and encargado_ok):
        detalle = ", ".join(failed_to) if failed_to else "sin detalle"
        print(
            "[pasantia_completion] No se pudo enviar la notificaci?n a todos los destinatarios. "
            f"Fallidos: {detalle}"
        )
        return total, True, False

    notif = NotificacionPasantia(
        pasante_id=pasante_id,
        carrera_id=pasante.carrera_id,
        total_horas=total,
        enviado_a=", ".join(sent_to) if sent_to else None,
    )
    db.add(notif)
    db.commit()

    return total, True, True


def check_and_notify_near_completion(db: Session, pasante_id: int, horas_faltantes_threshold: int = 20) -> Tuple[Decimal, bool, bool]:
    """Notifica cuando un pasante está cerca de completar su meta (falta X horas o menos).
    Returns: (total_horas, esta_cerca, notificado_ahora)."""
    pasante = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante:
        return Decimal("0"), False, False

    meta_raw = getattr(pasante, "meta_horas_pasantia", None) or Decimal("240")
    try:
        meta = Decimal(str(meta_raw))
    except Exception:
        meta = Decimal("240")

    total = total_horas_pasante(db, pasante_id)
    validadas = horas_validadas_pasante(db, pasante_id)
    
    # Calcular horas faltantes
    horas_faltantes = meta - total
    esta_cerca = 0 < horas_faltantes <= horas_faltantes_threshold
    
    if not esta_cerca:
        return total, False, False
    
    # Verificar si ya se notificó recientemente (evitar spam)
    fecha_limite = datetime.utcnow() - timedelta(days=7)  # Solo notificar una vez por semana
    
    notificacion_existente = (
        db.query(NotificacionPasantia)
        .filter(NotificacionPasantia.pasante_id == pasante_id)
        .filter(NotificacionPasantia.tipo_notificacion == "CERCA_COMPLETAR")
        .filter(NotificacionPasantia.creado_en >= fecha_limite)
        .first()
    )
    
    if notificacion_existente:
        return total, True, False
    
    # Obtener encargados
    encargados = _encargados_de_carrera(db, pasante.carrera_id)
    emails_encargados = [e.email for e in encargados if e.email]
    email_pasante = pasante.email if pasante.email else None
    
    # Si no hay destinatarios, igual registramos para no reintentar
    if not emails_encargados and not email_pasante:
        notif = NotificacionPasantia(
            pasante_id=pasante_id,
            carrera_id=pasante.carrera_id,
            total_horas=total,
            enviado_a=None,
            tipo_notificacion="CERCA_COMPLETAR"
        )
        db.add(notif)
        db.commit()
        return total, True, True
    
    # Información del pasante
    carrera_nombre = getattr(getattr(pasante, "carrera", None), "nombre", None)
    if pasante.carrera_id is None:
        carrera_linea = "?"
    elif carrera_nombre:
        carrera_linea = f"{pasante.carrera_id} - {carrera_nombre}"
    else:
        carrera_linea = str(pasante.carrera_id)
    
    programa_nombre = getattr(getattr(pasante, "programa", None), "nombre", None)
    programa_linea = programa_nombre or "No asignado"
    
    # Correo para encargados
    subject_encargado = f"⚠️ Alerta: Pasante cerca de completar meta de horas"
    
    # Formatear horas en formato legible
    total_legible = formatear_horas_legibles(float(total))
    validadas_legible = formatear_horas_legibles(float(validadas))
    faltantes_legible = formatear_horas_legibles(float(horas_faltantes))
    
    body_encargado = f"""Estimado/a Encargado/a:

Se informa que el/la pasante está cerca de cumplir su meta de horas de pasantía.

Datos del pasante:
- Nombre: {pasante.nombres} {pasante.apellidos}
- Usuario: {pasante.username}
- CI: {pasante.carnet_identidad}
- Carrera: {carrera_linea}
- Programa: {programa_linea}
- Meta horas: {meta} horas
- Horas acumuladas: {total_legible}
- Horas validadas (APROBADO): {validadas_legible}
- Horas faltantes: {faltantes_legible}

Recomendación: Supervisar el progreso y preparar los trámites de finalización.

Atentamente,
Sistema de Control de Asistencia
"""
    
    # Correo para pasante
    subject_pasante = f"🎯 ¡Estás cerca! Te faltan pocas horas para completar tu pasantía"
    body_pasante = f"""Estimado/a {pasante.nombres}:

¡Buenas noticias! Estás muy cerca de completar tu meta de horas de pasantía.

Tu progreso:
- Carrera: {carrera_linea}
- Programa: {programa_linea}
- Meta horas: {meta} horas
- Horas acumuladas: {total_legible}
- Horas validadas (APROBADO): {validadas_legible}
- Horas faltantes: {faltantes_legible}

¡Animo! Ya casi completas tu pasantía.

Atentamente,
Sistema de Control de Asistencia
"""
    
    sent_to: List[str] = []
    failed_to: List[str] = []
    
    # Enviar a encargados
    for correo_encargado in emails_encargados:
        try:
            enviado = send_email(subject=subject_encargado, body=body_encargado, to=[correo_encargado])
            if enviado:
                sent_to.append(correo_encargado)
            else:
                failed_to.append(correo_encargado)
        except Exception as e:
            print(f"[near_completion] Error enviando al encargado {correo_encargado}: {e}")
            failed_to.append(correo_encargado)
    
    # Enviar a pasante
    if email_pasante:
        try:
            enviado = send_email(subject=subject_pasante, body=body_pasante, to=[email_pasante])
            if enviado:
                sent_to.append(email_pasante)
            else:
                failed_to.append(email_pasante)
        except Exception as e:
            print(f"[near_completion] Error enviando al pasante {email_pasante}: {e}")
            failed_to.append(email_pasante)
    
    # Registrar notificación
    notif = NotificacionPasantia(
        pasante_id=pasante_id,
        carrera_id=pasante.carrera_id,
        total_horas=total,
        enviado_a=", ".join(sent_to) if sent_to else None,
        tipo_notificacion="CERCA_COMPLETAR"
    )
    db.add(notif)
    db.commit()
    
    return total, True, True
