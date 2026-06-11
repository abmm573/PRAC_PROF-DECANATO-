-- 1. Tabla de Carreras (Las 5 de la Facultad de Ciencias Sociales)
CREATE TABLE carreras (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    logo_url VARCHAR(255),
    estado BOOLEAN DEFAULT TRUE
);

-- 2. Tabla de Roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL -- 'ADMINISTRADOR', 'ENCARGADO', 'PASANTE'
);

-- 3. Tabla de Usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    carnet_identidad VARCHAR(20) UNIQUE NOT NULL,
    ru VARCHAR(30),
    unidad_asignada VARCHAR(150),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    celular VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol_id INT REFERENCES roles(id),
    carrera_id INT REFERENCES carreras(id) ON DELETE SET NULL, -- Null para Decano/Coordinador
    estado BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla de Configuración de Geocerca (Para no tener coordenadas "hardcodeadas" en FastAPI)
CREATE TABLE configuracion_facultad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    latitud DECIMAL(10, 8) NOT NULL,  -- Ej: -16.5048 (Aprox. UMSA)
    longitud DECIMAL(11, 8) NOT NULL, -- Ej: -68.1299
    radio_permitido_metros INT DEFAULT 50,
    actualizado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla de Asistencias
CREATE TABLE asistencias (
    id SERIAL PRIMARY KEY,
    pasante_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    hora_entrada TIMESTAMPTZ NOT NULL,
    latitud_entrada DECIMAL(10, 8) NOT NULL,
    longitud_entrada DECIMAL(11, 8) NOT NULL,
    hora_salida TIMESTAMPTZ,
    latitud_salida DECIMAL(10, 8),
    longitud_salida DECIMAL(11, 8),
    horas_trabajadas DECIMAL(5, 2), -- Se calcula al marcar salida
    UNIQUE(pasante_id, fecha) -- Un pasante solo tiene un registro de asistencia por día
);

-- 6. Tabla de Reportes Diarios
CREATE TABLE reportes (
    id SERIAL PRIMARY KEY,
    asistencia_id INT UNIQUE REFERENCES asistencias(id) ON DELETE CASCADE,
    actividades_realizadas TEXT NOT NULL,
    archivo_adjunto_url VARCHAR(255), -- Ruta donde se guarda el PDF o imagen (AWS S3, local, etc.)
    estado VARCHAR(20) DEFAULT 'PENDIENTE', -- 'PENDIENTE', 'APROBADO', 'RECHAZADO'
    comentarios_director TEXT,
    revisado_por INT REFERENCES usuarios(id), -- ID del Director de Carrera que lo revisó
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Insertar los 4 roles del sistema
INSERT INTO roles (nombre) VALUES ('ADMINISTRADOR'), ('ENCARGADO'),('PASANTE');

-- Insertar un par de carreras de Ciencias Sociales (puedes agregar las 5 luego)
INSERT INTO carreras (nombre, descripcion) VALUES 
('Antropologia', 'Carrera de Antropología'),
('Sociología', 'Carrera de Sociología'),
('Sociología', 'Carrera de Sociología'),
('Trabajo Social', 'Carrera de Trabajo Social'),
('Comunicación Social', 'Carrera de Comunicación Social');

ALTER TABLE asistencias ALTER COLUMN latitud_entrada DROP NOT NULL; ALTER TABLE asistencias ALTER COLUMN longitud_entrada DROP NOT NULL;