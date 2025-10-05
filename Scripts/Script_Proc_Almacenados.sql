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

CREATE PROCEDURE agregar_nueva_cita (
    IN cliente_id_param INT,
    IN vehiculo_id_param INT,
    IN empleado_id_param INT,
    IN fecha_cita_param DATETIME,
    IN descripcion_param VARCHAR(255)
)
BEGIN
    INSERT INTO 
        Cita (ClienteID, VehiculoID, EmpleadoID, FechaCita, Descripcion)
    VALUES 
        (cliente_id_param, vehiculo_id_param, empleado_id_param, fecha_cita_param, descripcion_param);
END$$

DELIMITER ;

-- Procedimiento para obtener citas por cliente

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_citas_cliente (
    IN cliente_id INT
)
BEGIN
    SELECT 
        c.CitaID,
        c.FechaCita,
        c.Descripcion,
        c.Estado,
        v.Placa AS Vehiculo,
        e.Nombre AS EmpleadoNombre,
        e.Apellido AS EmpleadoApellido
    FROM 
        Cita c
        INNER JOIN Vehiculo v ON c.VehiculoID = v.VehiculoID
        LEFT JOIN Empleado e ON c.EmpleadoID = e.EmpleadoID
    WHERE 
        c.ClienteID = cliente_id
    ORDER BY c.FechaCita DESC;
END$$

DELIMITER ;

-- Procedimiento para actualizarestado de la cita 

USE taller_mecanica;
DELIMITER $$

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

DELIMITER ;

-- Procedimiento para eliminar cita 

USE taller_mecanica;
DELIMITER $$

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
    IN descripcion_param VARCHAR(200),
    IN horas_param DECIMAL(5,2),
    IN costo_param DECIMAL(10,2)
)
BEGIN
    INSERT INTO detalletrabajo (OrdenTrabajoID, Descripcion, ManoDeObraHoras, CostoManoDeObra)
    VALUES (orden_trabajo_id, descripcion_param, horas_param, costo_param);
END$$

DELIMITER ;

--Procedimiento para agregar repuesto a orden

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE agregar_repuesto_a_orden (
    IN orden_trabajo_id INT,
    IN repuesto_id INT,
    IN cantidad_param INT
)
BEGIN
    DECLARE precio_unitario DECIMAL(10,2);

    -- Obtenemos el precio por unidad del repuesto
    SELECT PrecioUnitario INTO precio_unitario
    FROM repuesto
    WHERE RepuestoID = repuesto_id;

    -- Insertamos el detalle del repuesto dentro de la orden de trabajo
    INSERT INTO ordentrabajarepuesto (OrdenTrabajoID, RepuestoID, Cantidad, PrecioUnitario)
    VALUES (orden_trabajo_id, repuesto_id, cantidad_param, precio_unitario);

    -- Actualizamos el inventarion - reduciendo el stiock por el repuesto que sacamos
    UPDATE repuesto
    SET StockActual = StockActual - cantidad_param
    WHERE RepuestoID = repuesto_id;

    -- Registramos la salida del respuesto.
    INSERT INTO inventariomovimiento (RepuestoID, TipoMovimiento, Cantidad, FechaMovimiento)
    VALUES (repuesto_id, 'Salida', cantidad_param, NOW());
END$$

DELIMITER ;

--Procedimiento para agregar servicio a orden

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE agregar_servicio_a_orden (
    IN orden_trabajo_id INT,
    IN servicio_id INT,
    IN cantidad_param INT
)
BEGIN
    DECLARE precio_base DECIMAL(10,2);

    SELECT PrecioBase INTO precio_base
    FROM servicio
    WHERE ServicioID = servicio_id;

    INSERT INTO ordentrabajoservicio (OrdenTrabajoID, ServicioID, Cantidad, PrecioUnitario)
    VALUES (orden_trabajo_id, servicio_id, cantidad_param, precio_base);
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
    FROM ordentrabajarepuesto orp
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
        + IFNULL((SELECT SUM(Cantidad * PrecioUnitario) FROM ordentrabajarepuesto WHERE OrdenTrabajoID = orden_trabajo_id),0)
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
    IN monto_param DECIMAL(10,2),
    IN metodo_param ENUM('Efectivo','Tarjeta','Transferencia')
)
BEGIN
    INSERT INTO pago (FacturaID, Monto, FechaPago, MetodoPago)
    VALUES (factura_id, monto_param, NOW(), metodo_param);
END$$

DELIMITER ;

--Procedimiento para obtener historial de un vehículo

USE taller_mecanica;
DELIMITER $$

CREATE PROCEDURE obtener_historial_vehiculo_por_id (
    IN vehiculo_id_param INT
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
        v.VehiculoID = vehiculo_id_param
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


