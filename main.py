from db_connector import select_cliente, insert_cliente, update_contacto
from db_connector import crear_vehiculo, modificar_vehiculo, obtener_vehiculo_por_id, eliminar_vehiculo
from db_connector import execute_stored_procedure, crear_proveedor, obtener_proveedor_por_id, modificar_proveedor, eliminar_proveedor
from db_connector import execute_stored_procedure, crear_factura, obtener_factura_por_id, modificar_factura, eliminar_factura
from db_connector import execute_stored_procedure, obtener_citas_cliente, agregar_nueva_cita, actualizar_estado_cita, eliminar_cita 


#from db_connector import execute_stored_procedure # Usamos la función base
# Nota: La función mostrar_resultado_consulta debe estar definida aquí o importada.
# Asumo que usarás una versión simplificada de la función base del db_connector para esta demostración.

def mostrar_resultado_consulta(columns, results):
    """Formatea y muestra los resultados de una consulta."""
    if columns and results:
        print("\n--- RESULTADOS DE LA CONSULTA ---")
        print("Columnas:", columns)
        for row in results:
            print(f"-> {row}")
        print("---------------------------------")
    elif columns is None and results is None:
        pass # La operación de modificación fue exitosa y ya fue reportada por db_connector.py
    else:
        print("INFO: La consulta no devolvió resultados.")

# def main():
#     print("\n--- INICIO DEL PROGRAMA DE ACCESO A DATOS ---")

#     # 1. --- EJEMPLO 1: Inserción (INSERT) ---
#     # Se recomienda insertar un nuevo cliente primero para asegurar que hay datos para probar las otras operaciones.
#     print("\n[ TAREA 1: Ejecutar Inserción de Nuevo Cliente ]")
    
#     nuevo_nombre = "Juan"
#     nuevo_apellido = "Pérez"
#     nuevo_telefono = "555-1234"
#     nuevo_email = "juan.perez@test.com"
#     nueva_direccion = "Calle Falsa 123"
    
#     # Llama al SP: agregar_nuevo_cliente
#     insert_cliente(nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_email, nueva_direccion)

#     # 2. --- EJEMPLO 2: Consulta (SELECT) ---
#     # Asume que el cliente a buscar es el primero insertado o que ya existe (ej. ID=1).
#     # ¡Asegúrate de que este ID exista en tu tabla!
#     print("\n[ TAREA 2: Ejecutar Consulta de Cliente Existente ]")
    
#     id_cliente_a_buscar = 1 
    
#     # Llama al SP: obtener_datos_cliente
#     columns, results = select_cliente(id_cliente_a_buscar)
#     mostrar_resultado_consulta(columns, results)
    
#     # 3. --- EJEMPLO 3: Actualización (UPDATE) ---
#     print("\n[ TAREA 3: Ejecutar Actualización de Contacto ]")
    
#     id_a_actualizar = 1 
#     telefono_nuevo = "555-9999"
#     direccion_nueva = "Avenida Siempre Viva 742"
    
#     # Llama al SP: actualizar_contacto_cliente
#     update_contacto(id_a_actualizar, telefono_nuevo, direccion_nueva)
    
#     # Opcional: Volver a consultar para verificar la actualización
#     print("\n[ TAREA 3.1: Verificar Actualización ]")
#     columns, results = select_cliente(id_a_actualizar)
#     mostrar_resultado_consulta(columns, results)

#     print("\n--- FIN DEL PROGRAMA ---")

""" def main():
    print("\n--- INICIO: PRUEBAS DE OPERACIONES CRUD DE VEHICULO ---")

    # Definimos el ID del cliente al que se asignará el vehículo (Debe existir)
    CLIENTE_ID_EXISTENTE = 1
    
    # El ID del vehículo que vamos a insertar y luego usar en las pruebas
    # Lo usaremos como 1 o el que sepamos que se va a insertar.
    VEHICULO_ID_PRUEBA = 11

    # 1. --- TAREA 1: Creación (INSERT) ---
    print("\n[ TAREA 1: Ejecutar Creación de Nuevo Vehículo ]")
    
    # Parámetros para el SP: crear_vehiculo
    cliente_id = CLIENTE_ID_EXISTENTE
    placa = "ABC123" 
    marca = "Toyota"
    modelo = "Corolla"
    anio = 2020
    vin = "ABCDEFGHIJ012345"
    color = "Rojo"
    
    # Llama al SP: crear_vehiculo (Usando la función genérica)
    execute_stored_procedure(
        'crear_vehiculo', 
        cliente_id, placa, marca, modelo, anio, vin, color
    )

    # 2. --- TAREA 2: Consulta (SELECT) ---
    print("\n[ TAREA 2: Ejecutar Consulta de Vehículo ]")
    
    # Llama al SP: obtener_vehiculo_por_id
    columns, results = execute_stored_procedure(
        'obtener_vehiculo_por_id', 
        VEHICULO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)
    
        # 3. --- TAREA 3: Modificación (UPDATE) ---
    print("\n[ TAREA 3: Ejecutar Modificación de Vehículo ]")
    
    # Parámetros modificados
    placa_mod = "XYZ123" # No la cambiamos (es UNIQUE)
    marca_mod = "Toyota"
    modelo_mod = "Corolla SE" # Nuevo modelo
    color_mod = "Negro" # Nuevo color
    
    # Llama al SP: modificar_vehiculo
    execute_stored_procedure(
        'modificar_vehiculo', 
        VEHICULO_ID_PRUEBA, 
        CLIENTE_ID_EXISTENTE, 
        placa_mod, 
        marca_mod, 
        modelo_mod, 
        2020, # Año sin modificar
        "ABCDEFGHIJ012345", # VIN sin modificar
        color_mod
    )
    
    # Opcional: Volver a consultar para verificar la Modificación
    print("\n[ TAREA 3.1: Verificar Modificación ]")
    columns, results = execute_stored_procedure(
        'obtener_vehiculo_por_id', 
        VEHICULO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)

    # 4. --- TAREA 4: Eliminación (DELETE) ---
    print("\n[ TAREA 4: Ejecutar Eliminación de Vehículo ]")
    
    #Llama al SP: eliminar_vehiculo
    execute_stored_procedure(
        'eliminar_vehiculo', 
        VEHICULO_ID_PRUEBA
    )
    
    # Opcional: Volver a consultar para verificar la Eliminación
    print("\n[ TAREA 4.1: Verificar Eliminación (Debería dar 'No se encontraron datos') ]")
    columns, results = execute_stored_procedure(
        'obtener_vehiculo_por_id', 
        VEHICULO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)

    print("\n--- FIN DEL PROGRAMA ---") """

""" def main():
    print("\n--- INICIO: PRUEBAS CRUD PARA LA TABLA 'Servicio' ---")
    
    # 1. --- TAREA 1: Creación (INSERT) ---
    print("\n[ TAREA 1: Ejecutar Creación de Nuevo Servicio ]")
    
    # Parámetros para el SP: crear_servicio
    nombre = "Cambio de Aceite Premium"
    descripcion = "Incluye filtro de aire y aceite sintético de alta calidad."
    precio_base = 75.50
    
    # Llamada al SP: crear_servicio
    execute_stored_procedure('crear_servicio', nombre, descripcion, precio_base)
    
    # Asumimos que el primer servicio insertado tendrá el ID 1. 
    # AJUSTA ESTE VALOR si ya tenías servicios.
    SERVICIO_ID_PRUEBA = 1 

    # 2. --- TAREA 2: Consulta (SELECT) ---
    print("\n[ TAREA 2: Ejecutar Consulta de Servicio Existente ]")
    
    # Llamada al SP: obtener_servicio_por_id
    columns, results = execute_stored_procedure(
        'obtener_servicio_por_id', 
        SERVICIO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)
    
    # 3. --- TAREA 3: Modificación (UPDATE) ---
    print("\n[ TAREA 3: Ejecutar Modificación de Servicio ]")
    
    # Parámetros modificados (Aumento de precio y descripción)
    nombre_mod = "Cambio de Aceite Premium"
    descripcion_mod = "¡OFERTA! Incluye filtro de aire y aceite sintético de alta calidad."
    precio_base_mod = 85.00 # Aumento de precio
    
    # Llamada al SP: modificar_servicio
    execute_stored_procedure(
        'modificar_servicio', 
        SERVICIO_ID_PRUEBA, 
        nombre_mod, 
        descripcion_mod, 
        precio_base_mod
    )
    
    # Opcional: Volver a consultar para verificar la Modificación
    print("\n[ TAREA 3.1: Verificar Modificación ]")
    columns, results = execute_stored_procedure(
        'obtener_servicio_por_id', 
        SERVICIO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)

    # 4. --- TAREA 4: Eliminación (DELETE) ---
    print("\n[ TAREA 4: Ejecutar Eliminación de Servicio ]")
    
    # Llamada al SP: eliminar_servicio
    execute_stored_procedure(
        'eliminar_servicio', 
        SERVICIO_ID_PRUEBA
    )
    
    # Opcional: Volver a consultar para verificar la Eliminación
    print("\n[ TAREA 4.1: Verificar Eliminación (Debería dar 'no devolvió resultados') ]")
    columns, results = execute_stored_procedure(
        'obtener_servicio_por_id', 
        SERVICIO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)

    print("\n--- FIN DEL PROGRAMA ---") """



""" def main():
    print("\n--- INICIO: PRUEBAS CRUD PARA LA TABLA 'Repuesto' ---")
    
    # Define el ID de un proveedor existente
    PROVEEDOR_ID_EXISTENTE = 1 
    # Define el ID del repuesto que se usará para la prueba (asumiendo que será el ID 1)
    REPUESTO_ID_PRUEBA = 1

    # 1. --- TAREA 1: Creación (INSERT) ---
    print("\n[ TAREA 1: Ejecutar Creación de Nuevo Repuesto ]")
    
    # Parámetros para el SP: crear_repuesto
    proveedor_id = PROVEEDOR_ID_EXISTENTE
    nombre = "Filtro de Aceite"
    descripcion = "Filtro de alta eficiencia para motores de 2.0L."
    precio_unitario = 15.99
    stock_inicial = 50
    
    # Llamada al SP: crear_repuesto
    execute_stored_procedure(
        'crear_repuesto', 
        proveedor_id, nombre, descripcion, precio_unitario, stock_inicial
    )

    # 2. --- TAREA 2: Consulta (SELECT) ---
    print("\n[ TAREA 2: Ejecutar Consulta de Repuesto Existente ]")
    
    # Llamada al SP: obtener_repuesto_por_id
    columns, results = execute_stored_procedure(
        'obtener_repuesto_por_id', 
        REPUESTO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)
    
    # 3. --- TAREA 3: Modificación (UPDATE) ---
    print("\n[ TAREA 3: Ejecutar Modificación de Repuesto ]")
    
    # Parámetros modificados (Aumento de precio y ajuste de stock)
    precio_nuevo = 17.50
    stock_ajustado = 45 # Se vendieron 5 unidades
    
    # Llamada al SP: modificar_repuesto
    execute_stored_procedure(
        'modificar_repuesto', 
        REPUESTO_ID_PRUEBA, 
        PROVEEDOR_ID_EXISTENTE, 
        "Filtro de Aceite", # Nombre sin modificar
        "Filtro de alta eficiencia, versión mejorada.", # Descripción modificada
        precio_nuevo, 
        stock_ajustado
    )
    
    # Opcional: Volver a consultar para verificar la Modificación
    print("\n[ TAREA 3.1: Verificar Modificación ]")
    columns, results = execute_stored_procedure(
        'obtener_repuesto_por_id', 
        REPUESTO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)

    # 4. --- TAREA 4: Eliminación (DELETE) ---
    print("\n[ TAREA 4: Ejecutar Eliminación de Repuesto ]")
    
    # Llamada al SP: eliminar_repuesto
    execute_stored_procedure(
        'eliminar_repuesto', 
        REPUESTO_ID_PRUEBA
    )
    
    # Opcional: Volver a consultar para verificar la Eliminación
    print("\n[ TAREA 4.1: Verificar Eliminación ]")
    columns, results = execute_stored_procedure(
        'obtener_repuesto_por_id', 
        REPUESTO_ID_PRUEBA
    )
    mostrar_resultado_consulta(columns, results)

    print("\n--- FIN DEL PROGRAMA ---") """

""" def main():
    print("\n--- INICIO: PRUEBAS CRUD PARA LA TABLA 'Proveedor' ---")
    
    # Define el ID del proveedor que se usará para la prueba (asumiendo que será el ID 1)
    PROVEEDOR_ID_PRUEBA = 1

    # 1. --- TAREA 1: Creación (INSERT) ---
    print("\n[ TAREA 1: Ejecutar Creación de Nuevo Proveedor ]")
    
    # Parámetros para el SP: crear_proveedor
    nombre = "AutoRepuestos Global"
    telefono = "800-REPUESTOS"
    email = "contacto@global.com"
    direccion = "Calle de los Talleres 456"
    
    # Llamada al SP: crear_proveedor
    crear_proveedor(nombre, telefono, email, direccion)

    # 2. --- TAREA 2: Consulta (SELECT) ---
    print("\n[ TAREA 2: Ejecutar Consulta de Proveedor Existente ]")
    
    # Llamada al SP: obtener_proveedor_por_id
    columns, results = obtener_proveedor_por_id(PROVEEDOR_ID_PRUEBA)
    mostrar_resultado_consulta(columns, results)
    
    # 3. --- TAREA 3: Modificación (UPDATE) ---
    print("\n[ TAREA 3: Ejecutar Modificación de Proveedor ]")
    
    # Parámetros modificados
    nombre_mod = "AutoRepuestos Global S.A."
    telefono_mod = "555-9876" # Nuevo teléfono
    email_mod = "ventas@global.com" # Nuevo email
    direccion_mod = "Calle de los Talleres 456"
    
    # Llamada al SP: modificar_proveedor
    modificar_proveedor(PROVEEDOR_ID_PRUEBA, nombre_mod, telefono_mod, email_mod, direccion_mod)
    
    # Opcional: Volver a consultar para verificar la Modificación
    print("\n[ TAREA 3.1: Verificar Modificación ]")
    columns, results = obtener_proveedor_por_id(PROVEEDOR_ID_PRUEBA)
    mostrar_resultado_consulta(columns, results)

    # 4. --- TAREA 4: Eliminación (DELETE) ---
    print("\n[ TAREA 4: Ejecutar Eliminación de Proveedor ]")
    
    # Llamada al SP: eliminar_proveedor
    eliminar_proveedor(PROVEEDOR_ID_PRUEBA)
    
    # Opcional: Volver a consultar para verificar la Eliminación
    print("\n[ TAREA 4.1: Verificar Eliminación ]")
    columns, results = obtener_proveedor_por_id(PROVEEDOR_ID_PRUEBA)
    mostrar_resultado_consulta(columns, results)

    print("\n--- FIN DEL PROGRAMA ---") """

""" def main():
    print("\n--- INICIO: PRUEBAS CRUD PARA LA TABLA 'Factura' ---")
    
    # Define el ID de una Orden de Trabajo existente
    ORDEN_TRABAJO_ID_EXISTENTE = 1 
    # Define el ID de la factura que se usará para la prueba (asumiendo que será el ID 1)
    FACTURA_ID_PRUEBA = 1

    # 1. --- TAREA 1: Creación (INSERT) ---
    print("\n[ TAREA 1: Ejecutar Creación de Nueva Factura ]")
    
    # Parámetros iniciales
    orden_id = ORDEN_TRABAJO_ID_EXISTENTE
    subtotal = 150.00
    iva = 30.00
    total = 180.00
    
    # Llamada al SP: crear_factura
    crear_factura(orden_id, subtotal, iva, total)

    # 2. --- TAREA 2: Consulta (SELECT) ---
    print("\n[ TAREA 2: Ejecutar Consulta de Factura Existente ]")
    
    # Llamada al SP: obtener_factura_por_id
    columns, results = obtener_factura_por_id(FACTURA_ID_PRUEBA)
    mostrar_resultado_consulta(columns, results)
    
    # 3. --- TAREA 3: Modificación (UPDATE) ---
    print("\n[ TAREA 3: Ejecutar Modificación de Factura ]")
    
    # Parámetros modificados (Ajuste del subtotal/total)
    subtotal_mod = 165.00
    iva_mod = 33.00
    total_mod = 198.00
    
    # Llamada al SP: modificar_factura
    modificar_factura(FACTURA_ID_PRUEBA, subtotal_mod, iva_mod, total_mod)
    
    # Opcional: Volver a consultar para verificar la Modificación
    print("\n[ TAREA 3.1: Verificar Modificación ]")
    columns, results = obtener_factura_por_id(FACTURA_ID_PRUEBA)
    mostrar_resultado_consulta(columns, results)

    # 4. --- TAREA 4: Eliminación (DELETE) ---
    print("\n[ TAREA 4: Ejecutar Eliminación de Factura ]")
    
    # Llamada al SP: eliminar_factura
    eliminar_factura(FACTURA_ID_PRUEBA)
    
    # Opcional: Volver a consultar para verificar la Eliminación
    print("\n[ TAREA 4.1: Verificar Eliminación ]")
    columns, results = obtener_factura_por_id(FACTURA_ID_PRUEBA)
    mostrar_resultado_consulta(columns, results)

    print("\n--- FIN DEL PROGRAMA ---") """

def main():
    print("\n--- INICIO: PRUEBAS CRUD PARA LA TABLA 'Cita' ---")
    
    # IDs EXISTENTES PARA PRUEBA
    CLIENTE_ID_EXISTENTE = 1 
    VEHICULO_ID_EXISTENTE = 5
    EMPLEADO_ID_EXISTENTE = 1 # Asumimos la existencia de un empleado
    CITA_ID_PRUEBA = 1 # ID de la cita existente para las pruebas

    # 1. --- TAREA 1: Creación (INSERT) ---
    print("\n[ TAREA 1: Ejecutar Creación de Nueva Cita ]")
    
    # Parámetros para el SP: agregar_nueva_cita
    cliente_id = CLIENTE_ID_EXISTENTE
    vehiculo_id = VEHICULO_ID_EXISTENTE
    empleado_id = EMPLEADO_ID_EXISTENTE
    # Nota: Usamos un formato de fecha compatible con MySQL (YYYY-MM-DD HH:MM:SS)
    fecha_cita = "2025-10-15 14:30:00" 
    descripcion = "Revisión de frenos delanteros."
    
    # Llamada al SP: agregar_nueva_cita
    agregar_nueva_cita(cliente_id, vehiculo_id, empleado_id, fecha_cita, descripcion)

    # 2. --- TAREA 2: Consulta por Cliente (SELECT) ---
    print("\n[ TAREA 2: Ejecutar Consulta de Citas por Cliente ]")
    
    # Llamada al SP: obtener_citas_cliente
    columns, results = obtener_citas_cliente(CLIENTE_ID_EXISTENTE)
    mostrar_resultado_consulta(columns, results)
    
    # 3. --- TAREA 3: Actualización (UPDATE) ---
    # Usaremos el ID de la cita que ya existe (CITA_ID_PRUEBA = 1)
    print("\n[ TAREA 3: Ejecutar Actualización de Estado de Cita ]")
    
    cita_id_a_actualizar = CITA_ID_PRUEBA
    nuevo_estado = "Confirmada" # Nuevo estado
    
    # Llamada al SP: actualizar_estado_cita
    actualizar_estado_cita(cita_id_a_actualizar, nuevo_estado)
    
    # Opcional: Volver a consultar para verificar la Actualización (usando el SP de Cliente)
    print("\n[ TAREA 3.1: Verificar Actualización de Estado ]")
    columns, results = obtener_citas_cliente(CLIENTE_ID_EXISTENTE)
    mostrar_resultado_consulta(columns, results)


    # 4. --- TAREA 4: Eliminación (DELETE) ---
    print("\n[ TAREA 4: Ejecutar Eliminación de Cita ]")
    
    # Llamada al SP: eliminar_cita
    eliminar_cita(CITA_ID_PRUEBA)
    
    # Opcional: Volver a consultar para verificar la Eliminación
    print("\n[ TAREA 4.1: Verificar Eliminación ]")
    columns, results = obtener_citas_cliente(CLIENTE_ID_EXISTENTE)
    mostrar_resultado_consulta(columns, results)

    print("\n--- FIN DEL PROGRAMA ---")

if __name__ == "__main__":
    main()