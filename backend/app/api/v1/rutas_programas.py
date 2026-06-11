from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pathlib import Path
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4

from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.db.database import get_db
from app.models.programa_pasantia import ProgramaPasantia
from app.models.usuario import Usuario
from app.schemas.programa_schema import ProgramaCreate, ProgramaResponse, ProgramaUpdate

router = APIRouter()

_PROGRAMAS_DIR = Path(__file__).resolve().parents[2] / "static" / "programas_docs"
_PROGRAMAS_DIR.mkdir(parents=True, exist_ok=True)


def _programa_a_dict(p: ProgramaPasantia) -> dict:
    return {
        "id": p.id,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "gestion": p.gestion,
        "estado": bool(p.estado),
        "documento_url": p.documento_url,
    }


@router.get("/listar", response_model=List[ProgramaResponse])
def listar_programas(
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    nombre_rol = getattr(usuario_actual.rol, "nombre", "")
    query = db.query(ProgramaPasantia)
    if not (nombre_rol == "ADMINISTRADOR" and incluir_inactivos):
        query = query.filter(ProgramaPasantia.estado == True)  # noqa: E712
    return [_programa_a_dict(p) for p in query.order_by(func.lower(ProgramaPasantia.nombre)).all()]


@router.post("/crear", response_model=ProgramaResponse)
def crear_programa(
    datos: ProgramaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(rol_requerido(["ADMINISTRADOR"])),
):
    nombre = (datos.nombre or "").strip()
    if not nombre:
        raise HTTPException(400, detail="El nombre es obligatorio.")

    ya = (
        db.query(ProgramaPasantia)
        .filter(func.lower(ProgramaPasantia.nombre) == nombre.lower())
        .first()
    )
    if ya:
        raise HTTPException(409, detail="Ya existe un programa con ese nombre.")

    p = ProgramaPasantia(
        nombre=nombre,
        descripcion=(datos.descripcion.strip() if datos.descripcion else None),
        gestion=(datos.gestion.strip() if datos.gestion else None),
        estado=bool(datos.estado) if datos.estado is not None else True,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return _programa_a_dict(p)


@router.put("/editar/{programa_id}", response_model=ProgramaResponse)
def editar_programa(
    programa_id: int,
    datos: ProgramaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(rol_requerido(["ADMINISTRADOR"])),
):
    p = db.query(ProgramaPasantia).filter(ProgramaPasantia.id == programa_id).first()
    if not p:
        raise HTTPException(404, detail="Programa no encontrado.")

    update_data = datos.model_dump(exclude_unset=True)

    if "nombre" in update_data and update_data["nombre"] is not None:
        nombre = (update_data["nombre"] or "").strip()
        if not nombre:
            raise HTTPException(400, detail="El nombre es obligatorio.")
        ya = (
            db.query(ProgramaPasantia)
            .filter(func.lower(ProgramaPasantia.nombre) == nombre.lower(), ProgramaPasantia.id != p.id)
            .first()
        )
        if ya:
            raise HTTPException(409, detail="Ya existe un programa con ese nombre.")
        p.nombre = nombre

    if "descripcion" in update_data:
        p.descripcion = update_data["descripcion"].strip() if update_data["descripcion"] else None
    if "gestion" in update_data:
        p.gestion = update_data["gestion"].strip() if update_data["gestion"] else None
    if "estado" in update_data and update_data["estado"] is not None:
        p.estado = bool(update_data["estado"])
    if "documento_url" in update_data:
        p.documento_url = update_data["documento_url"]

    db.commit()
    db.refresh(p)
    return _programa_a_dict(p)


@router.delete("/desactivar/{programa_id}", response_model=ProgramaResponse)
def desactivar_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(rol_requerido(["ADMINISTRADOR"])),
):
    p = db.query(ProgramaPasantia).filter(ProgramaPasantia.id == programa_id).first()
    if not p:
        raise HTTPException(404, detail="Programa no encontrado.")
    p.estado = False
    db.commit()
    db.refresh(p)
    return _programa_a_dict(p)


@router.post("/documento/{programa_id}", response_model=ProgramaResponse)
def subir_documento_programa(
    programa_id: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(rol_requerido(["ADMINISTRADOR"])),
):
    if not archivo or not archivo.filename:
        raise HTTPException(400, detail="Archivo obligatorio.")

    p = db.query(ProgramaPasantia).filter(ProgramaPasantia.id == programa_id).first()
    if not p:
        raise HTTPException(404, detail="Programa no encontrado.")

    safe_name = Path(archivo.filename).name
    ext = Path(safe_name).suffix.lower()
    if ext not in [".pdf", ".png", ".jpg", ".jpeg", ".webp"]:
        raise HTTPException(400, detail="Formato no soportado. Usa PDF o imagen.")

    final_name = f"{uuid4().hex}_{safe_name}"
    dest = _PROGRAMAS_DIR / final_name
    content = archivo.file.read()
    if not content:
        raise HTTPException(400, detail="Archivo vacio.")
    dest.write_bytes(content)

    p.documento_url = f"/static/programas_docs/{final_name}"
    db.commit()
    db.refresh(p)
    return _programa_a_dict(p)

