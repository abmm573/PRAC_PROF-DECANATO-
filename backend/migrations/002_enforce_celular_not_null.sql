-- Ejecutar sobre la BD existente (PostgreSQL)
-- Requiere que todos los usuarios tengan celular (no NULL ni vac?o) antes de aplicar NOT NULL.

DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM usuarios
    WHERE celular IS NULL OR btrim(celular) = ''
  ) THEN
    RAISE EXCEPTION 'No se puede aplicar NOT NULL: existen usuarios sin celular. Primero actualiza esos registros.';
  END IF;
END $$;

ALTER TABLE usuarios
  ALTER COLUMN celular SET NOT NULL;

-- Evita guardar cadena vac?a
ALTER TABLE usuarios
  ADD CONSTRAINT IF NOT EXISTS ck_usuarios_celular_no_vacio CHECK (btrim(celular) <> '');
