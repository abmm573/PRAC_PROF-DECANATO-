-- 008: catalogo de programas de pasantia + relacion con usuarios

CREATE TABLE IF NOT EXISTS programas_pasantia (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL,
  descripcion TEXT,
  gestion VARCHAR(20),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  documento_url VARCHAR(255),
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Evitar duplicados por nombre (case-insensitive)
CREATE UNIQUE INDEX IF NOT EXISTS ux_programas_pasantia_nombre_lower
  ON programas_pasantia ((lower(nombre)));

ALTER TABLE usuarios
  ADD COLUMN IF NOT EXISTS programa_id INTEGER REFERENCES programas_pasantia(id);

CREATE INDEX IF NOT EXISTS ix_usuarios_programa_id ON usuarios (programa_id);

