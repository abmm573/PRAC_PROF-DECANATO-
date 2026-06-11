from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
import hashlib
import os
import secrets
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
from uuid import uuid4

from pydantic import EmailStr, TypeAdapter, ValidationError

from app.db.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, Token, UsuarioUpdate, MiPerfilUpdate
from app.schemas.password_reset_schema import PasswordResetRequest, PasswordResetConfirm
from app.crud import crud_usuario
from app.core.security import verificar_password, crear_token_acceso, obtener_password_hash
from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.models.usuario import Usuario
from app.models.carrera import Rol
from app.models.password_reset_token import PasswordResetToken
from app.utils.emailer import send_email, email_service_configured, last_email_error

router = APIRouter()

_PROYECTO_DIR = Path(__file__).resolve().parents[2] / "static" / "proyecto_docs"
_PROYECTO_DIR.mkdir(parents=True, exist_ok=True)


_EMAIL_ADAPTER = TypeAdapter(EmailStr)


def _parse_email(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        raise HTTPException(400, detail="El email es obligatorio.")
    raw = raw.lower()
    try:
        return str(_EMAIL_ADAPTER.validate_python(raw))
    except ValidationError:
        raise HTTPException(400, detail="Email inv?lido. Usa formato usuario@dominio.com")


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _frontend_base_url() -> str:
    return (os.getenv("FRONTEND_URL") or "http://localhost:5173").rstrip("/")


def _password_reset_minutes() -> int:
    try:
        return int(os.getenv("PASSWORD_RESET_EXPIRE_MINUTES", "30"))
    except Exception:
        return 30


@router.post("/password-reset/solicitar")
def solicitar_reset_password(
    payload: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    """
    Envia un correo con un link/token para recuperar contrasena.
    Respuesta generica para no filtrar si el email existe.
    """
    email = _parse_email(payload.email)

    if not email_service_configured():
        raise HTTPException(503, detail="Servicio de correo no configurado en el servidor.")

    usuario = crud_usuario.obtener_usuario_por_email(db, email=email)
    ahora = datetime.now(timezone.utc)

    # Siempre generamos un token para que el flujo no revele si el correo existe.
    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    expira_en = ahora + timedelta(minutes=_password_reset_minutes())

    if usuario:
        # Invalidar tokens anteriores no usados
        try:
            (
                db.query(PasswordResetToken)
                .filter(
                    PasswordResetToken.usuario_id == usuario.id,
                    PasswordResetToken.usado_en.is_(None),
                    PasswordResetToken.expira_en >= ahora,
                )
                .update({PasswordResetToken.usado_en: ahora}, synchronize_session=False)
            )
            db.commit()
        except Exception:
            db.rollback()

        prt = PasswordResetToken(
            usuario_id=usuario.id,
            token_hash=token_hash,
            expira_en=expira_en,
            usado_en=None,
        )
        db.add(prt)
        db.commit()

    link = f"{_frontend_base_url()}/reset-password?token={token}"
    subject = "Recuperacion de contrasena"
    body = (
        "Solicitud de recuperacion de contrasena\n\n"
        f"Para cambiar tu contrasena usa este enlace (vence en {_password_reset_minutes()} minutos):\n"
        f"{link}\n\n"
        "Si no solicitaste este cambio, ignora este correo.\n"
    )

    enviado = send_email(subject=subject, body=body, to=[email])
    if not enviado:
        detail = "No se pudo enviar el correo. Revisa la configuracion SMTP del servidor."
        debug = os.getenv("SMTP_DEBUG_ERRORS", "").strip().lower() in ("1", "true", "yes", "y", "on")
        if debug:
            err = last_email_error()
            if err:
                detail = f"{detail} Detalle: {err}"
        raise HTTPException(503, detail=detail)

    return {"ok": True}


@router.post("/password-reset/confirmar")
def confirmar_reset_password(
    payload: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    token = (payload.token or "").strip()
    if not token:
        raise HTTPException(400, detail="Token obligatorio.")

    nueva_password = payload.nueva_password or ""
    if len(nueva_password) < 6:
        raise HTTPException(400, detail="La contrasena debe tener al menos 6 caracteres.")

    ahora = datetime.now(timezone.utc)
    token_hash = _hash_token(token)

    prt = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.usado_en.is_(None),
            PasswordResetToken.expira_en >= ahora,
        )
        .first()
    )
    if not prt:
        raise HTTPException(400, detail="Token invalido o expirado.")

    usuario = db.query(Usuario).filter(Usuario.id == prt.usuario_id).first()
    if not usuario:
        raise HTTPException(400, detail="Token invalido o expirado.")

    usuario.password_hash = obtener_password_hash(nueva_password)
    prt.usado_en = ahora

    # Invalidar cualquier otro token vigente del usuario
    (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.usuario_id == usuario.id,
            PasswordResetToken.usado_en.is_(None),
            PasswordResetToken.expira_en >= ahora,
        )
        .update({PasswordResetToken.usado_en: ahora}, synchronize_session=False)
    )

    db.commit()
    return {"ok": True}


def _usuario_a_dict(user: Usuario, db: Session = None) -> dict:
    nombre_rol = None
    if hasattr(user, "rol") and user.rol and hasattr(user.rol, "nombre"):
        nombre_rol = user.rol.nombre
    elif db and user.rol_id:
        rol_db = db.query(Rol).filter(Rol.id == user.rol_id).first()
        nombre_rol = rol_db.nombre if rol_db else None
    programa_id = getattr(user, "programa_id", None)
    programa_nombre = None
    programa_gestion = None
    programa_documento_url = None

    if getattr(user, "programa", None) is not None:
        programa_nombre = getattr(user.programa, "nombre", None)
        programa_gestion = getattr(user.programa, "gestion", None)
        programa_documento_url = getattr(user.programa, "documento_url", None)
    elif db and programa_id:
        try:
            from app.models.programa_pasantia import ProgramaPasantia

            p = db.query(ProgramaPasantia).filter(ProgramaPasantia.id == programa_id).first()
            if p:
                programa_nombre = p.nombre
                programa_gestion = p.gestion
                programa_documento_url = p.documento_url
        except Exception:
            pass

    return {
        "id":               user.id,
        "nombres":          user.nombres,
        "apellidos":        user.apellidos,
        "carnet_identidad": user.carnet_identidad,   # agregado
        "ru":               getattr(user, "ru", None),
        "unidad_asignada":  getattr(user, "unidad_asignada", None),
        "username":         user.username,
        "email":            user.email,
        "celular":          user.celular,
        "rol_id":           user.rol_id,
        "carrera_id":       user.carrera_id,
        "estado":           user.estado,
        "rol":              nombre_rol,
        "carrera_nombre":   getattr(getattr(user, "carrera", None), "nombre", None),
        "carrera_logo_url": getattr(getattr(user, "carrera", None), "logo_url", None),
        "programa_id": programa_id,
        "programa_nombre": programa_nombre,
        "programa_gestion": programa_gestion,
        "programa_documento_url": programa_documento_url,
        "proyecto_nombre": getattr(user, "proyecto_nombre", None),
        "proyecto_documento_url": getattr(user, "proyecto_documento_url", None),
        "meta_horas_pasantia": float(getattr(user, "meta_horas_pasantia", 240) or 240),
    }


# ──────────────────────────────────────────────────────────────────────────────
# POST /registro
# ADMINISTRADOR → ENCARGADO o PASANTE (cualquier carrera)
# ENCARGADO     → solo PASANTE de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    nombre_rol_actual = getattr(usuario_actual.rol, "nombre", "")
    rol_nuevo = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    if not rol_nuevo:
        raise HTTPException(status_code=400, detail="El rol_id indicado no existe.")

    if nombre_rol_actual == "ENCARGADO":
        if rol_nuevo.nombre != "PASANTE":
            raise HTTPException(403, detail="Un Encargado solo puede registrar Pasantes.")
        if not usuario_actual.carrera_id:
            raise HTTPException(400, detail="Tu cuenta de encargado no tiene carrera asignada.")
        usuario = usuario.model_copy(update={"carrera_id": usuario_actual.carrera_id})

    email_norm = _parse_email(str(usuario.email))
    usuario = usuario.model_copy(update={"email": email_norm})

    if crud_usuario.obtener_usuario_por_email(db, email=email_norm):
        raise HTTPException(400, detail="El email ya está registrado.")

    username_candidato = crud_usuario.generar_username(usuario.nombres, usuario.apellidos, usuario.carnet_identidad)
    if crud_usuario.obtener_usuario_por_username(db, username=username_candidato):
        raise HTTPException(400, detail=f"El username '{username_candidato}' ya existe. Verifica el carnet de identidad.")

    nuevo_usuario = crud_usuario.crear_usuario(db=db, usuario=usuario)
    return _usuario_a_dict(nuevo_usuario, db)


# ──────────────────────────────────────────────────────────────────────────────
# POST /login
# ──────────────────────────────────────────────────────────────────────────────
@router.post("/login", response_model=Token, summary="Iniciar Sesión")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = _parse_email(form_data.username)
    usuario = crud_usuario.obtener_usuario_por_email(db, email=email)
    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos",
                            headers={"WWW-Authenticate": "Bearer"})
    if not usuario.estado:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Tu cuenta está desactivada.")

    return {"access_token": crear_token_acceso(data={"sub": usuario.email}), "token_type": "bearer"}


# ──────────────────────────────────────────────────────────────────────────────
# GET /listar
# ADMINISTRADOR → todos | ENCARGADO → PASANTES de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/listar", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    es_encargado = getattr(usuario_actual.rol, "nombre", "") == "ENCARGADO"
    carrera_id   = usuario_actual.carrera_id if es_encargado else None
    usuarios_db  = crud_usuario.obtener_usuarios(db=db, skip=skip, limit=limit, carrera_id=carrera_id)
    return [_usuario_a_dict(u) for u in usuarios_db]


# ──────────────────────────────────────────────────────────────────────────────
# PUT /editar/{usuario_id}
# ADMINISTRADOR → edita cualquier usuario
# ENCARGADO     → solo puede editar PASANTES de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.put("/editar/{usuario_id}", response_model=UsuarioResponse)
def editar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    nombre_rol_actual = getattr(usuario_actual.rol, "nombre", "")

    update_payload = datos.model_dump(exclude_unset=True)
    if "email" in update_payload:
        datos.email = _parse_email(str(update_payload.get("email")))

    # Verificar que el ENCARGADO solo edite pasantes de su carrera
    if nombre_rol_actual == "ENCARGADO":
        objetivo = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Usuario no encontrado.")
        rol_objetivo = getattr(objetivo.rol, "nombre", "")
        if rol_objetivo != "PASANTE" or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes editar pasantes de tu carrera.")

    # Validaci?n: celular obligatorio (no permitir borrarlo)
    if hasattr(datos, "celular") and ("celular" in datos.model_dump(exclude_unset=True)):
        if datos.celular is None or str(datos.celular).strip() == "":
            raise HTTPException(400, detail="No puedes dejar el celular vac?o.")

    usuario_actualizado = crud_usuario.actualizar_usuario(db=db, usuario_id=usuario_id, datos_actualizar=datos)
    if not usuario_actualizado:
        raise HTTPException(404, detail="Usuario no encontrado.")
    return _usuario_a_dict(usuario_actualizado, db)


# ──────────────────────────────────────────────────────────────────────────────
# DELETE /desactivar/{usuario_id}
# ADMINISTRADOR → desactiva cualquier usuario
# ENCARGADO     → solo puede desactivar PASANTES de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.delete("/desactivar/{usuario_id}", response_model=UsuarioResponse)
def desactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    nombre_rol_actual = getattr(usuario_actual.rol, "nombre", "")

    if nombre_rol_actual == "ENCARGADO":
        objetivo = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Usuario no encontrado.")
        rol_objetivo = getattr(objetivo.rol, "nombre", "")
        if rol_objetivo != "PASANTE" or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes desactivar pasantes de tu carrera.")

    usuario_borrado = crud_usuario.desactivar_usuario(db=db, usuario_id=usuario_id)
    if not usuario_borrado:
        raise HTTPException(404, detail="Usuario no encontrado.")
    return _usuario_a_dict(usuario_borrado, db)


# ──────────────────────────────────────────────────────────────────────────────
# GET /me
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/me", response_model=UsuarioResponse)
def leer_usuario_actual(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return _usuario_a_dict(usuario_actual)


@router.put("/mi-perfil", response_model=UsuarioResponse)
def actualizar_mi_perfil(
    datos: MiPerfilUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    update_data = datos.model_dump(exclude_unset=True)

    # celular no puede quedar vacio si se manda
    if "celular" in update_data:
        if update_data["celular"] is None or str(update_data["celular"]).strip() == "":
            raise HTTPException(400, detail="No puedes dejar el celular vacio.")

    # cambio de contrasena
    password_actual = (update_data.get("password_actual") or "").strip() if "password_actual" in update_data else ""
    nueva_password = (update_data.get("nueva_password") or "").strip() if "nueva_password" in update_data else ""

    if password_actual or nueva_password:
        if (not password_actual) or (not nueva_password):
            raise HTTPException(400, detail="Para cambiar contrasena debes enviar password_actual y nueva_password.")
        if len(nueva_password) < 6:
            raise HTTPException(400, detail="La contrasena debe tener al menos 6 caracteres.")
        if not verificar_password(password_actual, usuario_actual.password_hash):
            raise HTTPException(400, detail="Password actual incorrecto.")
        usuario_actual.password_hash = obtener_password_hash(nueva_password)

    # campos editables
    for campo in ["nombres", "apellidos", "celular", "ru"]:
        if campo in update_data and update_data[campo] is not None:
            value = update_data[campo]
            if isinstance(value, str):
                value = value.strip()
                if value == "":
                    value = None
            setattr(usuario_actual, campo, value)

    db.commit()
    db.refresh(usuario_actual)
    return _usuario_a_dict(usuario_actual, db)


@router.put("/mi-proyecto", response_model=UsuarioResponse)
def actualizar_mi_proyecto(
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"])),
):
    if "proyecto_nombre" not in datos.model_dump(exclude_unset=True):
        raise HTTPException(400, detail="proyecto_nombre es obligatorio.")

    nombre = (datos.proyecto_nombre or "").strip() if datos.proyecto_nombre is not None else ""
    if not nombre:
        raise HTTPException(400, detail="proyecto_nombre es obligatorio.")

    usuario_actual.proyecto_nombre = nombre
    db.commit()
    db.refresh(usuario_actual)
    return _usuario_a_dict(usuario_actual, db)


@router.post("/proyecto-documento", response_model=UsuarioResponse)
def subir_documento_proyecto(
    archivo: UploadFile = File(...),
    usuario_id: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    if not archivo or not archivo.filename:
        raise HTTPException(400, detail="Archivo obligatorio.")

    nombre_rol_actual = getattr(getattr(usuario_actual, "rol", None), "nombre", "") or ""

    objetivo_id = usuario_id or usuario_actual.id
    if usuario_id is not None:
        if nombre_rol_actual not in ("ADMINISTRADOR", "ENCARGADO"):
            raise HTTPException(403, detail="No autorizado.")

        if nombre_rol_actual == "ENCARGADO":
            objetivo = db.query(Usuario).filter(Usuario.id == objetivo_id).first()
            if not objetivo:
                raise HTTPException(404, detail="Usuario no encontrado.")
            rol_objetivo = getattr(objetivo.rol, "nombre", "")
            if rol_objetivo != "PASANTE" or objetivo.carrera_id != usuario_actual.carrera_id:
                raise HTTPException(403, detail="Solo puedes editar pasantes de tu carrera.")
    else:
        if nombre_rol_actual != "PASANTE":
            raise HTTPException(403, detail="Solo pasante puede subir su propio documento sin usuario_id.")

    objetivo = db.query(Usuario).filter(Usuario.id == objetivo_id).first()
    if not objetivo:
        raise HTTPException(404, detail="Usuario no encontrado.")

    ext = Path(archivo.filename).suffix.lower()
    if ext not in (".pdf", ".png", ".jpg", ".jpeg"):
        raise HTTPException(400, detail="Tipo de archivo no permitido. Usa PDF o imagen.")

    safe_base = f"{objetivo.username}_{uuid4().hex}{ext}"
    destino = _PROYECTO_DIR / safe_base
    contenido = archivo.file.read()
    destino.write_bytes(contenido)

    objetivo.proyecto_documento_url = f"/static/proyecto_docs/{safe_base}"
    db.commit()
    db.refresh(objetivo)
    return _usuario_a_dict(objetivo, db)
