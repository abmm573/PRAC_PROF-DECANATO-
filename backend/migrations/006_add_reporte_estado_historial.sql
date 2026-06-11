-- Crea historial de cambios de estado para reportes (aprobacion/rechazo/verificacion)

CREATE TABLE IF NOT EXISTS reporte_estado_historial (
  id SERIAL PRIMARY KEY,
  reporte_id INTEGER NOT NULL REFERENCES reportes(id) ON DELETE CASCADE,
  estado_anterior VARCHAR(20),
  estado_nuevo VARCHAR(20) NOT NULL,
  comentarios TEXT NOT NULL,
  actor_id INTEGER NOT NULL REFERENCES usuarios(id),
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_reporte_estado_historial_reporte_id
  ON reporte_estado_historial (reporte_id);

CREATE INDEX IF NOT EXISTS ix_reporte_estado_historial_actor_id
  ON reporte_estado_historial (actor_id);

