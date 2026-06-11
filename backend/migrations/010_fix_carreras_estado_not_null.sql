-- Asegura que carreras.estado nunca sea NULL
-- Motivo: el response_model de FastAPI espera boolean y NULL provoca 500 (ResponseValidationError).

UPDATE carreras
SET estado = TRUE
WHERE estado IS NULL;

ALTER TABLE carreras
  ALTER COLUMN estado SET DEFAULT TRUE;

ALTER TABLE carreras
  ALTER COLUMN estado SET NOT NULL;
