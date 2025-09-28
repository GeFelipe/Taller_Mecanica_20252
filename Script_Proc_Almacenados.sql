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