-- Agrega campos para identificar el programa/proyecto de pasantia por pasante
-- y meta de horas configurables.

ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS proyecto_nombre VARCHAR(255);
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS proyecto_documento_url VARCHAR(255);
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS meta_horas_pasantia NUMERIC(6,2) DEFAULT 240;

