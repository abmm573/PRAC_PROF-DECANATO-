from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.base_datos.conexion import obtener_bd
from app.modelos.usuario import Usuario

# Le indicamos a FastAPI dónde está la ruta de login
esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Configuraciones de Seguridad (Idealmente mover a variables de entorno .env)
CLAVE_SECRETA = "super_secreta_clave_ciencias_sociales_umsa_2026" 
ALGORITMO = "HS256"
TIEMPO_EXPIRACION_MINUTOS = 60 # El token durará 1 hora

# Configuración de Passlib para usar bcrypt
contexto_criptografia = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """Verifica si la contraseña ingresada coincide con la guardada en la base de datos."""
    return contexto_criptografia.verify(contrasena_plana, contrasena_hash)

def obtener_hash_contrasena(contrasena: str) -> str:
    """Encripta la contraseña plana para guardarla de forma segura."""
    return contexto_criptografia.hash(contrasena)

def crear_token_acceso(datos: dict) -> str:
    """Genera el JWT (JSON Web Token) con los datos del usuario y tiempo de expiración."""
    a_codificar = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=TIEMPO_EXPIRACION_MINUTOS)
    
    # Agregamos la fecha de expiración al contenido del token ('exp' es una convención de JWT)
    a_codificar.update({"exp": expiracion})
    
    # Generamos y firmamos el token
    token_jwt = jwt.encode(a_codificar, CLAVE_SECRETA, algorithm=ALGORITMO)
    return token_jwt


def obtener_usuario_actual(token: str = Depends(esquema_oauth2), bd: Session = Depends(obtener_bd)):
    """Desencripta el token y devuelve al usuario que está haciendo la petición."""
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Desencriptamos el token con nuestra clave secreta
        carga_util = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        correo: str = carga_util.get("sub")
        if correo is None:
            raise excepcion_credenciales
    except jwt.JWTError:
        raise excepcion_credenciales
        
    usuario = bd.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        raise excepcion_credenciales
        
    return usuario