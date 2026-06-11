-- Ejecutar sobre la BD existente (PostgreSQL)
-- Agrega logo_url a carreras para personalizaci?n por carrera.

ALTER TABLE carreras ADD COLUMN IF NOT EXISTS logo_url VARCHAR(255);

CREATE INDEX IF NOT EXISTS ix_carreras_logo_url ON carreras (logo_url);
