-- Migration: Add tipo_notificacion field to notificaciones_pasantia table
-- Description: Adds the notification type field to distinguish between completion and near-completion notifications

-- Add the new column
ALTER TABLE notificaciones_pasantia 
ADD COLUMN tipo_notificacion VARCHAR(20) DEFAULT 'COMPLETADA';

-- Update existing records to have the default type
UPDATE notificaciones_pasantia 
SET tipo_notificacion = 'COMPLETADA' 
WHERE tipo_notificacion IS NULL;

-- Drop the old unique constraint
DROP INDEX IF EXISTS uq_notif_pasantia_pasante;

-- Create the new composite unique constraint
ALTER TABLE notificaciones_pasantia 
ADD CONSTRAINT uq_notif_pasantia_pasante_tipo 
UNIQUE (pasante_id, tipo_notificacion);

-- Add index for better performance on the new field
CREATE INDEX idx_notificaciones_pasantia_tipo ON notificaciones_pasantia(tipo_notificacion);
CREATE INDEX idx_notificaciones_pasantia_creado_en_tipo ON notificaciones_pasantia(creado_en, tipo_notificacion);

-- Add comment to document the field types
COMMENT ON COLUMN notificaciones_pasantia.tipo_notificacion IS 'Type of notification: COMPLETADA for completed goals, CERCA_COMPLETAR for near completion alerts';
