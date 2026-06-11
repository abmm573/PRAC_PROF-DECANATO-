from __future__ import annotations

from pathlib import Path
import re
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencias import rol_requerido
from app.db.database import get_db
from app.crud import crud_carrera
from app.models.carrera import Carrera
from app.schemas.carrera_schema import CarreraResponse, CarreraUpdate, CarreraCreate


router = APIRouter()


def _safe_ext(filename: str) -> str:
    name = (filename or "").lower().strip()
    m = re.search(r"\.(png|jpg|jpeg|webp|gif)$", name)
    if not m:
        return ""
    return m.group(1)


@router.post("/", response_model=CarreraResponse)
def crear_carrera(
    datos: CarreraCreate,
    db: Session = Depends(get_db),
    _usuario=Depends(rol_requerido(["ADMINISTRADOR"])),
):
    nombre = (datos.nombre or "").strip()
    if not nombre:
        raise HTTPException(400, detail="El nombre es obligatorio.")
    existe = db.query(Carrera).filter(Carrera.nombre.ilike(nombre)).first()
    if existe:
        raise HTTPException(400, detail="Ya existe una carrera con ese nombre.")
    return crud_carrera.crear_carrera(db, datos)


@router.get("/", response_model=list[CarreraResponse])
def listar_carreras(
    db: Session = Depends(get_db),
    _usuario=Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"])),
):
    carreras = crud_carrera.listar_carreras(db)
    # Backward-compat: algunas BDs antiguas tienen estado NULL.
    for c in carreras:
        if getattr(c, "estado", None) is None:
            c.estado = True
    return carreras


@router.put("/{carrera_id}", response_model=CarreraResponse)
def editar_carrera(
    carrera_id: int,
    datos: CarreraUpdate,
    db: Session = Depends(get_db),
    _usuario=Depends(rol_requerido(["ADMINISTRADOR"])),
):
    carrera = crud_carrera.actualizar_carrera(db, carrera_id, datos)
    if not carrera:
        raise HTTPException(404, detail="Carrera no encontrada.")
    return carrera

@router.delete("/{carrera_id}", response_model=CarreraResponse)
def eliminar_carrera(
    carrera_id: int,
    db: Session = Depends(get_db),
    _usuario=Depends(rol_requerido(["ADMINISTRADOR"])),
):
    carrera = crud_carrera.desactivar_carrera(db, carrera_id)
    if not carrera:
        raise HTTPException(404, detail="Carrera no encontrada.")
    return carrera



@router.post("/{carrera_id}/logo", response_model=CarreraResponse)
async def subir_logo_carrera(
    carrera_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _usuario=Depends(rol_requerido(["ADMINISTRADOR"])),
):
    carrera = crud_carrera.obtener_carrera(db, carrera_id)
    if not carrera:
        raise HTTPException(404, detail="Carrera no encontrada.")

    if not file or not file.filename:
        raise HTTPException(400, detail="Archivo inv?lido.")

    ext = _safe_ext(file.filename)
    if not ext:
        raise HTTPException(400, detail="Formato inv?lido. Usa: png, jpg, jpeg, webp o gif.")

    content_type = (file.content_type or "").lower()
    if not content_type.startswith("image/"):
        raise HTTPException(400, detail="El archivo debe ser una imagen.")

    logos_dir = Path(__file__).resolve().parents[2] / "static" / "logos"
    logos_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"carrera_{carrera_id}_{stamp}.{ext}"
    dest = logos_dir / filename

    try:
        with dest.open("wb") as f:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
    finally:
        try:
            await file.close()
        except Exception:
            pass

    carrera = crud_carrera.actualizar_carrera(db, carrera_id, CarreraUpdate(logo_url=f"/static/logos/{filename}"))
    return carrera

