from db_connector import select_cliente, insert_cliente, update_contacto

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

def main():
    print("\n--- INICIO DEL PROGRAMA DE ACCESO A DATOS ---")

    # 1. --- EJEMPLO 1: Inserción (INSERT) ---
    # Se recomienda insertar un nuevo cliente primero para asegurar que hay datos para probar las otras operaciones.
    print("\n[ TAREA 1: Ejecutar Inserción de Nuevo Cliente ]")
    
    nuevo_nombre = "Juan"
    nuevo_apellido = "Pérez"
    nuevo_telefono = "555-1234"
    nuevo_email = "juan.perez@test.com"
    nueva_direccion = "Calle Falsa 123"
    
    # Llama al SP: agregar_nuevo_cliente
    insert_cliente(nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_email, nueva_direccion)

    # 2. --- EJEMPLO 2: Consulta (SELECT) ---
    # Asume que el cliente a buscar es el primero insertado o que ya existe (ej. ID=1).
    # ¡Asegúrate de que este ID exista en tu tabla!
    print("\n[ TAREA 2: Ejecutar Consulta de Cliente Existente ]")
    
    id_cliente_a_buscar = 1 
    
    # Llama al SP: obtener_datos_cliente
    columns, results = select_cliente(id_cliente_a_buscar)
    mostrar_resultado_consulta(columns, results)
    
    # 3. --- EJEMPLO 3: Actualización (UPDATE) ---
    print("\n[ TAREA 3: Ejecutar Actualización de Contacto ]")
    
    id_a_actualizar = 1 
    telefono_nuevo = "555-9999"
    direccion_nueva = "Avenida Siempre Viva 742"
    
    # Llama al SP: actualizar_contacto_cliente
    update_contacto(id_a_actualizar, telefono_nuevo, direccion_nueva)
    
    # Opcional: Volver a consultar para verificar la actualización
    print("\n[ TAREA 3.1: Verificar Actualización ]")
    columns, results = select_cliente(id_a_actualizar)
    mostrar_resultado_consulta(columns, results)

    print("\n--- FIN DEL PROGRAMA ---")


if __name__ == "__main__":
    main()