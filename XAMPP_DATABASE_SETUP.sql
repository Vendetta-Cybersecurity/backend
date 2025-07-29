-- =============================================
-- SCRIPT PARA CREAR LA BASE DE DATOS EN XAMPP/phpMyAdmin
-- Ejecutar este script completo en phpMyAdmin
-- =============================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS figger_energy 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE figger_energy;

-- =============================================
-- 1. DEPARTAMENTOS - Estructura organizacional
-- =============================================
CREATE TABLE departamentos (
    id_departamento INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 2. ROLES - Roles específicos por departamento
-- =============================================
CREATE TABLE roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    id_departamento INT,
    descripcion TEXT,
    nivel_acceso ENUM('basico', 'intermedio', 'avanzado', 'admin') DEFAULT 'basico',
    permisos_sistema JSON,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
);

-- =============================================
-- 3. EMPLEADOS - Información del personal  
-- =============================================
CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    numero_documento VARCHAR(20) NOT NULL UNIQUE,
    tipo_documento ENUM('CC', 'CE', 'PP') DEFAULT 'CC',
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    direccion TEXT,
    ciudad VARCHAR(100),
    id_departamento INT,
    id_rol INT,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE NULL,
    salario DECIMAL(12,2),
    foto_perfil VARCHAR(255),
    estado ENUM('activo', 'inactivo', 'suspendido') DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento),
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- =============================================
-- 4. USUARIOS - Cuentas de acceso a la plataforma
-- =============================================
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    id_empleado INT NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    ultimo_acceso TIMESTAMP NULL,
    intentos_fallidos INT DEFAULT 0,
    bloqueado BOOLEAN DEFAULT FALSE,
    fecha_bloqueo TIMESTAMP NULL,
    token_2fa VARCHAR(100) NULL,
    token_recuperacion VARCHAR(100) NULL,
    fecha_expiracion_token TIMESTAMP NULL,
    configuracion_usuario JSON,
    estado ENUM('activo', 'inactivo', 'bloqueado') DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
);

-- =============================================
-- 5. SESIONES - Control de sesiones activas
-- =============================================
CREATE TABLE sesiones (
    id_sesion INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    token_sesion VARCHAR(255) NOT NULL UNIQUE,
    ip_origen VARCHAR(45),
    user_agent TEXT,
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    ubicacion VARCHAR(100),
    dispositivo VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- =============================================
-- 6. PERFILES_EMPLEADOS - Información extendida del perfil
-- =============================================
CREATE TABLE perfiles_empleados (
    id_perfil INT PRIMARY KEY AUTO_INCREMENT,
    id_empleado INT NOT NULL,
    biografia TEXT,
    habilidades JSON,
    experiencia_laboral JSON,
    educacion JSON,
    certificaciones JSON,
    idiomas JSON,
    redes_sociales JSON,
    preferencias_notificaciones JSON,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
);

-- =============================================
-- 7. NOTIFICACIONES - Sistema de notificaciones de la plataforma
-- =============================================
CREATE TABLE notificaciones (
    id_notificacion INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    tipo ENUM('info', 'warning', 'error', 'success') DEFAULT 'info',
    categoria ENUM('sistema', 'seguridad', 'trabajo', 'personal') DEFAULT 'sistema',
    leida BOOLEAN DEFAULT FALSE,
    fecha_lectura TIMESTAMP NULL,
    url_accion VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- =============================================
-- 8. ACTIVIDADES_USUARIO - Registro de actividades en la plataforma
-- =============================================
CREATE TABLE actividades_usuario (
    id_actividad INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    accion VARCHAR(100) NOT NULL,
    descripcion TEXT,
    modulo VARCHAR(50),
    ip_origen VARCHAR(45),
    datos_adicionales JSON,
    fecha_actividad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- =============================================
-- 9. LOG_SISTEMA - Logs generales del sistema para auditoría
-- =============================================
CREATE TABLE log_sistema (
    id_log INT PRIMARY KEY AUTO_INCREMENT,
    nivel ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL,
    mensaje TEXT NOT NULL,
    modulo VARCHAR(50),
    id_usuario INT NULL,
    ip_origen VARCHAR(45),
    user_agent TEXT,
    datos_contexto JSON,
    fecha_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- =============================================
-- DATOS INICIALES BÁSICOS
-- =============================================

-- Insertar departamentos
INSERT INTO departamentos (nombre, descripcion) VALUES
('Administración', 'Gestión financiera, recursos humanos y jurídica'),
('IT', 'Tecnología de la información y sistemas'),
('Operaciones', 'Instalación, mantenimiento y monitoreo de proyectos');

-- Insertar roles básicos
INSERT INTO roles (nombre, id_departamento, descripcion, nivel_acceso, permisos_sistema) VALUES
('CEO - Gerente General', 1, 'Dirección estratégica y representación legal', 'admin', 
 '{"dashboard": true, "usuarios": true, "reportes": true, "configuracion": true}'),
('Gerencia Jurídica', 1, 'Contratos y cumplimiento regulatorio', 'avanzado',
 '{"dashboard": true, "contratos": true, "reportes": true}'),
('Recursos Humanos', 1, 'Gestión de personal y capacitación', 'intermedio',
 '{"dashboard": true, "empleados": true, "capacitacion": true}'),
('CISO', 2, 'Seguridad de la información y ciberseguridad', 'admin',
 '{"dashboard": true, "seguridad": true, "logs": true, "usuarios": true}'),
('Desarrollador', 2, 'Desarrollo y mantenimiento de aplicaciones', 'avanzado',
 '{"dashboard": true, "desarrollo": true, "logs": true}'),
('Administrador de Sistemas', 2, 'Gestión de infraestructura tecnológica', 'avanzado',
 '{"dashboard": true, "sistemas": true, "monitoreo": true}'),
('Ingeniero de Proyectos', 3, 'Diseño y supervisión técnica de proyectos', 'avanzado',
 '{"dashboard": true, "proyectos": true, "reportes": true}'),
('Técnico de Campo', 3, 'Instalación y mantenimiento en campo', 'basico',
 '{"dashboard": true, "mantenimiento": true}');

-- =============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =============================================
CREATE INDEX idx_empleados_departamento ON empleados(id_departamento);
CREATE INDEX idx_empleados_estado ON empleados(estado);
CREATE INDEX idx_empleados_email ON empleados(email);
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_estado ON usuarios(estado);
CREATE INDEX idx_sesiones_token ON sesiones(token_sesion);
CREATE INDEX idx_sesiones_activa ON sesiones(activa);
CREATE INDEX idx_notificaciones_usuario ON notificaciones(id_usuario);
CREATE INDEX idx_notificaciones_leida ON notificaciones(leida);
CREATE INDEX idx_actividades_usuario ON actividades_usuario(id_usuario);
CREATE INDEX idx_actividades_fecha ON actividades_usuario(fecha_actividad);
CREATE INDEX idx_log_nivel ON log_sistema(nivel);
CREATE INDEX idx_log_fecha ON log_sistema(fecha_log);

-- =============================================
-- MENSAJE DE CONFIRMACIÓN
-- =============================================
SELECT 'Base de datos figger_energy creada exitosamente!' as mensaje;
SELECT COUNT(*) as total_departamentos FROM departamentos;
SELECT COUNT(*) as total_roles FROM roles;
