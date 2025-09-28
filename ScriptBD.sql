-- Crear base de datos
CREATE DATABASE IF NOT EXISTS Taller_Mecanica;
USE Taller_Mecanica;

-- Crear usuario
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin1234';

-- Tabla Cliente
CREATE TABLE Cliente (
    ClienteID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Telefono VARCHAR(20),
    Email VARCHAR(100),
    Direccion VARCHAR(200),
    FechaRegistro DATE DEFAULT CURRENT_DATE --Modificar por CURRENT_TIMESTAMP ?
);

-- Tabla Vehiculo
CREATE TABLE Vehiculo (
    VehiculoID INT AUTO_INCREMENT PRIMARY KEY,
    ClienteID INT,
    Placa VARCHAR(20) UNIQUE NOT NULL,
    Marca VARCHAR(50),
    Modelo VARCHAR(50),
    Anio INT,
    VIN VARCHAR(50),
    Color VARCHAR(30),
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID)
);

-- Tabla Empleado
CREATE TABLE Empleado (
    EmpleadoID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Cargo VARCHAR(50),
    Telefono VARCHAR(20),
    Email VARCHAR(100),
    FechaContratacion DATE
);

-- Tabla Proveedor
CREATE TABLE Proveedor (
    ProveedorID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Telefono VARCHAR(20),
    Email VARCHAR(100),
    Direccion VARCHAR(200)
);

-- Tabla Repuesto
CREATE TABLE Repuesto (
    RepuestoID INT AUTO_INCREMENT PRIMARY KEY,
    ProveedorID INT,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(200),
    PrecioUnitario DECIMAL(10,2),
    StockActual INT DEFAULT 0,
    FOREIGN KEY (ProveedorID) REFERENCES Proveedor(ProveedorID)
);

-- Tabla InventarioMovimiento
CREATE TABLE InventarioMovimiento (
    MovimientoID INT AUTO_INCREMENT PRIMARY KEY,
    RepuestoID INT,
    TipoMovimiento ENUM('Entrada','Salida'),
    Cantidad INT NOT NULL,
    FechaMovimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (RepuestoID) REFERENCES Repuesto(RepuestoID)
);

-- Tabla Cita
CREATE TABLE Cita (
    CitaID INT AUTO_INCREMENT PRIMARY KEY,
    ClienteID INT,
    VehiculoID INT,
    FechaHora DATETIME NOT NULL,
    Motivo VARCHAR(200),
    Estado ENUM('Pendiente','Atendida','Cancelada') DEFAULT 'Pendiente',
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID),
    FOREIGN KEY (VehiculoID) REFERENCES Vehiculo(VehiculoID)
);

-- Tabla OrdenTrabajo
CREATE TABLE OrdenTrabajo (
    OrdenTrabajoID INT AUTO_INCREMENT PRIMARY KEY,
    CitaID INT,
    EmpleadoID INT,
    FechaInicio DATETIME,
    FechaFin DATETIME,
    Estado ENUM('En Proceso','Finalizada','Cancelada') DEFAULT 'En Proceso',
    FOREIGN KEY (CitaID) REFERENCES Cita(CitaID),
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

-- Tabla DetalleTrabajo
CREATE TABLE DetalleTrabajo (
    DetalleTrabajoID INT AUTO_INCREMENT PRIMARY KEY,
    OrdenTrabajoID INT,
    Descripcion VARCHAR(200),
    ManoDeObraHoras DECIMAL(5,2),
    CostoManoDeObra DECIMAL(10,2),
    FOREIGN KEY (OrdenTrabajoID) REFERENCES OrdenTrabajo(OrdenTrabajoID)
);

-- Tabla OrdenTrabajoRepuesto
CREATE TABLE OrdenTrabajoRepuesto (
    OrdenTrabajoRepuestoID INT AUTO_INCREMENT PRIMARY KEY,
    OrdenTrabajoID INT,
    RepuestoID INT,
    Cantidad INT,
    PrecioUnitario DECIMAL(10,2),
    FOREIGN KEY (OrdenTrabajoID) REFERENCES OrdenTrabajo(OrdenTrabajoID),
    FOREIGN KEY (RepuestoID) REFERENCES Repuesto(RepuestoID)
);

-- Tabla Factura
CREATE TABLE Factura (
    FacturaID INT AUTO_INCREMENT PRIMARY KEY,
    OrdenTrabajoID INT,
    FechaEmision DATETIME DEFAULT CURRENT_TIMESTAMP,
    Subtotal DECIMAL(10,2),
    IVA DECIMAL(10,2),
    Total DECIMAL(10,2),
    FOREIGN KEY (OrdenTrabajoID) REFERENCES OrdenTrabajo(OrdenTrabajoID)
);

-- Tabla Pago
CREATE TABLE Pago (
    PagoID INT AUTO_INCREMENT PRIMARY KEY,
    FacturaID INT,
    Monto DECIMAL(10,2) NOT NULL,
    FechaPago DATETIME DEFAULT CURRENT_TIMESTAMP,
    MetodoPago ENUM('Efectivo','Tarjeta','Transferencia'),
    FOREIGN KEY (FacturaID) REFERENCES Factura(FacturaID)
);

-- Tabla Servicio
CREATE TABLE Servicio (
    ServicioID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(200),
    PrecioBase DECIMAL(10,2)
);

-- Tabla OrdenTrabajoServicio
CREATE TABLE OrdenTrabajoServicio (
    OrdenTrabajoServicioID INT AUTO_INCREMENT PRIMARY KEY,
    OrdenTrabajoID INT,
    ServicioID INT,
    Cantidad INT,
    PrecioUnitario DECIMAL(10,2),
    FOREIGN KEY (OrdenTrabajoID) REFERENCES OrdenTrabajo(OrdenTrabajoID),
    FOREIGN KEY (ServicioID) REFERENCES Servicio(ServicioID)
);

-- Tabla HistorialVehiculo
CREATE TABLE HistorialVehiculo (
    HistorialID INT AUTO_INCREMENT PRIMARY KEY,
    VehiculoID INT,
    OrdenTrabajoID INT,
    Observaciones VARCHAR(300),
    FechaRegistro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (VehiculoID) REFERENCES Vehiculo(VehiculoID),
    FOREIGN KEY (OrdenTrabajoID) REFERENCES OrdenTrabajo(OrdenTrabajoID)
);