-- Agrega Registro Universitario (RU) y Unidad asignada a usuarios
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS ru VARCHAR(30);
CREATE INDEX IF NOT EXISTS ix_usuarios_ru ON usuarios (ru);

ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS unidad_asignada VARCHAR(150);

