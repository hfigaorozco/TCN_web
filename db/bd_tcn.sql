CREATE DATABASE tcn;
USE tcn;

-- 0. TABLA USUARIO
CREATE TABLE usuario(
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone varchar(10) not null unique,
    password varchar(16) not null,
    es_admin tinyint(1) not null default 0
);

-- 1. TABLA CIUDAD
CREATE TABLE ciudad (
    codigo VARCHAR(3) PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE
);

-- 2. TABLA EDO_AUTOBUS
CREATE TABLE edo_autobus (
    codigo VARCHAR(4) PRIMARY KEY,
    descripcion VARCHAR(10) NOT NULL
);

-- 3. TABLA EDO_CORRIDA
CREATE TABLE edo_corrida(
    codigo VARCHAR(3) PRIMARY KEY,
    descripcion VARCHAR(10) NOT NULL UNIQUE
);

-- 4. TABLA AMENIDAD
CREATE TABLE amenidad(
    codigo VARCHAR(4) PRIMARY KEY,
    descripcion VARCHAR(25) NOT NULL
);

-- 5. TABLA TIPO_AUTOBUS
CREATE TABLE tipo_autobus (
    codigo VARCHAR(4) PRIMARY KEY,
    descripcion VARCHAR(10) NOT NULL UNIQUE
);

-- 6. TABLA TIPO_PASAJERO
CREATE TABLE tipo_pasajero (
    codigo VARCHAR(4) PRIMARY KEY,
    descripcion VARCHAR(10) NOT NULL,
    porcentajeDesc INT NOT NULL
);

-- 7. TABLA MARCA
CREATE TABLE marca (
    clave VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(15) NOT NULL
);

-- 8. TABLA OPERADOR
CREATE TABLE operador (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(15) NOT NULL,
    apellPat VARCHAR(15) NOT NULL,
    apellMat VARCHAR(15),
    fechaNac DATE NOT NULL,
    telefono VARCHAR(10) NOT NULL UNIQUE,
    fechaContrato DATE NOT NULL
);

-- 9. TABLA PASAJERO
CREATE TABLE pasajero (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    apellPat VARCHAR(20) NOT NULL,
    apellMat VARCHAR(20),
    fechaNac DATE NOT NULL,
    edad INT NOT NULL,
    correoElect VARCHAR(40),
    telefono VARCHAR(10) NOT NULL
);

-- 10. TABLA MODELO
CREATE TABLE modelo (
    clave VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(15) NOT NULL,
    marca VARCHAR(5) NOT NULL
);

-- 11. TABLA RUTA
CREATE TABLE ruta (
    codigo VARCHAR(9) PRIMARY KEY,
    distancia FLOAT NOT NULL,       
    ciudadOrigen VARCHAR(3) NOT NULL,      
    ciudadDestino VARCHAR(3) NOT NULL       
);

-- 12. TABLA AUTOBUS
CREATE TABLE autobus(
    numero INT PRIMARY KEY,
    matricula CHAR(6) NOT NULL UNIQUE,
    claveWIFI VARCHAR(20),
    cantAsientos INT NOT NULL,
    tipoAutobus VARCHAR(4) NOT NULL,
    estado VARCHAR(4) NOT NULL,
    marca VARCHAR(5) NOT NULL,
    modelo VARCHAR(5) NOT NULL
);

-- 13. TABLA CORRIDA
CREATE TABLE corrida(
    numero INT PRIMARY KEY AUTO_INCREMENT, 
    hora_salida TIME NOT NULL, 
    fecha_salida DATE NOT NULL,
    hora_llegada TIME NOT NULL,
    fecha_llegada DATE NOT NULL, 
    tarifaBase FLOAT NOT NULL, 
    lugaresDisp INT NOT NULL,
    autobus INT NOT NULL, 
    ruta VARCHAR(9) NOT NULL,
    operador INT, 
    estado VARCHAR(3) NOT NULL 
);

-- 14. TABLA RESERVACION
CREATE TABLE reservacion (
    numero INT PRIMARY KEY AUTO_INCREMENT, 
    fecha DATE NOT NULL, 
    fechaLimPago DATE NOT NULL, 
    cantPasajeros INT NOT NULL, 
    subtotal FLOAT NOT NULL, 
    IVA FLOAT NOT NULL, 
    total FLOAT NOT NULL, 
    pasajero INT NOT NULL, 
    corrida INT NOT NULL,
    usuario INT NULL
);

-- 15. TABLA ASIENTO
CREATE TABLE asiento(
    clave VARCHAR(6) PRIMARY KEY,
    numero INT NOT NULL,
    ubicacion VARCHAR(7) NOT NULL,
    autobus INT NOT NULL
);

-- 16. TABLA ASIENTO_RESERVACION
CREATE TABLE asiento_reservacion(
    asiento VARCHAR(6) NOT NULL,
    reservacion INT NOT NULL,
    PRIMARY KEY (asiento, reservacion)
);

-- 17. TABLA BOLETO
CREATE TABLE boleto(
    numero INT AUTO_INCREMENT PRIMARY KEY,
    precio FLOAT NOT NULL,
    asiento VARCHAR(6) NOT NULL,
    pasajero INT NOT NULL,
    tipoPasajero VARCHAR(4) NOT NULL,
    corrida INT NOT NULL
);

-- 18. TABLA LISTADO_AMENIDADES
CREATE TABLE listado_amenidades(
    tipoAutobus VARCHAR(4) NOT NULL,
    amenidad VARCHAR(4) NOT NULL,
    PRIMARY KEY(tipoAutobus, amenidad)
);

-- 19. TABLA CORRIDA_ASIENTO
CREATE TABLE corrida_asiento(
    corrida INT NOT NULL,
    asiento VARCHAR(6) NOT NULL,
    estado VARCHAR(13) NOT NULL,
    PRIMARY KEY (corrida, asiento)
);

-- RESTRICCIONES DE LLAVE FORÁNEA

-- RUTA
ALTER TABLE ruta
ADD CONSTRAINT fk_ruta_origen
FOREIGN KEY (ciudadOrigen) REFERENCES ciudad(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ruta
ADD CONSTRAINT fk_ruta_destino
FOREIGN KEY (ciudadDestino) REFERENCES ciudad(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;

-- AUTOBUS
ALTER TABLE autobus
ADD CONSTRAINT fk_tipoAutobus
FOREIGN KEY (tipoAutobus) REFERENCES tipo_autobus(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE autobus
ADD CONSTRAINT fk_estadoAutobus
FOREIGN KEY (estado) REFERENCES edo_autobus(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE autobus
ADD CONSTRAINT fk_marcaAutobus
FOREIGN KEY (marca) REFERENCES marca(clave)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE autobus
ADD CONSTRAINT fk_modeloAutobus
FOREIGN KEY (modelo) REFERENCES modelo(clave)
ON UPDATE CASCADE ON DELETE RESTRICT;

-- CORRIDA
ALTER TABLE corrida
ADD CONSTRAINT fk_corrida_autobus
FOREIGN KEY (autobus) REFERENCES autobus(numero)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE corrida
ADD CONSTRAINT fk_corrida_ruta
FOREIGN KEY (ruta) REFERENCES ruta(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE corrida
ADD CONSTRAINT fk_corrida_operador
FOREIGN KEY (operador) REFERENCES operador(numero)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE corrida
ADD CONSTRAINT fk_corrida_estado
FOREIGN KEY (estado) REFERENCES edo_corrida(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;

-- RESERVACION
ALTER TABLE reservacion
ADD CONSTRAINT fk_reserva_pasajero
FOREIGN KEY (pasajero) REFERENCES pasajero(numero)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE reservacion
ADD CONSTRAINT fk_reserva_corrida
FOREIGN KEY (corrida) REFERENCES corrida(numero)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE reservacion
ADD CONSTRAINT fk_reserva_usuario
FOREIGN KEY (usuario) REFERENCES usuario(id)
ON UPDATE CASCADE ON DELETE RESTRICT;

-- ASIENTO_RESERVACION
ALTER TABLE asiento_reservacion
ADD CONSTRAINT fk_asiento_reservacion_asiento
FOREIGN KEY (asiento) REFERENCES asiento(clave)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE asiento_reservacion
ADD CONSTRAINT fk_asiento_reservacion_reservacion
FOREIGN KEY (reservacion) REFERENCES reservacion(numero)
ON UPDATE CASCADE ON DELETE RESTRICT;

-- BOLETO
ALTER TABLE boleto
ADD CONSTRAINT fk_boleto_asiento
FOREIGN KEY (asiento) REFERENCES asiento(clave)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE boleto
ADD CONSTRAINT fk_boleto_pasajero
FOREIGN KEY (pasajero) REFERENCES pasajero(numero)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE boleto
ADD CONSTRAINT fk_boleto_tipoPasajero
FOREIGN KEY (tipoPasajero) REFERENCES tipo_pasajero(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE boleto
ADD CONSTRAINT fk_boleto_corrida
FOREIGN KEY (corrida) REFERENCES corrida(numero)
ON UPDATE CASCADE ON DELETE RESTRICT;

-- LISTADO_AMENIDADES
ALTER TABLE listado_amenidades
ADD CONSTRAINT fk_listado_tipoAutobus
FOREIGN KEY (tipoAutobus) REFERENCES tipo_autobus(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE listado_amenidades
ADD CONSTRAINT fk_listado_amenidad
FOREIGN KEY (amenidad) REFERENCES amenidad(codigo)
ON UPDATE CASCADE ON DELETE RESTRICT;


-- TABLA CORRIDA_ASIENTO
ALTER TABLE corrida_asiento
ADD CONSTRAINT fk_corrida_asiento_corrida 
FOREIGN KEY (corrida) REFERENCES corrida(numero)
ON UPDATE CASCADE ON DELETE CASCADE;
        
ALTER TABLE corrida_asiento
ADD CONSTRAINT fk_corrida_asiento_asiento 
FOREIGN KEY (asiento) REFERENCES asiento(clave)
ON UPDATE CASCADE ON DELETE RESTRICT;