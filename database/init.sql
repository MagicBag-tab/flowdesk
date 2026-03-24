--Script para generacion de base de datos en postgresql puro(sin comentarios para limpieza)
CREATE TABLE rol (
    id_rol INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE usuario (
    id_usuario INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    estado VARCHAR(30) NOT NULL,
    telefono VARCHAR(20),
    id_rol INT NOT NULL,
    CONSTRAINT fk_usuario_rol
        FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE proveedor (
    id_proveedor INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(150) UNIQUE,
    direccion VARCHAR(200)
);

CREATE TABLE producto (
    id_producto INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_proveedor INT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    stock_actual INT NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo INT NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0),
    estado VARCHAR(30) NOT NULL,
    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE cliente (
    id_cliente INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    correo VARCHAR(150) UNIQUE,
    direccion VARCHAR(200)
);

CREATE TABLE venta (
    id_venta INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha DATE NOT NULL,
    total NUMERIC(10,2) NOT NULL CHECK (total >= 0),
    estado VARCHAR(30) NOT NULL,
    id_cliente INT NOT NULL,
    id_usuario INT NOT NULL,
    CONSTRAINT fk_venta_cliente
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_venta_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE detalle_venta (
    id_detalle INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0),
    subtotal NUMERIC(10,2) NOT NULL CHECK (subtotal >= 0),
    CONSTRAINT uq_detalle_venta_producto UNIQUE (id_venta, id_producto),
    CONSTRAINT fk_detalle_venta
        FOREIGN KEY (id_venta) REFERENCES venta(id_venta)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_detalle_producto
        FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE movimiento_inventario (
    id_movimiento INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    tipo_movimiento VARCHAR(30) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    motivo VARCHAR(200),
    precio_venta NUMERIC(10,2) CHECK (precioventa >= 0),
    CONSTRAINT fk_movimiento_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_movimiento_producto
        FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE tarea (
    id_tarea INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_limite DATE,
    estado VARCHAR(30) NOT NULL,
    prioridad VARCHAR(20) NOT NULL,
    CONSTRAINT fk_tarea_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE reporte (
    id_reporte INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    fecha_generacion DATE NOT NULL,
    periodo VARCHAR(50) NOT NULL,
    formato VARCHAR(20) NOT NULL
);

CREATE TABLE alerta (
    id_alerta INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_producto INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha DATE NOT NULL,
    estado VARCHAR(30) NOT NULL,
    CONSTRAINT fk_alerta_producto
        FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE empleado (
    id_empleado INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    cargo VARCHAR(100) NOT NULL,
    CONSTRAINT fk_empleado_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE horas_empleado (
    id_empleado INT NOT NULL,
    fecha DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME NOT NULL,
    horas_trabajadas NUMERIC(5,2) NOT NULL CHECK (horas_trabajadas >= 0),
    PRIMARY KEY (id_empleado, fecha),
    CONSTRAINT fk_horas_empleado
        FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT chk_horas_empleado_rango
        CHECK (hora_salida >= hora_entrada)
);

CREATE TABLE empleado_rol (
    id_empleado INT NOT NULL,
    id_rol INT NOT NULL,
    PRIMARY KEY (id_empleado, id_rol),
    CONSTRAINT fk_empleado_rol_empleado
        FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_empleado_rol_rol
        FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);