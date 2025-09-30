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