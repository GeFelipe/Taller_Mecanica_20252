--Procedimiento para consultar la tabla cliente
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_datos_cliente (
    IN id_param INT
)
BEGIN
    SELECT 
        ClienteID, 
        Nombre, 
        Apellido, 
        Telefono, 
        Email, 
        Direccion, 
        FechaRegistro
    FROM 
        cliente
    WHERE 
        ClienteID = id_param;
END$$

DELIMITER ;

--Procedimiento para agregar nuevo cliente

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE agregar_nuevo_cliente (
    IN nombre_param VARCHAR(100),
    IN apellido_param VARCHAR(100),
    IN telefono_param VARCHAR(20),
    IN email_param VARCHAR(100),
    IN direccion_param VARCHAR(200)
)
BEGIN
    INSERT INTO 
        cliente (Nombre, Apellido, Telefono, Email, Direccion)
    VALUES 
        (nombre_param, apellido_param, telefono_param, email_param, direccion_param);
END$$

DELIMITER ;

-- Procedimiento para actualizar contacto de un cliente

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE actualizar_contacto_cliente (
    IN id_param INT,
    IN telefono_param VARCHAR(20),
    IN direccion_param VARCHAR(200)
)
BEGIN
    UPDATE 
        cliente
    SET 
        Telefono = telefono_param,
        Direccion = direccion_param
    WHERE 
        ClienteID = id_param;
END$$

DELIMITER ;

-- Procedimiento para eliminar un cliente

USE taller_mecanica
DELIMITER $$

CREATE PROCEDURE eliminar_cliente (
    IN id_param INT
)
BEGIN
    DELETE FROM cliente
    WHERE ClienteID = id_param;
END$$

DELIMITER ;

-- Procedimiento para Crear Cita 

USE taller_mecanica;
DELIMITER $$

-- Procedimiento para crear una nueva cita
CREATE PROCEDURE agregar_nueva_cita (
    IN cliente_id_param INT,
    IN vehiculo_id_param INT,
    IN fecha_hora_param DATETIME,
    IN motivo_param VARCHAR(200)
)
BEGIN
    INSERT INTO 
        Cita (ClienteID, VehiculoID, FechaHora, Motivo)
    VALUES 
        (cliente_id_param, vehiculo_id_param, fecha_hora_param, motivo_param);
END$$

-- Procedimiento para obtener citas por cliente
CREATE PROCEDURE obtener_citas_cliente (
    IN cliente_id INT
)
BEGIN
    SELECT 
        c.CitaID,
        c.FechaHora,
        c.Motivo,
        c.Estado,
        v.Placa AS Vehiculo
    FROM 
        Cita c
        INNER JOIN Vehiculo v ON c.VehiculoID = v.VehiculoID
    WHERE 
        c.ClienteID = cliente_id
    ORDER BY c.FechaHora DESC;
END$$

DELIMITER ;

-- Procedimiento para actualizar el estado de una cita
CREATE PROCEDURE actualizar_estado_cita (
    IN cita_id INT,
    IN estado VARCHAR(50)
)
BEGIN
    UPDATE 
        Cita
    SET 
        Estado = estado
    WHERE 
        CitaID = cita_id;
END$$

-- Procedimiento para eliminar una cita
CREATE PROCEDURE eliminar_cita (
    IN cita_id INT
)
BEGIN
    DELETE FROM Cita
    WHERE CitaID = cita_id;
END$$

DELIMITER ;


--Procedimiento para crear nueva orden de trabajo

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE crear_orden_trabajo (
    IN cita_id INT,
    IN empleado_id INT,
    IN observaciones VARCHAR(300)
)
BEGIN
    DECLARE nuevo_orden_id INT;
    DECLARE vehiculo_id INT;

    -- Creamos la ordenn de trabajo
    INSERT INTO ordentrabajo (CitaID, EmpleadoID, FechaInicio, Estado)
    VALUES (cita_id, empleado_id, NOW(), 'En Proceso');

    --Obtenemos el id del insert que acabamos de ejecutar
    SET nuevo_orden_id = LAST_INSERT_ID();

    -- Obtenemos el vehículo asociado a la cita
    SELECT VehiculoID INTO vehiculo_id 
    FROM cita 
    WHERE CitaID = cita_id;

    -- Registramos la orden trabajo en el historial de vehículo
    INSERT INTO historialvehiculo (VehiculoID, OrdenTrabajoID, Observaciones, FechaRegistro)
    VALUES (vehiculo_id, nuevo_orden_id, observaciones, NOW());
END$$

DELIMITER ;

--Procedimiento para agregar detalle de mano de obra

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE agregar_detalle_trabajo (
    IN orden_trabajo_id INT,
    IN descripcion VARCHAR(200),
    IN horas DECIMAL(5,2),
    IN costo DECIMAL(10,2)
)
BEGIN
    INSERT INTO detalletrabajo (OrdenTrabajoID, Descripcion, ManoDeObraHoras, CostoManoDeObra)
    VALUES (orden_trabajo_id, descripcion, horas, costo);
END$$

DELIMITER ;

--Procedimiento para agregar repuesto a orden

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE agregar_repuesto_a_orden (
    IN orden_trabajo_id INT,
    IN repuesto_id INT,
    IN cantidad INT
)
BEGIN
    DECLARE precio_unitario DECIMAL(10,2);

    -- Obtenemos el precio por unidad del repuesto
    SELECT PrecioUnitario INTO precio_unitario
    FROM repuesto
    WHERE RepuestoID = repuesto_id;

    -- Insertamos el detalle del repuesto dentro de la orden de trabajo
    INSERT INTO ordentrabajorepuesto (OrdenTrabajoID, RepuestoID, Cantidad, PrecioUnitario)
    VALUES (orden_trabajo_id, repuesto_id, cantidad, precio_unitario);

    -- Actualizamos el inventarion - reduciendo el stiock por el repuesto que sacamos
    UPDATE repuesto
    SET StockActual = StockActual - cantidad
    WHERE RepuestoID = repuesto_id;

    -- Registramos la salida del respuesto.
    INSERT INTO inventariomovimiento (RepuestoID, TipoMovimiento, Cantidad, FechaMovimiento)
    VALUES (repuesto_id, 'Salida', cantidad, NOW());
END$$

DELIMITER ;

--Procedimiento para agregar servicio a orden

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE agregar_servicio_a_orden (
    IN orden_trabajo_id INT,
    IN servicio_id INT,
    IN cantidad INT
)
BEGIN
    DECLARE precio_base DECIMAL(10,2);

    SELECT PrecioBase INTO precio_base
    FROM servicio
    WHERE ServicioID = servicio_id;

    INSERT INTO ordentrabajoservicio (OrdenTrabajoID, ServicioID, Cantidad, PrecioUnitario)
    VALUES (orden_trabajo_id, servicio_id, cantidad, precio_base);
END$$

DELIMITER ;

--Procedimiento para marcar como finalizada una orden de trabajo (cambiamos el estado de la orden a finalizada) - una posible mejora es crear una tabla de estados de orden para no tener código quemado.

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE finalizar_orden_trabajo (
    IN orden_trabajo_id INT,
    IN observaciones VARCHAR(300)
)
BEGIN
    DECLARE vehiculo_id INT;

    -- Actualizamos estado y fecha de la orden
    UPDATE ordentrabajo
    SET Estado = 'Finalizada',
        FechaFin = NOW()
    WHERE OrdenTrabajoID = orden_trabajo_id;

    -- Obtenemos el vehículo asociado
    SELECT c.VehiculoID INTO vehiculo_id
    FROM ordentrabajo o
    JOIN cita c ON o.CitaID = c.CitaID
    WHERE o.OrdenTrabajoID = orden_trabajo_id;

    -- Registrar en historial
    INSERT INTO historialvehiculo (VehiculoID, OrdenTrabajoID, Observaciones, FechaRegistro)
    VALUES (vehiculo_id, orden_trabajo_id, observaciones, NOW());
END$$

DELIMITER ;

-- Procedimiento para consultar orden de servicio completa

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_orden_completa (
    IN orden_trabajo_id INT
)
BEGIN
     SELECT 
        o.OrdenTrabajoID,
        o.FechaInicio,
        o.FechaFin,
        o.Estado,
        c.Nombre AS Cliente,
        v.Placa AS Vehiculo,
        e.Nombre AS Empleado
    FROM ordentrabajo o
    JOIN cita ci ON o.CitaID = ci.CitaID
    JOIN cliente c ON ci.ClienteID = c.ClienteID
    JOIN vehiculo v ON ci.VehiculoID = v.VehiculoID
    LEFT JOIN empleado e ON o.EmpleadoID = e.EmpleadoID
    WHERE o.OrdenTrabajoID = orden_trabajo_id;

    -- Obtenemos detalle de trabajo
    SELECT * FROM detalletrabajo WHERE OrdenTrabajoID = orden_trabajo_id;

    -- Obtenemos repuestos
    SELECT 
        r.Nombre AS Repuesto,
        orp.Cantidad,
        orp.PrecioUnitario
    FROM ordentrabajorepuesto orp
    JOIN repuesto r ON orp.RepuestoID = r.RepuestoID
    WHERE orp.OrdenTrabajoID = orden_trabajo_id;

    -- Obtenemos Servicios
    SELECT 
        s.Nombre AS Servicio,
        os.Cantidad,
        os.PrecioUnitario
    FROM ordentrabajoservicio os
    JOIN servicio s ON os.ServicioID = s.ServicioID
    WHERE os.OrdenTrabajoID = orden_trabajo_id;
END$$

DELIMITER ;
 
-- Procedimiento para generar factura desde una orden de trabajo

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE generar_factura_desde_orden (
    IN orden_trabajo_id INT
)
BEGIN
    DECLARE subtotal DECIMAL(10,2);
    DECLARE iva DECIMAL(10,2);
    DECLARE total DECIMAL(10,2);

    -- Calculamo el subtotal sumando mano de obra - repuestos - servicios)
    SELECT 
        IFNULL(SUM(CostoManoDeObra),0)
        + IFNULL((SELECT SUM(Cantidad * PrecioUnitario) FROM ordentrabajorepuesto WHERE OrdenTrabajoID = orden_trabajo_id),0)
        + IFNULL((SELECT SUM(Cantidad * PrecioUnitario) FROM ordentrabajoservicio WHERE OrdenTrabajoID = orden_trabajo_id),0)
    INTO subtotal
    FROM detalletrabajo
    WHERE OrdenTrabajoID = orden_trabajo_id;

    SET iva = subtotal * 0.19;
    SET total = subtotal + iva;

    -- Insertamos la factura
    INSERT INTO factura (OrdenTrabajoID, FechaEmision, Subtotal, IVA, Total)
    VALUES (orden_trabajo_id, NOW(), subtotal, iva, total);
END$$

DELIMITER ;

-- Procedimiento para registrar un pago

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE registrar_pago (
    IN factura_id INT,
    IN monto DECIMAL(10,2),
    IN metodo ENUM('Efectivo','Tarjeta','Transferencia')
)
BEGIN
    INSERT INTO pago (FacturaID, Monto, FechaPago, MetodoPago)
    VALUES (factura_id, monto, NOW(), metodo);
END$$

DELIMITER ;

-- Procedimiento para eliminar un pago 

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE eliminar_pago (
    IN pago_id INT
)
BEGIN
    DELETE FROM Pago
    WHERE PagoID = pago_id;
END$$

DELIMITER ;

-- Procedimiento para obtener pagos por factura
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_pagos_por_factura (
    IN factura_id INT
)
BEGIN
    SELECT 
        p.PagoID,
        p.FacturaID,
        f.FechaEmision,
        p.Monto,
        p.FechaPago,
        p.MetodoPago
    FROM 
        Pago p
    INNER JOIN 
        Factura f ON p.FacturaID = f.FacturaID
    WHERE 
        p.FacturaID = factura_id;
END$$

DELIMITER ;

-- Procedimiento para actualizar un pago
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE actualizar_pago (
    IN pago_id INT,
    IN nuevo_monto DECIMAL(10,2),
    IN nuevo_metodo ENUM('Efectivo','Tarjeta','Transferencia')
)
BEGIN
    UPDATE Pago
    SET 
        Monto = nuevo_monto,
        MetodoPago = nuevo_metodo,
        FechaPago = NOW()
    WHERE 
        PagoID = pago_id;
END$$

DELIMITER ;

--Procedimiento para obtener historial de un vehículo

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_historial_vehiculo_por_id (
    IN vehiculo_id INT
)
BEGIN
    SELECT 
        v.VehiculoID,
        v.Placa,
        v.Marca,
        v.Modelo,
        v.Anio,
        v.Color,
        c.ClienteID,
        CONCAT(c.Nombre, ' ', c.Apellido) AS NombreCliente,
        c.Telefono AS TelefonoCliente,
        c.Email AS EmailCliente,
        c.Direccion AS DireccionCliente,
        o.OrdenTrabajoID,
        o.FechaInicio,
        o.FechaFin,
        o.Estado AS EstadoOrden,
        e.EmpleadoID,
        CONCAT(e.Nombre, ' ', e.Apellido) AS EmpleadoAsignado,
        h.HistorialID,
        h.Observaciones,
        h.FechaRegistro AS FechaHistorial,
        ct.CitaID,
        ct.FechaHora,
        ct.Motivo,
        ct.Estado AS EstadoCita
    FROM 
        vehiculo v
        INNER JOIN cliente c ON v.ClienteID = c.ClienteID
        LEFT JOIN historialvehiculo h ON v.VehiculoID = h.VehiculoID
        LEFT JOIN ordentrabajo o ON h.OrdenTrabajoID = o.OrdenTrabajoID
        LEFT JOIN empleado e ON o.EmpleadoID = e.EmpleadoID
        LEFT JOIN cita ct ON v.VehiculoID = ct.VehiculoID
    WHERE 
        v.VehiculoID = vehiculo_id
    ORDER BY 
        h.FechaRegistro DESC, o.FechaInicio DESC;
END$$

DELIMITER ;

-- Procedimiento para obtener todos los historiales

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_historiales_todos_vehiculos ()
BEGIN
    SELECT 
        v.VehiculoID,
        v.Placa,
        v.Marca,
        v.Modelo,
        v.Anio,
        v.Color,
        c.ClienteID,
        CONCAT(c.Nombre, ' ', c.Apellido) AS NombreCliente,
        o.OrdenTrabajoID,
        o.FechaInicio,
        o.FechaFin,
        o.Estado AS EstadoOrden,
        e.EmpleadoID,
        CONCAT(e.Nombre, ' ', e.Apellido) AS EmpleadoAsignado,
        h.Observaciones,
        h.FechaRegistro,
        ct.FechaHora AS FechaCita,
        ct.Motivo AS MotivoCita
    FROM 
        vehiculo v
        INNER JOIN cliente c ON v.ClienteID = c.ClienteID
        LEFT JOIN historialvehiculo h ON v.VehiculoID = h.VehiculoID
        LEFT JOIN ordentrabajo o ON h.OrdenTrabajoID = o.OrdenTrabajoID
        LEFT JOIN empleado e ON o.EmpleadoID = e.EmpleadoID
        LEFT JOIN cita ct ON v.VehiculoID = ct.VehiculoID
    ORDER BY 
        v.VehiculoID, h.FechaRegistro DESC;
END$$

DELIMITER ;


-- Procedimiento para crear registros de vehículos

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE crear_vehiculo (
    IN cliente_id_param INT,
    IN placa_param VARCHAR(20),
    IN marca_param VARCHAR(50),
    IN modelo_param VARCHAR(50),
    IN anio_param INT,
    IN vin_param VARCHAR(50),
    IN color_param VARCHAR(30)
)
BEGIN
    INSERT INTO 
        Vehiculo (ClienteID, Placa, Marca, Modelo, Anio, VIN, Color)
    VALUES 
        (cliente_id_param, placa_param, marca_param, modelo_param, anio_param, vin_param, color_param);
END$$

DELIMITER ;

-- Procedimiento para modificar un registro de vehículo

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE modificar_vehiculo (
    IN vehiculo_id_param INT,
    IN cliente_id_param INT,
    IN placa_param VARCHAR(20),
    IN marca_param VARCHAR(50),
    IN modelo_param VARCHAR(50),
    IN anio_param INT,
    IN vin_param VARCHAR(50),
    IN color_param VARCHAR(30)
)
BEGIN
    UPDATE 
        Vehiculo
    SET 
        ClienteID = cliente_id_param,
        Placa = placa_param,
        Marca = marca_param,
        Modelo = modelo_param,
        Anio = anio_param,
        VIN = vin_param,
        Color = color_param
    WHERE 
        VehiculoID = vehiculo_id_param;
END$$

DELIMITER ;

-- Procedimiento para consultar el registro de un vehículo

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_vehiculo_por_id (
    IN vehiculo_id_param INT
)
BEGIN
    SELECT 
        VehiculoID, 
        ClienteID, 
        Placa, 
        Marca, 
        Modelo, 
        Anio, 
        VIN, 
        Color
    FROM 
        Vehiculo
    WHERE 
        VehiculoID = vehiculo_id_param;
END$$

DELIMITER ;

-- Procedimiento para eliminar un vehículo

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE eliminar_vehiculo (
    IN vehiculo_id_param INT
)
BEGIN
    DELETE FROM 
        Vehiculo
    WHERE 
        VehiculoID = vehiculo_id_param;
END$$

DELIMITER ;

--Procedimiento almacenado para insertar un servicio

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE crear_servicio (
    IN nombre_param VARCHAR(100),
    IN descripcion_param VARCHAR(200),
    IN precio_base_param DECIMAL(10,2)
)
BEGIN
    INSERT INTO 
        Servicio (Nombre, Descripcion, PrecioBase)
    VALUES 
        (nombre_param, descripcion_param, precio_base_param);
END$$

DELIMITER ;

--Procedimiento almacenado para obtener un servicio

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_servicio_por_id (
    IN servicio_id_param INT
)
BEGIN
    SELECT 
        ServicioID, 
        Nombre, 
        Descripcion, 
        PrecioBase
    FROM 
        Servicio
    WHERE 
        ServicioID = servicio_id_param;
END$$

DELIMITER ;

--Procedimiento almacenado para actualizar un servicio

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE modificar_servicio (
    IN servicio_id_param INT,
    IN nombre_param VARCHAR(100),
    IN descripcion_param VARCHAR(200),
    IN precio_base_param DECIMAL(10,2)
)
BEGIN
    UPDATE 
        Servicio
    SET 
        Nombre = nombre_param,
        Descripcion = descripcion_param,
        PrecioBase = precio_base_param
    WHERE 
        ServicioID = servicio_id_param;
END$$

DELIMITER ;

-- Procedimiento almacenado para eliminar un servicio

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE eliminar_servicio (
    IN servicio_id_param INT
)
BEGIN
    DELETE FROM 
        Servicio
    WHERE 
        ServicioID = servicio_id_param;
END$$

DELIMITER ;

--Procedimiento almacenado para crear respuesto

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE crear_repuesto (
    IN proveedor_id_param INT,
    IN nombre_param VARCHAR(100),
    IN descripcion_param VARCHAR(200),
    IN precio_unitario_param DECIMAL(10,2),
    IN stock_actual_param INT
)
BEGIN
    INSERT INTO 
        Repuesto (ProveedorID, Nombre, Descripcion, PrecioUnitario, StockActual)
    VALUES 
        (proveedor_id_param, nombre_param, descripcion_param, precio_unitario_param, stock_actual_param);
END$$

DELIMITER ;

--Procedimiento para consultar un respuesto

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_repuesto_por_id (
    IN repuesto_id_param INT
)
BEGIN
    SELECT 
        RepuestoID, 
        ProveedorID, 
        Nombre, 
        Descripcion, 
        PrecioUnitario, 
        StockActual
    FROM 
        Repuesto
    WHERE 
        RepuestoID = repuesto_id_param;
END$$

DELIMITER ;

--Procedimiento para modificar un repuesto
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE modificar_repuesto (
    IN repuesto_id_param INT,
    IN proveedor_id_param INT,
    IN nombre_param VARCHAR(100),
    IN descripcion_param VARCHAR(200),
    IN precio_unitario_param DECIMAL(10,2),
    IN stock_actual_param INT
)
BEGIN
    UPDATE 
        Repuesto
    SET 
        ProveedorID = proveedor_id_param,
        Nombre = nombre_param,
        Descripcion = descripcion_param,
        PrecioUnitario = precio_unitario_param,
        StockActual = stock_actual_param
    WHERE 
        RepuestoID = repuesto_id_param;
END$$

DELIMITER ;

--Procedimiento para eliminar un repuesto
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE eliminar_repuesto (
    IN repuesto_id_param INT
)
BEGIN
    DELETE FROM 
        Repuesto
    WHERE 
        RepuestoID = repuesto_id_param;
END$$

DELIMITER ;

-- Procedimiento para crear un proveedor

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE crear_proveedor (
    IN nombre_param VARCHAR(100),
    IN telefono_param VARCHAR(20),
    IN email_param VARCHAR(100),
    IN direccion_param VARCHAR(200)
)
BEGIN
    INSERT INTO 
        Proveedor (Nombre, Telefono, Email, Direccion)
    VALUES 
        (nombre_param, telefono_param, email_param, direccion_param);
END$$

DELIMITER ;

--Procedimiento para consultar un proveedor

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_proveedor_por_id (
    IN proveedor_id_param INT
)
BEGIN
    SELECT 
        ProveedorID, 
        Nombre, 
        Telefono, 
        Email, 
        Direccion
    FROM 
        Proveedor
    WHERE 
        ProveedorID = proveedor_id_param;
END$$

DELIMITER ;

--Procedimiento para modificar un proveedor

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE modificar_proveedor (
    IN proveedor_id_param INT,
    IN nombre_param VARCHAR(100),
    IN telefono_param VARCHAR(20),
    IN email_param VARCHAR(100),
    IN direccion_param VARCHAR(200)
)
BEGIN
    UPDATE 
        Proveedor
    SET 
        Nombre = nombre_param,
        Telefono = telefono_param,
        Email = email_param,
        Direccion = direccion_param
    WHERE 
        ProveedorID = proveedor_id_param;
END$$

DELIMITER ;

--Procedimiento para eliminar un proveedor

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE eliminar_proveedor (
    IN proveedor_id_param INT
)
BEGIN
    DELETE FROM 
        Proveedor
    WHERE 
        ProveedorID = proveedor_id_param;
END$$

DELIMITER ;

--Procedimiento para crear factura

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE crear_factura (
    IN orden_trabajo_id_param INT,
    IN subtotal_param DECIMAL(10,2),
    IN iva_param DECIMAL(10,2),
    IN total_param DECIMAL(10,2)
)
BEGIN
    INSERT INTO 
        Factura (OrdenTrabajoID, Subtotal, IVA, Total)
    VALUES 
        (orden_trabajo_id_param, subtotal_param, iva_param, total_param);
END$$

DELIMITER ;

--Procedimiento para consultar factura

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_factura_por_id (
    IN factura_id_param INT
)
BEGIN
    SELECT 
        FacturaID, 
        OrdenTrabajoID, 
        FechaEmision, 
        Subtotal, 
        IVA, 
        Total
    FROM 
        Factura
    WHERE 
        FacturaID = factura_id_param;
END$$

DELIMITER ;

--Procedimiento para modificar factura

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE modificar_factura (
    IN factura_id_param INT,
    IN subtotal_param DECIMAL(10,2),
    IN iva_param DECIMAL(10,2),
    IN total_param DECIMAL(10,2)
)
BEGIN
    UPDATE 
        Factura
    SET 
        Subtotal = subtotal_param,
        IVA = iva_param,
        Total = total_param
    WHERE 
        FacturaID = factura_id_param;
END$$

DELIMITER ;

--Procedimiento para eliminar factura

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE eliminar_factura (
    IN factura_id_param INT
)
BEGIN
    DELETE FROM 
        Factura
    WHERE 
        FacturaID = factura_id_param;
END$$

DELIMITER ;

-- Procedimiento para crear un empleado
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE crear_empleado (
    IN nombre_param VARCHAR(100),
    IN apellido_param VARCHAR(100),
    IN cargo_param VARCHAR(50),
    IN telefono_param VARCHAR(20),
    IN email_param VARCHAR(100),
    IN fecha_contratacion_param DATE
)
BEGIN
    INSERT INTO 
        Empleado (Nombre, Apellido, Cargo, Telefono, Email, FechaContratacion)
    VALUES 
        (nombre_param, apellido_param, cargo_param, telefono_param, email_param, fecha_contratacion_param);
END$$

DELIMITER ;

-- Procedimiento para obtener un empleado por ID
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_empleado_por_id (
    IN empleado_id_param INT
)
BEGIN
    SELECT 
        EmpleadoID, 
        Nombre, 
        Apellido, 
        Cargo, 
        Telefono, 
        Email, 
        FechaContratacion
    FROM 
        Empleado
    WHERE 
        EmpleadoID = empleado_id_param;
END$$

DELIMITER ;

-- Procedimiento para modificar un empleado
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE modificar_empleado (
    IN empleado_id_param INT,
    IN nombre_param VARCHAR(100),
    IN apellido_param VARCHAR(100),
    IN cargo_param VARCHAR(50),
    IN telefono_param VARCHAR(20),
    IN email_param VARCHAR(100),
    IN fecha_contratacion_param DATE
)
BEGIN
    UPDATE 
        Empleado
    SET 
        Nombre = nombre_param,
        Apellido = apellido_param,
        Cargo = cargo_param,
        Telefono = telefono_param,
        Email = email_param,
        FechaContratacion = fecha_contratacion_param
    WHERE 
        EmpleadoID = empleado_id_param;
END$$

DELIMITER ;

-- Procedimiento para eliminar un empleado
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE eliminar_empleado (
    IN empleado_id_param INT
)
BEGIN
    DELETE FROM 
        Empleado
    WHERE 
        EmpleadoID = empleado_id_param;
END$$

DELIMITER ;

-- Procedimiento para obtener todos los empleados - sok
USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_todos_empleados ()
BEGIN
    SELECT 
        EmpleadoID, 
        Nombre, 
        Apellido, 
        Cargo, 
        Telefono, 
        Email, 
        FechaContratacion
    FROM 
        Empleado;
END$$

DELIMITER ;


--Procedimiento para obtener mano de obra por orden
DELIMITER $$
CREATE PROCEDURE obtener_mano_obra_por_orden(IN p_orden_id INT)
BEGIN
    SELECT 
        DetalleTrabajoID,
        Descripcion,
        ManoDeObraHoras,
        CostoManoDeObra
    FROM DetalleTrabajo
    WHERE OrdenTrabajoID = p_orden_id;
END$$
DELIMITER ;

--Procedimiento para obtener respuestos por orden
DELIMITER $$
CREATE PROCEDURE obtener_repuestos_por_orden(IN p_orden_id INT)
BEGIN
    SELECT 
        otr.OrdenTrabajoRepuestoID,
        r.RepuestoID,
        r.Nombre,
        otr.Cantidad,
        otr.PrecioUnitario
    FROM OrdenTrabajoRepuesto otr
    INNER JOIN Repuesto r ON r.RepuestoID = otr.RepuestoID
    WHERE otr.OrdenTrabajoID = p_orden_id;
END$$
DELIMITER ;

--Procedimiento para obtener servicios por orden
DELIMITER $$
CREATE PROCEDURE obtener_servicios_por_orden(IN p_orden_id INT)
BEGIN
    SELECT 
        ots.OrdenTrabajoServicioID,
        s.ServicioID,
        s.Nombre,
        ots.Cantidad,
        ots.PrecioUnitario
    FROM OrdenTrabajoServicio ots
    INNER JOIN Servicio s ON s.ServicioID = ots.ServicioID
    WHERE ots.OrdenTrabajoID = p_orden_id;
END$$
DELIMITER ;

--Procedimiento para actualizar mano de obra
DELIMITER $$
CREATE PROCEDURE actualizar_detalle_trabajo(
    IN p_detalle_id INT,
    IN p_descripcion VARCHAR(200),
    IN p_horas DECIMAL(5,2),
    IN p_costo DECIMAL(10,2)
)
BEGIN
    UPDATE DetalleTrabajo
    SET 
        Descripcion = p_descripcion,
        ManoDeObraHoras = p_horas,
        CostoManoDeObra = p_costo
    WHERE DetalleTrabajoID = p_detalle_id;
END$$
DELIMITER ;


--Procedimiento para eliminar cualquier detalle de la orden de trabajo (mano de obra/repuesto/servicio)
DELIMITER $$
CREATE PROCEDURE eliminar_detalle_orden(IN p_detalle_id INT)
BEGIN
    -- Eliminar mano de obra si existe
    DELETE FROM DetalleTrabajo
    WHERE DetalleTrabajoID = p_detalle_id;

    -- Eliminar repuesto si existe
    DELETE FROM OrdenTrabajoRepuesto
    WHERE OrdenTrabajoRepuestoID = p_detalle_id;

    -- Eliminar servicio si existe
    DELETE FROM OrdenTrabajoServicio
    WHERE OrdenTrabajoServicioID = p_detalle_id;
END$$
DELIMITER ;


--Procedimiento para actualizar repuesto en una orden
DELIMITER $$

CREATE PROCEDURE actualizar_repuesto_orden (
    IN p_detalle_id INT,
    IN p_cantidad INT
)
BEGIN
    UPDATE OrdenTrabajoRepuesto
    SET Cantidad = p_cantidad
    WHERE OrdenTrabajoRepuestoID = p_detalle_id;
END$$

DELIMITER ;

--Procedimiento para actualizar servicio en una orden
DELIMITER $$

CREATE PROCEDURE actualizar_servicio_orden (
    IN p_detalle_id INT,
    IN p_cantidad INT
)
BEGIN
    UPDATE OrdenTrabajoServicio
    SET Cantidad = p_cantidad
    WHERE OrdenTrabajoServicioID = p_detalle_id;
END$$

DELIMITER ;
