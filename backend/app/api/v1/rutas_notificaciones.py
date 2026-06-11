from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os

from app.db.database import get_db
from app.models.usuario import Usuario
from app.models.carrera import Rol
from app.api.dependencias import rol_requerido
from app.utils.pasantia_completion import check_and_notify_near_completion, check_and_notify_completion
from app.utils.emailer import send_email, email_service_configured
from pydantic import BaseModel

router = APIRouter()

@router.post("/verificar-cerca-completar")
def verificar_pasantes_cerca_completar(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR"]))
):
    """
    Verifica todos los pasantes y envía notificaciones a aquellos que están 
    a 20 horas o menos de completar su meta de pasantía.
    """
    # Obtener todos los pasantes activos
    pasantes = (
        db.query(Usuario)
        .outerjoin(Rol, Usuario.rol_id == Rol.id)
        .filter(Usuario.estado.is_(True))
        .filter(Usuario.rol_id == 3)  # PASANTE
        .all()
    )
    
    resultados = []
    notificados = 0
    
    for pasante in pasantes:
        try:
            # Verificar si está cerca de completar
            total_horas, esta_cerca, notificado_ahora = check_and_notify_near_completion(
                db=db, 
                pasante_id=pasante.id, 
                horas_faltantes_threshold=20
            )
            
            # También verificar si ya completó
            total_horas_completado, cumplio, notificado_completado = check_and_notify_completion(
                db=db, 
                pasante_id=pasante.id
            )
            
            resultado = {
                "pasante_id": pasante.id,
                "nombre": f"{pasante.nombres} {pasante.apellidos}",
                "username": pasante.username,
                "total_horas": float(total_horas),
                "esta_cerca": esta_cerca,
                "notificado_cerca": notificado_ahora,
                "cumplio_meta": cumplio,
                "notificado_completado": notificado_completado
            }
            
            resultados.append(resultado)
            
            if notificado_ahora:
                notificados += 1
                
        except Exception as e:
            print(f"[notificaciones] Error verificando pasante {pasante.id}: {e}")
            continue
    
    return {
        "mensaje": f"Verificación completada. {notificados} pasantes notificados.",
        "total_pasantes_verificados": len(pasantes),
        "pasantes_notificados": notificados,
        "detalle": resultados
    }

@router.post("/verificar-pasante/{pasante_id}")
def verificar_pasante_especifico(
    pasante_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    """
    Verifica un pasante específico y envía notificaciones si está cerca de completar.
    """
    # Verificar que el pasante existe
    pasante = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante:
        raise HTTPException(status_code=404, detail="Pasante no encontrado.")
    
    # Verificar si está cerca de completar
    total_horas, esta_cerca, notificado_ahora = check_and_notify_near_completion(
        db=db, 
        pasante_id=pasante_id, 
        horas_faltantes_threshold=20
    )
    
    # También verificar si ya completó
    total_horas_completado, cumplio, notificado_completado = check_and_notify_completion(
        db=db, 
        pasante_id=pasante_id
    )
    
    return {
        "pasante_id": pasante_id,
        "nombre": f"{pasante.nombres} {pasante.apellidos}",
        "username": pasante.username,
        "total_horas": float(total_horas),
        "esta_cerca": esta_cerca,
        "notificado_cerca": notificado_ahora,
        "cumplio_meta": cumplio,
        "notificado_completado": notificado_completado,
        "mensaje": "Notificación procesada correctamente." if (notificado_ahora or notificado_completado) else "No se enviaron notificaciones."
    }


class EmailTestRequest(BaseModel):
    to: str
    subject: str
    body: str


@router.post("/test-email")
def test_email(
    request: EmailTestRequest,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    """
    Endpoint de prueba para verificar la configuración del servicio de correo.
    """
    print(f"[test_email] Enviando correo de prueba a: {request.to}")
    
    # Verificar si el servicio de correo está configurado
    if not email_service_configured():
        print("[test_email] ❌ Servicio de correo no configurado")
        return {
            "success": False,
            "message": "Servicio de correo no configurado. Verifica las variables SMTP en el archivo .env",
            "config_status": {
                "SMTP_HOST": bool(os.getenv('SMTP_HOST')),
                "SMTP_USER": bool(os.getenv('SMTP_USER')),
                "SMTP_PASS": bool(os.getenv('SMTP_PASS')),
                "SMTP_FROM": bool(os.getenv('SMTP_FROM'))
            }
        }
    
    try:
        enviado = send_email(
            subject=request.subject,
            body=request.body,
            to=[request.to]
        )
        
        if enviado:
            print(f"[test_email] ✅ Correo enviado exitosamente a {request.to}")
            return {
                "success": True,
                "message": f"Correo de prueba enviado exitosamente a {request.to}",
                "config_status": "Configuración SMTP correcta"
            }
        else:
            print(f"[test_email] ❌ Error al enviar correo a {request.to}")
            return {
                "success": False,
                "message": "Error al enviar correo. Verifica la configuración SMTP",
                "config_status": "Error en el envío"
            }
            
    except Exception as e:
        print(f"[test_email] ❌ Excepción al enviar correo: {e}")
        return {
            "success": False,
            "message": f"Excepción al enviar correo: {str(e)}",
            "config_status": "Error en el servidor"
        }
