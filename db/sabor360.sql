CREATE DATABASE IF NOT EXISTS sabor360
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sabor360;

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('CLIENTE','ADMINISTRADOR') NOT NULL DEFAULT 'CLIENTE',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Administrador (
    id_administrador INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    nivel_acceso ENUM('BASICO','TOTAL') NOT NULL DEFAULT 'BASICO',
    CONSTRAINT fk_admin_usuario
        FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Inventario (
    id_inventario INT AUTO_INCREMENT PRIMARY KEY,
    producto VARCHAR(100) NOT NULL,
    unidad_medida VARCHAR(30) NOT NULL,
    cantidad_actual DECIMAL(10,2) NOT NULL DEFAULT 0,
    stock_minimo DECIMAL(10,2) NOT NULL DEFAULT 0,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Menu (
    id_menu INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_menu DATE NOT NULL,
    descripcion VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Plato (
    id_plato INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio DECIMAL(10,2) NOT NULL DEFAULT 0,
    tipo ENUM('DESAYUNO','ALMUERZO','CENA') NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS MenuPlato (
    id_menu INT NOT NULL,
    id_plato INT NOT NULL,
    PRIMARY KEY (id_menu, id_plato),
    CONSTRAINT fk_menup_menu
        FOREIGN KEY (id_menu) REFERENCES Menu(id_menu)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_menup_plato
        FOREIGN KEY (id_plato) REFERENCES Plato(id_plato)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS PlatoInventario (
    id_plato INT NOT NULL,
    id_inventario INT NOT NULL,
    cantidad_necesaria DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_plato, id_inventario),
    CONSTRAINT fk_pi_plato
        FOREIGN KEY (id_plato) REFERENCES Plato(id_plato)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pi_inventario
        FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Consumo (
    id_consumo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_plato INT NOT NULL,
    id_menu INT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    fecha_consumo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_consumo_usuario
        FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_consumo_plato
        FOREIGN KEY (id_plato) REFERENCES Plato(id_plato)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_consumo_menu
        FOREIGN KEY (id_menu) REFERENCES Menu(id_menu)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS MovimientoInventario (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_inventario INT NOT NULL,
    id_administrador INT NULL,
    tipo_movimiento ENUM('ENTRADA','SALIDA') NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    motivo VARCHAR(255),
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mov_inv
        FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_mov_admin
        FOREIGN KEY (id_administrador) REFERENCES Administrador(id_administrador)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

-- Datos básicos para comprobar que la base funciona
INSERT IGNORE INTO Usuario (id_usuario, nombre, correo, contrasena_hash, tipo_usuario)
VALUES (1, 'Usuario de prueba', 'prueba@sabor360.local', 'CAMBIAR_POR_HASH_REAL', 'CLIENTE');

INSERT IGNORE INTO Plato (id_plato, nombre, descripcion, precio, tipo)
VALUES
(1, 'Huevos con arepa', 'Plato de prueba para desayuno', 8000, 'DESAYUNO'),
(2, 'Arroz con pollo', 'Plato de prueba para almuerzo', 15000, 'ALMUERZO'),
(3, 'Sopa ligera', 'Plato de prueba para cena', 10000, 'CENA');
