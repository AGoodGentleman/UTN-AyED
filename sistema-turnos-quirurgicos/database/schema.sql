DROP DATABASE IF EXISTS turnos_quirurgicos;
CREATE DATABASE turnos_quirurgicos
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE turnos_quirurgicos;

CREATE TABLE especialidad (
  id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL,
  descripcion VARCHAR(255),
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT uk_especialidad_nombre UNIQUE (nombre)
);

CREATE TABLE paciente (
  id_paciente INT AUTO_INCREMENT PRIMARY KEY,
  dni VARCHAR(20) NOT NULL,
  nombre VARCHAR(80) NOT NULL,
  apellido VARCHAR(80) NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  telefono VARCHAR(40),
  email VARCHAR(120),
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT uk_paciente_dni UNIQUE (dni)
);

CREATE TABLE profesional (
  id_profesional INT AUTO_INCREMENT PRIMARY KEY,
  matricula VARCHAR(40) NOT NULL,
  dni VARCHAR(20) NOT NULL,
  nombre VARCHAR(80) NOT NULL,
  apellido VARCHAR(80) NOT NULL,
  telefono VARCHAR(40),
  email VARCHAR(120),
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  id_especialidad INT NOT NULL,
  CONSTRAINT uk_profesional_matricula UNIQUE (matricula),
  CONSTRAINT uk_profesional_dni UNIQUE (dni),
  CONSTRAINT fk_profesional_especialidad
    FOREIGN KEY (id_especialidad) REFERENCES especialidad (id_especialidad)
);

CREATE TABLE quirofano (
  id_quirofano INT AUTO_INCREMENT PRIMARY KEY,
  numero VARCHAR(20) NOT NULL,
  ubicacion VARCHAR(120) NOT NULL,
  descripcion VARCHAR(255),
  estado ENUM('HABILITADO', 'MANTENIMIENTO', 'FUERA_DE_SERVICIO') NOT NULL DEFAULT 'HABILITADO',
  CONSTRAINT uk_quirofano_numero UNIQUE (numero)
);

CREATE TABLE tipo_cirugia (
  id_tipo_cirugia INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  duracion_estimada_minutos INT NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  id_especialidad INT NOT NULL,
  CONSTRAINT ck_tipo_cirugia_duracion CHECK (duracion_estimada_minutos > 0),
  CONSTRAINT uk_tipo_cirugia_nombre_especialidad UNIQUE (nombre, id_especialidad),
  CONSTRAINT fk_tipo_cirugia_especialidad
    FOREIGN KEY (id_especialidad) REFERENCES especialidad (id_especialidad)
);

CREATE TABLE turno_quirurgico (
  id_turno INT AUTO_INCREMENT PRIMARY KEY,
  fecha_hora_inicio DATETIME NOT NULL,
  fecha_hora_fin DATETIME NOT NULL,
  margen_pre_operatorio_minutos INT NOT NULL DEFAULT 30,
  margen_post_operatorio_minutos INT NOT NULL DEFAULT 30,
  estado ENUM('PROGRAMADO', 'CONFIRMADO', 'EN_CURSO', 'FINALIZADO', 'CANCELADO') NOT NULL DEFAULT 'PROGRAMADO',
  observaciones VARCHAR(500),
  motivo_cancelacion VARCHAR(500),
  id_paciente INT NOT NULL,
  id_quirofano INT NOT NULL,
  id_tipo_cirugia INT NOT NULL,
  CONSTRAINT ck_turno_fechas CHECK (fecha_hora_fin > fecha_hora_inicio),
  CONSTRAINT ck_turno_margenes CHECK (margen_pre_operatorio_minutos >= 0 AND margen_post_operatorio_minutos >= 0),
  CONSTRAINT fk_turno_paciente
    FOREIGN KEY (id_paciente) REFERENCES paciente (id_paciente),
  CONSTRAINT fk_turno_quirofano
    FOREIGN KEY (id_quirofano) REFERENCES quirofano (id_quirofano),
  CONSTRAINT fk_turno_tipo_cirugia
    FOREIGN KEY (id_tipo_cirugia) REFERENCES tipo_cirugia (id_tipo_cirugia)
);

CREATE TABLE turno_profesional (
  id_turno INT NOT NULL,
  id_profesional INT NOT NULL,
  rol ENUM('CIRUJANO_PRINCIPAL', 'CIRUJANO_ASISTENTE', 'ANESTESIOLOGO', 'INSTRUMENTADOR') NOT NULL,
  PRIMARY KEY (id_turno, id_profesional),
  CONSTRAINT fk_turno_profesional_turno
    FOREIGN KEY (id_turno) REFERENCES turno_quirurgico (id_turno)
    ON DELETE CASCADE,
  CONSTRAINT fk_turno_profesional_profesional
    FOREIGN KEY (id_profesional) REFERENCES profesional (id_profesional)
);

CREATE INDEX ix_turno_quirofano_intervalo
  ON turno_quirurgico (id_quirofano, fecha_hora_inicio, fecha_hora_fin, estado);

CREATE INDEX ix_turno_paciente_intervalo
  ON turno_quirurgico (id_paciente, fecha_hora_inicio, fecha_hora_fin, estado);

CREATE INDEX ix_turno_profesional_profesional
  ON turno_profesional (id_profesional, id_turno);

CREATE INDEX ix_turno_profesional_rol
  ON turno_profesional (id_turno, rol);

INSERT INTO especialidad (nombre, descripcion) VALUES
  ('Cirugia General', 'Procedimientos quirurgicos generales'),
  ('Traumatologia', 'Cirugias de huesos y articulaciones'),
  ('Cardiologia', 'Procedimientos cardiovasculares');

INSERT INTO paciente (dni, nombre, apellido, fecha_nacimiento, telefono, email) VALUES
  ('30111222', 'Ana', 'Perez', '1984-05-10', '2604000001', 'ana.perez@example.com'),
  ('28555777', 'Luis', 'Gomez', '1979-09-03', '2604000002', 'luis.gomez@example.com');

INSERT INTO profesional (matricula, dni, nombre, apellido, telefono, email, id_especialidad) VALUES
  ('MP-1001', '20111111', 'Carla', 'Rossi', '2604100001', 'c.rossi@example.com', 1),
  ('MP-1002', '20222222', 'Mario', 'Diaz', '2604100002', 'm.diaz@example.com', 1),
  ('MP-2001', '20333333', 'Elena', 'Ruiz', '2604100003', 'e.ruiz@example.com', 2);

INSERT INTO quirofano (numero, ubicacion, descripcion, estado) VALUES
  ('Q1', 'Primer piso', 'Quirofano principal', 'HABILITADO'),
  ('Q2', 'Segundo piso', 'Quirofano traumatologia', 'HABILITADO'),
  ('Q3', 'Primer piso', 'En reparacion programada', 'MANTENIMIENTO');

INSERT INTO tipo_cirugia (nombre, descripcion, duracion_estimada_minutos, id_especialidad) VALUES
  ('Apendicectomia', 'Extraccion quirurgica del apendice', 90, 1),
  ('Colecistectomia', 'Extraccion quirurgica de vesicula', 120, 1),
  ('Artroscopia', 'Procedimiento articular minimamente invasivo', 75, 2);
