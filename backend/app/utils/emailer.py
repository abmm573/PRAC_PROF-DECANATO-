import os
import smtplib
from email.message import EmailMessage
from typing import Iterable, List, Optional, Tuple


SmtpProfile = Tuple[str, int, Optional[str], Optional[str], Optional[str], bool, bool]

_LAST_EMAIL_ERROR: Optional[str] = None


def _get_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "y", "on")


def _smtp_profile(name_prefix: str = "SMTP") -> Optional[SmtpProfile]:
    host = os.getenv(f"{name_prefix}_HOST")
    if not host:
        return None

    port = int(os.getenv(f"{name_prefix}_PORT", "587"))
    user = os.getenv(f"{name_prefix}_USER")
    password = os.getenv(f"{name_prefix}_PASS")
    from_addr = os.getenv(f"{name_prefix}_FROM") or user
    if not from_addr:
        print(f"[emailer] {name_prefix}_FROM/{name_prefix}_USER no configurado. Perfil omitido.")
        return None

    use_ssl = _get_bool(f"{name_prefix}_USE_SSL", False)
    use_tls = _get_bool(f"{name_prefix}_USE_TLS", True)
    return (host, port, user, password, from_addr, use_ssl, use_tls)


def send_email(*, subject: str, body: str, to: Iterable[str]) -> bool:
    """
    Perfiles SMTP soportados (primario y fallback):
      - Primario: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM,
                  SMTP_USE_TLS, SMTP_USE_SSL
      - Secundario: SMTP2_HOST, SMTP2_PORT, SMTP2_USER, SMTP2_PASS, SMTP2_FROM,
                    SMTP2_USE_TLS, SMTP2_USE_SSL

    Retorna True si se envio con algun perfil; False si no se pudo enviar.
    """
    # Diagnóstico: mostrar variables de entorno
    print("[emailer] Diagnóstico de variables SMTP:")
    print(f"  SMTP_HOST: {os.getenv('SMTP_HOST')}")
    print(f"  SMTP_PORT: {os.getenv('SMTP_PORT')}")
    print(f"  SMTP_USER: {os.getenv('SMTP_USER')}")
    print(f"  SMTP_PASS: {'***' if os.getenv('SMTP_PASS') else 'None'}")
    print(f"  SMTP_FROM: {os.getenv('SMTP_FROM')}")
    print(f"  SMTP_USE_TLS: {os.getenv('SMTP_USE_TLS')}")
    print(f"  SMTP_USE_SSL: {os.getenv('SMTP_USE_SSL')}")
    
    to_list = [x for x in (t.strip() for t in to) if x]
    if not to_list:
        print("[emailer] Lista de destinatarios vacia. Correo no enviado.")
        return False

    profiles: List[SmtpProfile] = []
    primary = _smtp_profile("SMTP")
    secondary = _smtp_profile("SMTP2")
    if primary:
        profiles.append(primary)
    if secondary:
        profiles.append(secondary)

    if not profiles:
        print("[emailer] SMTP_HOST/SMTP2_HOST no configurado. Correo no enviado.")
        return False

    last_error: Optional[Exception] = None

    for idx, (host, port, user, password, from_addr, use_ssl, use_tls) in enumerate(profiles, start=1):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_list)
        msg.set_content(body)

        server = None
        try:
            server = smtplib.SMTP_SSL(host, port) if use_ssl else smtplib.SMTP(host, port)
            server.ehlo()
            if (not use_ssl) and use_tls:
                server.starttls()
                server.ehlo()
            if user and password:
                server.login(user, password)
            refused = server.send_message(msg)
            if refused:
                raise smtplib.SMTPRecipientsRefused(refused)
            print(f"[emailer] Correo enviado usando perfil SMTP #{idx} ({host}:{port}).")
            return True
        except Exception as e:
            last_error = e
            print(f"[emailer] Fallo perfil SMTP #{idx} ({host}:{port}): {e}")
        finally:
            if server is not None:
                try:
                    server.quit()
                except Exception:
                    pass

    if last_error:
        global _LAST_EMAIL_ERROR
        _LAST_EMAIL_ERROR = str(last_error)
        print(f"[emailer] No se pudo enviar correo en ningun perfil SMTP: {last_error}")
    return False


def email_service_configured() -> bool:
    """Retorna True si existe al menos un perfil SMTP configurado."""
    print("[emailer] Verificando configuración de correo...")
    
    # Mostrar todas las variables de entorno relacionadas
    smtp_vars = [
        'SMTP_HOST', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASS', 'SMTP_FROM',
        'SMTP_USE_TLS', 'SMTP_USE_SSL',
        'SMTP2_HOST', 'SMTP2_PORT', 'SMTP2_USER', 'SMTP2_PASS', 'SMTP2_FROM'
    ]
    
    print("[emailer] Variables de entorno encontradas:")
    for var in smtp_vars:
        valor = os.getenv(var)
        if 'PASS' in var:
            print(f"  {var}: {'***' if valor else 'None'}")
        else:
            print(f"  {var}: {valor}")
    
    primary = _smtp_profile("SMTP")
    secondary = _smtp_profile("SMTP2")
    
    print(f"[emailer] Perfil SMTP primario: {'Configurado' if primary else 'No configurado'}")
    print(f"[emailer] Perfil SMTP secundario: {'Configurado' if secondary else 'No configurado'}")
    
    result = primary is not None or secondary is not None
    print(f"[emailer] Servicio configurado: {result}")
    
    return result


def last_email_error() -> Optional[str]:
    return _LAST_EMAIL_ERROR
