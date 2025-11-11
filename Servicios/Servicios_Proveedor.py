from flask import Flask, request, jsonify
import pyodbc
import sys
import os

# --- Ajustar path para acceder a config.py ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import CONNECTION_STRING

app = Flask(__name__)

# --- Crear conexión ---
def get_connection():
    return pyodbc.connect(CONNECTION_STRING)

# --- Crear proveedor ---
@app.route('/proveedor', methods=['POST'])
def crear_proveedor():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL crear_proveedor (?, ?, ?, ?)",
            (data['nombre'], data['telefono'], data['email'], data['direccion'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Proveedor creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Obtener proveedor por ID ---
@app.route('/proveedor/<int:proveedor_id>', methods=['GET'])
def obtener_proveedor(proveedor_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_proveedor_por_id (?)", proveedor_id)
        row = cursor.fetchone()
        if row:
            proveedor = {
                'ProveedorID': row[0],
                'Nombre': row[1],
                'Telefono': row[2],
                'Email': row[3],
                'Direccion': row[4]
            }
            return jsonify(proveedor)
        else:
            return jsonify({'mensaje': 'Proveedor no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Modificar proveedor ---
@app.route('/proveedor/<int:proveedor_id>', methods=['PUT'])
def modificar_proveedor(proveedor_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL modificar_proveedor (?, ?, ?, ?, ?)",
            (proveedor_id, data['nombre'], data['telefono'], data['email'], data['direccion'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Proveedor modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Eliminar proveedor ---
@app.route('/proveedor/<int:proveedor_id>', methods=['DELETE'])
def eliminar_proveedor(proveedor_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL eliminar_proveedor (?)", proveedor_id)
        conn.commit()
        return jsonify({'mensaje': 'Proveedor eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=4040)
