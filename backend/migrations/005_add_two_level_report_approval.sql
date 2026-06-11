-- Agrega campos para 2 niveles de revisión de reportes:
-- ENCARGADO: verificado_por/verificado_en
-- ADMIN: aprobado_por/aprobado_en

ALTER TABLE reportes ADD COLUMN IF NOT EXISTS verificado_por INTEGER;
ALTER TABLE reportes ADD COLUMN IF NOT EXISTS verificado_en TIMESTAMPTZ;
ALTER TABLE reportes ADD COLUMN IF NOT EXISTS aprobado_por INTEGER;
ALTER TABLE reportes ADD COLUMN IF NOT EXISTS aprobado_en TIMESTAMPTZ;

