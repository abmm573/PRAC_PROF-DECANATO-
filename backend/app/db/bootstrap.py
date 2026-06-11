from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session


def ensure_schema(db: Session) -> None:
    """Aplica cambios mÃ­nimos (idempotentes) para que la app arranque.

    No reemplaza un sistema de migraciones formal; solo evita errores cuando
    faltan columnas nuevas en bases existentes.
    """
    bind = getattr(db, "get_bind", None)
    engine = bind() if callable(bind) else None
    dialect = getattr(engine, "dialect", None)
    name = getattr(dialect, "name", "") if dialect else ""

    # Solo PostgreSQL (el proyecto usa psycopg2).
    if name != "postgresql":
        return

    # 1) usuarios.celular
    try:
        db.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS celular VARCHAR(20);"))
    except Exception:
        # Si el usuario no tiene permisos, no rompemos el arranque.
        pass

    # 2) carreras.logo_url
    try:
        db.execute(text("ALTER TABLE carreras ADD COLUMN IF NOT EXISTS logo_url VARCHAR(255);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_carreras_logo_url ON carreras (logo_url);"))
    except Exception:
        pass

    # 3) usuarios.ru + usuarios.unidad_asignada
    try:
        db.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS ru VARCHAR(30);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_usuarios_ru ON usuarios (ru);"))
        db.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS unidad_asignada VARCHAR(150);"))
    except Exception:
        pass

    # 4) reportes: verificaciÃ³n (encargado) y aprobaciÃ³n (admin)
    try:
        db.execute(text("ALTER TABLE reportes ADD COLUMN IF NOT EXISTS verificado_por INTEGER;"))
        db.execute(text("ALTER TABLE reportes ADD COLUMN IF NOT EXISTS verificado_en TIMESTAMPTZ;"))
        db.execute(text("ALTER TABLE reportes ADD COLUMN IF NOT EXISTS aprobado_por INTEGER;"))
        db.execute(text("ALTER TABLE reportes ADD COLUMN IF NOT EXISTS aprobado_en TIMESTAMPTZ;"))
    except Exception:
        pass

    # 5) usuarios: proyecto y meta horas
    try:
        db.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS proyecto_nombre VARCHAR(255);"))
        db.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS proyecto_documento_url VARCHAR(255);"))
        db.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS meta_horas_pasantia NUMERIC(6,2) DEFAULT 240;"))
    except Exception:
        pass

    # 6) historial de cambios de estado de reportes
    try:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS reporte_estado_historial (
              id SERIAL PRIMARY KEY,
              reporte_id INTEGER NOT NULL REFERENCES reportes(id) ON DELETE CASCADE,
              estado_anterior VARCHAR(20),
              estado_nuevo VARCHAR(20) NOT NULL,
              comentarios TEXT NOT NULL,
              actor_id INTEGER NOT NULL REFERENCES usuarios(id),
              creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
            );
        """))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_reporte_estado_historial_reporte_id ON reporte_estado_historial (reporte_id);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_reporte_estado_historial_actor_id ON reporte_estado_historial (actor_id);"))
    except Exception:
        pass

    # 7) catalogo de programas de pasantia + enlace en usuarios
    try:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS programas_pasantia (
              id SERIAL PRIMARY KEY,
              nombre VARCHAR(200) NOT NULL,
              descripcion TEXT,
              gestion VARCHAR(20),
              estado BOOLEAN NOT NULL DEFAULT TRUE,
              documento_url VARCHAR(255),
              creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
            );
        """))
        db.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS ux_programas_pasantia_nombre_lower
              ON programas_pasantia ((lower(nombre)));
        """))
        db.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS programa_id INTEGER REFERENCES programas_pasantia(id);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_usuarios_programa_id ON usuarios (programa_id);"))
    except Exception:
        pass

    # 8) recuperacion de contrasena por correo (tokens)
    try:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
              id SERIAL PRIMARY KEY,
              usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
              token_hash VARCHAR(64) NOT NULL UNIQUE,
              creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
              expira_en TIMESTAMPTZ NOT NULL,
              usado_en TIMESTAMPTZ
            );
        """))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_password_reset_tokens_usuario_id ON password_reset_tokens (usuario_id);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_password_reset_tokens_token_hash ON password_reset_tokens (token_hash);"))
    except Exception:
        pass

    # 9) carreras.estado: evitar NULL (rompe response_model)
    try:
        db.execute(text("UPDATE carreras SET estado = TRUE WHERE estado IS NULL;"))
        db.execute(text("ALTER TABLE carreras ALTER COLUMN estado SET DEFAULT TRUE;"))
        db.execute(text("ALTER TABLE carreras ALTER COLUMN estado SET NOT NULL;"))
    except Exception:
        pass

    db.commit()

