from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Idealmente, la contraseña y el usuario deben venir de un archivo .env
# Usamos un nombre representativo para la base de datos de la carrera
URL_BASE_DATOS = "postgresql://postgres:1234@localhost:5432/revistas"

# Motor principal de conexión
motor = create_engine(URL_BASE_DATOS)

# Creador de sesiones para cada petición que hagamos
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

# Clase base de la que heredarán todos nuestros modelos
Base = declarative_base()

# Dependencia de FastAPI para obtener la sesión de la base de datos y cerrarla automáticamente
def obtener_bd():
    bd = SesionLocal()
    try:
        yield bd
    finally:
        bd.close()