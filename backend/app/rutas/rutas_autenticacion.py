import httpx
import smtplib
import jwt
from email.message import EmailMessage
from datetime import datetime, timedelta
from passlib.context import CryptContext

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.base_datos.conexion import obtener_bd
from app.modelos.usuario import Usuario, RolUsuario
from app.esquemas.usuario import UsuarioCrear, UsuarioRespuesta
from app.nucleo.seguridad import obtener_hash_contrasena, verificar_contrasena, crear_token_acceso, obtener_usuario_actual

enrutador = APIRouter()

# --- CONFIGURACIÓN DE GOOGLE ---
GOOGLE_CLIENT_ID = "TU_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "TU_GOOGLE_CLIENT_SECRET"
GOOGLE_REDIRECT_URI = "http://localhost:8000/api/auth/google/callback"

# ==========================================
# 1. RUTAS TRADICIONALES (Formulario manual)
# ==========================================

@enrutador.post("/registro", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCrear, bd: Session = Depends(obtener_bd)):
    correo_limpio = usuario.correo.strip().lower()
    if not correo_limpio.endswith("@umsa.bo"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Solo se permiten correos institucionales terminados en @umsa.bo"
        )

    usuario_existente = bd.query(Usuario).filter(Usuario.correo == correo_limpio).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este correo ya está registrado en la plataforma."
        )
    
    contrasena_encriptada = obtener_hash_contrasena(usuario.contrasena)
    
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=correo_limpio,
        contrasena_hash=contrasena_encriptada,
        rol=RolUsuario.AUTOR # Por defecto
    )
    
    bd.add(nuevo_usuario)
    bd.commit()
    bd.refresh(nuevo_usuario) 
    
    return nuevo_usuario


@enrutador.post("/login")
def iniciar_sesion(credenciales: OAuth2PasswordRequestForm = Depends(), bd: Session = Depends(obtener_bd)):
    correo_limpio = credenciales.username.strip().lower()
    usuario = bd.query(Usuario).filter(Usuario.correo == correo_limpio).first()
    
    if not usuario or not verificar_contrasena(credenciales.password, usuario.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    datos_token = {
        "sub": usuario.correo, 
        "rol": usuario.rol.value if hasattr(usuario.rol, 'value') else usuario.rol
    }
    token_acceso = crear_token_acceso(datos=datos_token)
    
    return {
        "access_token": token_acceso, 
        "token_type": "bearer"
    }


@enrutador.get("/me")
def obtener_mis_datos(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return {
        "id": usuario_actual.id,
        "nombre": usuario_actual.nombre,
        "correo": usuario_actual.correo,
        "rol": usuario_actual.rol.value if hasattr(usuario_actual.rol, 'value') else usuario_actual.rol
    }


# ==========================================
# 2. CAMBIO DE CONTRASEÑA DESDE EL PANEL
# ==========================================

class CambiarMiContrasena(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str

@enrutador.put("/me/cambiar-contrasena")
def cambiar_mi_contrasena(
    datos: CambiarMiContrasena, 
    bd: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Permite a cualquier usuario logueado cambiar su propia contraseña."""
    
    # 1. Verificar que la contraseña actual ingresada sea correcta
    if not verificar_contrasena(datos.contrasena_actual, usuario_actual.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña actual ingresada es incorrecta."
        )
        
    # 2. Encriptar la nueva clave y actualizar la base de datos
    usuario_actual.contrasena_hash = obtener_hash_contrasena(datos.nueva_contrasena)
    bd.commit()
    
    return {"mensaje": "Tu contraseña ha sido actualizada exitosamente."}


# ==========================================
# 3. RUTAS GOOGLE OAUTH2 (Botón de Google)
# ==========================================

@enrutador.get("/google/login")
def login_google():
    """Redirige al usuario a la pantalla de login de Google."""
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email"
    }


@enrutador.get("/google/callback")
async def google_callback(code: str, bd: Session = Depends(obtener_bd)):
    """Recibe el código de Google, valida el dominio @umsa.bo y crea la sesión."""
    async with httpx.AsyncClient() as cliente:
        # Intercambiar código por token de acceso de Google
        res = await cliente.post("https://oauth2.googleapis.com/token", data={
            "code": code, 
            "client_id": GOOGLE_CLIENT_ID, 
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI, 
            "grant_type": "authorization_code"
        })
        tokens = res.json()
        
        # Obtener datos del usuario desde Google
        user_res = await cliente.get("https://www.googleapis.com/oauth2/v3/userinfo", 
                                     headers={"Authorization": f"Bearer {tokens['access_token']}"})
        user_info = user_res.json()

    correo = user_info.get("email")
    
    # Validar dominio estricto
    if not correo.endswith("@umsa.bo"):
        return RedirectResponse(url="http://localhost:5173/login?error=dominio")

    # Buscar usuario o crearlo automáticamente
    usuario = bd.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario:
        usuario = Usuario(
            nombre=user_info.get("name"), # El nombre real viene de Google
            correo=correo,
            contrasena_hash=obtener_hash_contrasena("google-auth-safe-password"),
            rol=RolUsuario.AUTOR
        )
        bd.add(usuario)
        bd.commit()
        bd.refresh(usuario)

    # Generar Token JWT de nuestro sistema para Vue
    token = crear_token_acceso({"sub": usuario.correo})
    
    # Redirigir al frontend con el token exitoso
    return RedirectResponse(url=f"http://localhost:5173/login?token={token}")


# ==========================================
# 4. RECUPERACIÓN DE CONTRASEÑA POR CORREO
# ==========================================

class SolicitudRecuperacion(BaseModel):
    correo: str

# Clave secreta larga para evitar advertencias de seguridad (Mínimo 32 caracteres)
SECRET_KEY_RECUPERACION = "esta_es_una_clave_secreta_muy_larga_y_segura_para_el_sistema_12345"

@enrutador.post("/solicitar-recuperacion")
def solicitar_recuperacion(datos: SolicitudRecuperacion, bd: Session = Depends(obtener_bd)):
    # 1. Limpiamos espacios y validamos el correo
    correo_limpio = datos.correo.strip().lower()
    usuario = bd.query(Usuario).filter(Usuario.correo == correo_limpio).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="El correo electrónico no se encuentra registrado en el sistema.")

    # 2. Crear un Token de recuperación válido por 15 minutos
    expiracion = datetime.utcnow() + timedelta(minutes=15)
    token_recuperacion = jwt.encode(
        {"sub": usuario.correo, "exp": expiracion, "tipo": "recuperacion"}, 
        SECRET_KEY_RECUPERACION, 
        algorithm="HS256"
    )

    # 3. Enviar el correo electrónico
    enviar_correo_recuperacion(usuario.correo, usuario.nombre, token_recuperacion)
    
    return {"mensaje": "Correo de recuperación enviado con éxito."}


def enviar_correo_recuperacion(correo_destino: str, nombre: str, token: str):
    """Función moderna para enviar correo mediante Gmail SMTP"""

    # Configurar con variables reales en producción
    remitente = "TU_CORREO@gmail.com"
    password_app = "TU_PASSWORD_DE_APLICACION"

    enlace_restaurar = f"http://localhost:5173/restaurar?token={token}"

    mensaje = EmailMessage()
    mensaje["Subject"] = "Recuperación de Contraseña - Revista Digital UMSA"
    mensaje["From"] = remitente
    mensaje["To"] = correo_destino

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 20px;">
        <div style="max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 16px; border: 1px solid #e2e8f0;">
          <h2 style="color: #0f172a;">Hola, {nombre} 👋</h2>
          <p style="color: #475569; line-height: 1.6;">Recibimos una solicitud para restaurar la contraseña de tu cuenta en la plataforma de Revistas de Ciencias Sociales.</p>
          <p style="color: #475569; line-height: 1.6;">Haz clic en el siguiente botón para crear una nueva contraseña. Este enlace expira de forma segura en 15 minutos.</p>
          <div style="text-align: center; margin: 30px 0;">
            <a href="{enlace_restaurar}" style="background-color: #7a1b2e; color: white; padding: 14px 28px; text-decoration: none; font-weight: bold; border-radius: 10px; display: inline-block;">Restaurar Contraseña</a>
          </div>
          <p style="color: #94a3b8; font-size: 12px; border-top: 1px solid #e2e8f0; padding-top: 15px;">Si no solicitaste este cambio, por favor ignora este correo. Tu cuenta sigue estando segura.</p>
        </div>
      </body>
    </html>
    """
    
    # Seteamos el contenido como HTML (procesa UTF-8 por defecto)
    mensaje.set_content(html, subtype="html")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, password_app)
        server.sendmail(remitente, correo_destino, mensaje.as_string())
        server.quit()
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor al intentar enviar el correo electrónico.")


# --- ESQUEMA Y RUTA PARA CONFIRMAR EL CAMBIO DE CONTRASEÑA ---

class ConfirmarRestablecer(BaseModel):
    token: str
    nueva_contrasena: str

@enrutador.post("/restablecer-contrasena")
def restablecer_contrasena(datos: ConfirmarRestablecer, bd: Session = Depends(obtener_bd)):
    """Desencripta el token enviado al correo, verifica su validez y actualiza la contraseña."""
    try:
        # Decodificar el token usando la misma firma segura
        payload = jwt.decode(datos.token, SECRET_KEY_RECUPERACION, algorithms=["HS256"])
        
        # Validar que sea estrictamente un token de recuperación (y no de sesión normal)
        if payload.get("tipo") != "recuperacion":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este token no es válido para recuperación de contraseña.")
            
        correo = payload.get("sub")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El enlace ha expirado. Por favor, solicita uno nuevo en la página de inicio.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El enlace de recuperación es inválido o está corrupto.")

    # Buscar al usuario asociado al token
    usuario = bd.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario asociado a este enlace ya no existe en el sistema.")

    # Encriptar la nueva contraseña e introducirla en la base de datos de forma segura
    usuario.contrasena_hash = obtener_hash_contrasena(datos.nueva_contrasena)
    bd.commit()

    return {"mensaje": "Tu contraseña ha sido restablecida con éxito. Ya puedes iniciar sesión con tus nuevas credenciales."}