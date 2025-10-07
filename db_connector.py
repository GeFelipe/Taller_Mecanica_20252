# Archivo: db_connector.py

import pyodbc
# Importamos la cadena de conexión definida en el archivo de configuración
from config import CONNECTION_STRING 

def execute_stored_procedure(procedure_name, *parameters):
    """
    Establece conexión con MySQL a través de pyodbc y ejecuta un procedimiento 
    almacenado con parámetros variables.
    
    Args:
        procedure_name (str): El nombre del procedimiento almacenado en la base de datos.
        *parameters: Argumentos posicionales que serán pasados al procedimiento.
        
    Returns:
        tuple or None: 
            Si es una consulta (SELECT), devuelve una tupla con (columns, results).
            Si es una modificación (INSERT/UPDATE), devuelve (None, None).
    """
    cnxn = None
    
    try:
        # 1. Establecer la conexión a la base de datos
        cnxn = pyodbc.connect(CONNECTION_STRING)
        cursor = cnxn.cursor()
        print("✅ Conexión establecida con la base de datos 'Taller_Mecanica'.")
        
        # 2. Preparar la sintaxis ODBC {CALL ...}
        # El signo '?' es el marcador de posición para cada parámetro
        placeholders = ', '.join(['?'] * len(parameters))
        sql_call = f"{{CALL {procedure_name}({placeholders})}}"
        
        # 3. Ejecutar el procedimiento almacenado
        print(f"INFO: Ejecutando: {sql_call} con parámetros: {parameters}")
        cursor.execute(sql_call, parameters)
        
        # 4. Intentar obtener resultados (Comprobar si fue un SELECT)
        try:
            results = cursor.fetchall()
            # Si hay resultados, obtenemos los nombres de las columnas
            columns = [col[0] for col in cursor.description]
            return columns, results
        
        except pyodbc.ProgrammingError:
            # Si no fue un SELECT (sino INSERT/UPDATE/DELETE), ocurre un ProgrammingError.
            # En este caso, confirmamos la transacción y no devolvemos resultados.
            cnxn.commit() 
            print("INFO: Operación de modificación completada y confirmada (COMMIT).")
            return None, None
            
    except pyodbc.Error as e:
        # 5. Manejo de Errores
        if cnxn:
            # Si hay un error, revertir cualquier posible cambio pendiente
            cnxn.rollback() 
        print(f"❌ ERROR en la Base de Datos al ejecutar '{procedure_name}': {e}")
        return None, None

    finally:
        # 6. Cerrar la conexión
        if cnxn:
            cnxn.close()
            print("INFO: Conexión cerrada.")

# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'cliente'
# ----------------------------------------------------------------------

def select_cliente(cliente_id):
    """Llama al SP obtener_datos_cliente (Consulta)."""
    print("\n--- INVOCACIÓN: SELECT CLIENTE ---")
    return execute_stored_procedure('obtener_datos_cliente', cliente_id)

def insert_cliente(nombre, apellido, telefono, email, direccion):
    """Llama al SP agregar_nuevo_cliente (Inserción)."""
    print("\n--- INVOCACIÓN: INSERT CLIENTE ---")
    return execute_stored_procedure('agregar_nuevo_cliente', nombre, apellido, telefono, email, direccion)

def update_contacto(cliente_id, telefono, direccion):
    """Llama al SP actualizar_contacto_cliente (Actualización)."""
    print("\n--- INVOCACIÓN: UPDATE CLIENTE ---")
    return execute_stored_procedure('actualizar_contacto_cliente', cliente_id, telefono, direccion)

def eliminar_cliente(cliente_id):
    """Llama al SP eliminar_cliente (Borrado)."""
    print("\n--- INVOCACIÓN: UPDATE CLIENTE ---")
    return execute_stored_procedure('eliminar_cliente', cliente_id)

# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'cita'
# ----------------------------------------------------------------------

def crear_cita(cliente_id, vehiculo_id, fecha_hora, motivo):
    """Llama al SP crear_cita (Inserción)."""
    print("\n--- INVOCACIÓN: INSERT CITA ---")
    return execute_stored_procedure('crear_cita', cliente_id, vehiculo_id, fecha_hora, motivo)

def obtener_cita_por_id(cita_id):
    """Llama al SP obtener_cita_por_id (Consulta)."""
    print("\n--- INVOCACIÓN: OBTENER CITA ---")
    return execute_stored_procedure('obtener_cita_por_id', cita_id)

def actualizar_estado_cita(cita_id, estado):
    """Llama al SP actualizar_estado_cita (Actualización)."""
    print("\n--- INVOCACIÓN: UPDATE ESTADO CITA ---")
    return execute_stored_procedure('actualizar_estado_cita', cita_id, estado)

def eliminar_cita(cita_id):
    """Llama al SP eliminar_cita (Borrado)."""
    print("\n--- INVOCACIÓN: DELETE CITA ---")
    return execute_stored_procedure('eliminar_cita', cita_id)

# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'procedimientos'
# ----------------------------------------------------------------------

def crear_orden_trabajo(cita_id, empleado_id, observaciones):
    """Llamar al SP crear_orden_trabajo"""
    print("\n--- INVOCACIÓN: CREAR ORDEN TRABAJO ---")
    return execute_stored_procedure('crear_orden_trabajo', cita_id, empleado_id, observaciones)

def agregar_detalle_trabajo(orden_trabajo_id, descripcion, horas, costo):
    """Llamar al SP agregar_detalle_trabajo"""
    print("\n--- INVOCACIÓN: AGREGAR DETALLE A ORDEN ---")
    return execute_stored_procedure('agregar_detalle_trabajo', orden_trabajo_id, descripcion, horas, costo)

def agregar_repuesto_orden(orden_trabajo_id, repuesto_id, cantidad):
    """Llamar al SP agregar_repuesto_a_orden"""
    print("\n--- INVOCACIÓN: AGREGAR REPUESTO A ORDEN ---")
    return execute_stored_procedure('agregar_repuesto_a_orden', orden_trabajo_id, repuesto_id, cantidad)

def agregar_servicio_orden(orden_trabajo_id, servicio_id, cantidad):
    """Llamar al SP agregar_servicio_a_orden"""
    print("\n--- INVOCACIÓN: AGREGAR SRVICIO A ORDEN ---")
    return execute_stored_procedure('agregar_servicio_a_orden', orden_trabajo_id, servicio_id, cantidad)

def finalizar_orden_trabjo(orden_trabajo_id, observaciones):
    """Llamar al SP finalizar_orden_trabajo"""
    print("\n--- INVOCACIÓN: FINALIZAR ORDEN ---")
    return execute_stored_procedure('finalizar_orden_trabajo', orden_trabajo_id, observaciones)

def obtener_orden(orden_trabajo_id):
    """Llamar al SP obtener_orden_completa"""
    print("\n--- INVOCACIÓN: OBTENER ORDEN ---")
    return execute_stored_procedure('obtener_orden_completa', orden_trabajo_id)


# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'facturas'
# ----------------------------------------------------------------------

def generar_factura_desde_orden(orden_trabajo_id):
    """Llamar al SP generar_factura_desde_orden"""
    print("\n--- INVOCACIÓN: GENERAR FACTURA ---")
    return execute_stored_procedure('generar_factura_desde_orden', orden_trabajo_id)

# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'pagos'
# ----------------------------------------------------------------------

def registrar_pago(factura_id, monto, metodo):
    """Llamar al SP registrar_pago"""
    print("\n--- INVOCACIÓN: REGISTRAR PAGO ---")
    return execute_stored_procedure('registrar_pago', factura_id, monto, metodo)

def eliminar_pago(pago_id):
    """Llama al SP eliminar_pago (Borrado)."""
    print("\n--- INVOCACIÓN: ELIMINAR PAGO ---")
    return execute_stored_procedure('eliminar_pago', pago_id)

def obtener_pagos_por_factura(factura_id):
    """Llama al SP obtener_pagos_por_factura."""
    print("\n--- INVOCACIÓN: OBTENER PAGOS POR FACTURA ---")
    return execute_stored_procedure('obtener_pagos_por_factura', factura_id)

def actualizar_pago(pago_id, nuevo_monto, nuevo_metodo):
    """Llama al SP actualizar_pago."""
    print("\n--- INVOCACIÓN: ACTUALIZAR PAGO ---")
    return execute_stored_procedure('actualizar_pago', pago_id, nuevo_monto, nuevo_metodo)

# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'Historial'
# ----------------------------------------------------------------------

def obtener_historial_vehiculo_por_id(vehiculo_id):
    """Llamar al SP obtener_historial_vehiculo_por_id"""
    print("\n--- INVOCACIÓN: OBTENER HISTORIAL VEHÍCULO ---")
    return execute_stored_procedure('obtener_historial_vehiculo_por_id', vehiculo_id)

def obtener_historiales_todos_vehiculos():
    """Llamar al SP obtener_historiales_todos_vehiculos"""
    print("\n--- INVOCACIÓN: OBTENER HISTORIAL VEHÍCULOS ---")
    return execute_stored_procedure('obtener_historiales_todos_vehiculos')

# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'vehiculo'
# ----------------------------------------------------------------------

def crear_vehiculo(ClienteID, Placa, Marca, Modelo, Anio, VIN, Color):
    """Llama al SP crear_vehiculo (Inserción)."""
    print("\n--- INVOCACIÓN: INSERT VEHICULO ---")
    return execute_stored_procedure('agregar_nuevo_vehículo', ClienteID, Placa, Marca, Modelo, Anio, VIN, Color)

def modificar_vehiculo(VehiculoID, ClienteID, Placa, Marca, Modelo, Anio, VIN, Color):
    """Llama al SP modificar_vehiculo (Actualización)."""
    print("\n--- INVOCACIÓN: UPDATE VEHICULO ---")
    return execute_stored_procedure('modificar_vehiculo',VehiculoID, ClienteID, Placa, Marca, Modelo, Anio, VIN, Color)

def obtener_vehiculo_por_id(VehiculoID ):
    """Llama al SP obtener_datos_cliente (Consulta)."""
    print("\n--- INVOCACIÓN: SELECT VEHICULO ---")
    return execute_stored_procedure('obtener_vehiculo_por_id',VehiculoID)

def eliminar_vehiculo(VehiculoID):
    """Llama al SP eliminar_vehiculo (Borrado)."""
    print("\n--- INVOCACIÓN: DELETE VEHICULO ---")
    return execute_stored_procedure('eliminar_vehiculo', VehiculoID)


# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'servicio'
# ----------------------------------------------------------------------

def crear_servicio(Nombre ,Descripcion , PrecioBase ):
    """Llama al SP crear_servicio (Inserción)."""
    print("\n--- INVOCACIÓN: INSERT SERVICIO ---")
    return execute_stored_procedure('crear_servicio', Nombre ,Descripcion , PrecioBase)

def obtener_servicio_por_id(ServicioID):
    """Llama al SP obtener_servicio_por_id (Actualización)."""
    print("\n--- INVOCACIÓN: OBTENER SERVICIO ---")
    return execute_stored_procedure('obtener_servicio_por_id',ServicioID)

def modificar_servicio(ServicioID, Nombre ,Descripcion , PrecioBase ):
    """Llama al SP modificar_servicio (Consulta)."""
    print("\n--- INVOCACIÓN: UPDATE SERVICIO ---")
    return execute_stored_procedure('modificar_servicio',ServicioID, Nombre, Descripcion ,PrecioBase )

def eliminar_servicio(ServicioID):
    """Llama al SP eliminar_servicio (Borrado)."""
    print("\n--- INVOCACIÓN: DELETE SERVICIO ---")
    return execute_stored_procedure('eliminar_servicio', ServicioID)


# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'repuesto'
# ----------------------------------------------------------------------

def crear_repuesto(proveedor_id, nombre, descripcion, precio_unitario, stock_actual):
    """Llama al SP crear_repuesto (Inserción)."""
    print("\n--- INVOCACIÓN: INSERT REPUESTO ---")
    return execute_stored_procedure('crear_repuesto', proveedor_id, nombre, descripcion, precio_unitario, stock_actual)

def obtener_repuesto_por_id(repuesto_id):
    """Llama al SP obtener_repuesto_por_id (Consulta)."""
    print("\n--- INVOCACIÓN: OBTENER REPUESTO ---")
    return execute_stored_procedure('obtener_repuesto_por_id', repuesto_id)

def modificar_repuesto(repuesto_id, proveedor_id, nombre, descripcion, precio_unitario, stock_actual):
    """Llama al SP modificar_repuesto (Actualización)."""
    print("\n--- INVOCACIÓN: UPDATE REPUESTO ---")
    return execute_stored_procedure('modificar_repuesto', repuesto_id, proveedor_id, nombre, descripcion, precio_unitario, stock_actual)

def eliminar_repuesto(repuesto_id):
    """Llama al SP eliminar_repuesto (Borrado)."""
    print("\n--- INVOCACIÓN: DELETE REPUESTO ---")
    return execute_stored_procedure('eliminar_repuesto', repuesto_id)

# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'proveedor'
# ----------------------------------------------------------------------

def crear_proveedor(nombre, telefono, email, direccion):
    """Llama al SP crear_proveedor (Inserción)."""
    print("\n--- INVOCACIÓN: INSERT PROVEEDOR ---")
    return execute_stored_procedure('crear_proveedor', nombre, telefono, email, direccion)

def obtener_proveedor_por_id(proveedor_id):
    """Llama al SP obtener_proveedor_por_id (Consulta)."""
    print("\n--- INVOCACIÓN: OBTENER PROVEEDOR ---")
    return execute_stored_procedure('obtener_proveedor_por_id', proveedor_id)

def modificar_proveedor(proveedor_id, nombre, telefono, email, direccion):
    """Llama al SP modificar_proveedor (Actualización)."""
    print("\n--- INVOCACIÓN: UPDATE PROVEEDOR ---")
    return execute_stored_procedure('modificar_proveedor', proveedor_id, nombre, telefono, email, direccion)

def eliminar_proveedor(proveedor_id):
    """Llama al SP eliminar_proveedor (Borrado)."""
    print("\n--- INVOCACIÓN: DELETE PROVEEDOR ---")
    return execute_stored_procedure('eliminar_proveedor', proveedor_id)

# ----------------------------------------------------------------------
# FUNCIONES DE CONVENIENCIA para los procedimientos de la tabla 'proveedor'
# ----------------------------------------------------------------------

def crear_factura(orden_trabajo_id, subtotal, iva, total):
    """Llama al SP crear_factura (Inserción)."""
    print("\n--- INVOCACIÓN: INSERT FACTURA ---")
    return execute_stored_procedure('crear_factura', orden_trabajo_id, subtotal, iva, total)

def obtener_factura_por_id(factura_id):
    """Llama al SP obtener_factura_por_id (Consulta)."""
    print("\n--- INVOCACIÓN: OBTENER FACTURA ---")
    return execute_stored_procedure('obtener_factura_por_id', factura_id)

def modificar_factura(factura_id, subtotal, iva, total):
    """Llama al SP modificar_factura (Actualización)."""
    print("\n--- INVOCACIÓN: UPDATE FACTURA ---")
    return execute_stored_procedure('modificar_factura', factura_id, subtotal, iva, total)

def eliminar_factura(factura_id):
    """Llama al SP eliminar_factura (Borrado)."""
    print("\n--- INVOCACIÓN: DELETE FACTURA ---")
    return execute_stored_procedure('eliminar_factura', factura_id)


# PARCE FALTA CREAR LOS DEMÁS MÉTODOS PARA FACTURA (ELIMINAR, ACTUALIZAR, OBTENER FACTURAS, OBTENER INFO DE UNA FACTURA)  - ok, teateados
# FALTAN TODOS LOS PRODECIMIENTOS PARA LA TABLA VEHICULO (CREAR, MODIFICAR, ELIMINAR, OBTENER) - ok, teateados
# FALTAN TODOS LOS PRODECIMIENTOS PARA LA TABLA SERVICIO (CREAR, MODIFICAR, ELIMINAR, OBTENER) - ok, testeados
# FALTAN TODOS LOS PRODECIMIENTOS PARA LA TABLA REPUESTO (CREAR, MODIFICAR, ELIMINAR, OBTENER) - ok, testeados
# FALTAN TODOS LOS PRODECIMIENTOS PARA LA TABLA PROVEEDOR (CREAR, MODIFICAR, ELIMINAR, OBTENER) - ok, testedos
# cliente - ok, teateados
# NO PUDE PROBAR PORQUE ME SALE UN ERROR EN LA CLASE ESTA CLASE, EN LA IMPORTACIÓN DE LA CLASE DE pyodbc
