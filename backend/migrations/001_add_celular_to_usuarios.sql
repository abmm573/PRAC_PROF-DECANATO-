-- Ejecutar sobre la BD existente (PostgreSQL)
-- Agrega columna celular si no existe.

ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS celular VARCHAR(20);

-- (Opcional) Index para b?squedas por celular
CREATE INDEX IF NOT EXISTS ix_usuarios_celular ON usuarios (celular);
