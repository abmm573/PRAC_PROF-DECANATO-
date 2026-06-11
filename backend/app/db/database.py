import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Permite configurar por .env/variables de entorno.
# Ejemplo:
#   DATABASE_URL=postgresql://postgres:postgre@localhost/asistencia
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:12345@localhost/asistencia",
)

engine_kwargs = {
    "pool_pre_ping": True,
}

# Evita que la app se quede colgada mucho tiempo si la BD no responde.
if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    engine_kwargs["connect_args"] = {"connect_timeout": 5}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
