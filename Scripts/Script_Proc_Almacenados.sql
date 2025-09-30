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


