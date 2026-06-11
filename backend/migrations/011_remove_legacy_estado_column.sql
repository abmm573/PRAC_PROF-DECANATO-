-- Eliminar el campo legacy 'estado' de la tabla reportes
-- Motivo: causaba errores 500 y conflictos con los nuevos campos separados

-- Primero verificar si la columna existe
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name='reportes' 
        AND column_name='estado'
    ) THEN
        -- Eliminar la columna legacy
        ALTER TABLE reportes DROP COLUMN estado;
        RAISE NOTICE 'Columna estado eliminada de la tabla reportes';
    ELSE
        RAISE NOTICE 'La columna estado no existe en la tabla reportes';
    END IF;
END $$;
