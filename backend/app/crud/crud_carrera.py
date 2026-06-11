from sqlalchemy.orm import Session

from app.models.carrera import Carrera
from app.schemas.carrera_schema import CarreraUpdate, CarreraCreate


def listar_carreras(db: Session):
    return db.query(Carrera).order_by(Carrera.id.asc()).all()


def obtener_carrera(db: Session, carrera_id: int):
    return db.query(Carrera).filter(Carrera.id == carrera_id).first()


def actualizar_carrera(db: Session, carrera_id: int, datos: CarreraUpdate):
    carrera = obtener_carrera(db, carrera_id)
    if not carrera:
        return None

    update_data = datos.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(carrera, key, value)

    db.commit()
    db.refresh(carrera)
    return carrera


def crear_carrera(db: Session, datos: CarreraCreate):
    carrera = Carrera(
        nombre=(datos.nombre or '').strip(),
        descripcion=datos.descripcion,
        logo_url=datos.logo_url,
        estado=bool(datos.estado),
    )
    db.add(carrera)
    db.commit()
    db.refresh(carrera)
    return carrera


def desactivar_carrera(db: Session, carrera_id: int):
    carrera = obtener_carrera(db, carrera_id)
    if not carrera:
        return None
    carrera.estado = False
    db.commit()
    db.refresh(carrera)
    return carrera
