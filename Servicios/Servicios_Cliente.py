# Archivo: servicios_cliente.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Seguridad.auth import token_required
from flask import Flask, request, jsonify
import pyodbc


# --- Ajustar path para acceder a config.py ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import CONNECTION_STRING

app = Flask(__name__)

# --- Crear conexión ---
def get_connection():
    return pyodbc.connect(CONNECTION_STRING)

# ===============================
#          ENDPOINTS CLIENTE
# ===============================

# --- Crear cliente ---
@app.route('/cliente', methods=['POST'])
@token_required
def crear_cliente():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL agregar_nuevo_cliente (?, ?, ?, ?, ?)",
            (
                data['nombre'],
                data['apellido'],
                data['telefono'],
                data['email'],
                data['direccion']
            )
        )

        conn.commit()
        return jsonify({'mensaje': 'Cliente creado exitosamente'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# --- Obtener todos los clientes ---
@app.route('/clientes', methods=['GET'])
@token_required
def obtener_clientes():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL obtener_todos_clientes()")

        clientes = []
        for row in cursor.fetchall():
            clientes.append({
                'ClienteID': row[0],
                'Nombre': row[1],
                'Apellido': row[2],
                'Telefono': row[3],
                'Email': row[4],
                'Direccion': row[5],
                'FechaRegistro': str(row[6]) if row[6] else None
            })

        return jsonify(clientes)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# --- Obtener cliente por ID ---
@app.route('/cliente/<int:cliente_id>', methods=['GET'])
@token_required
def obtener_cliente(cliente_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL obtener_datos_cliente (?)", cliente_id)
        row = cursor.fetchone()

        if row:
            cliente = {
                'ClienteID': row[0],
                'Nombre': row[1],
                'Apellido': row[2],
                'Telefono': row[3],
                'Email': row[4],
                'Direccion': row[5],
                'FechaRegistro': str(row[6]) if row[6] else None
            }
            return jsonify(cliente)
        else:
            return jsonify({'mensaje': 'Cliente no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# --- Modificar cliente ---
@app.route('/cliente/<int:cliente_id>', methods=['PUT'])
@token_required
def modificar_cliente(cliente_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL actualizar_contacto_cliente (?, ?, ?)",
            (
                cliente_id,
                data['telefono'],
                data['direccion']
            )
        )

        conn.commit()
        return jsonify({'mensaje': 'Cliente modificado exitosamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# --- Eliminar cliente ---
@app.route('/cliente/<int:cliente_id>', methods=['DELETE'])
@token_required
def eliminar_cliente(cliente_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL eliminar_cliente (?)", cliente_id)
        conn.commit()

        return jsonify({'mensaje': 'Cliente eliminado exitosamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ===============================
#       EJECUCIÓN LOCAL
# ===============================
if __name__ == '__main__':
    app.run(debug=True, port=4040)

