# Archivo: servicios_empleado.py

from flask import Flask, request, jsonify
import pyodbc
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Seguridad.auth import token_required

# --- Ajustar path para acceder a config.py ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import CONNECTION_STRING

app = Flask(__name__)

# --- Crear conexión ---
def get_connection():
    return pyodbc.connect(CONNECTION_STRING)

# ===============================
#       ENDPOINTS EMPLEADO
# ===============================

# --- Crear empleado ---
@app.route('/empleado', methods=['POST'])
@token_required
def crear_empleado():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL crear_empleado (?, ?, ?, ?, ?, ?)",
            (
                data['nombre'],
                data['apellido'],
                data.get('cargo'),
                data.get('telefono'),
                data.get('email'),
                data.get('fecha_contratacion')
            )
        )
        conn.commit()
        return jsonify({'mensaje': 'Empleado creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Obtener todos los empleados ---
@app.route('/empleados', methods=['GET'])
@token_required
def obtener_empleados():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_todos_empleados()")
        empleados = []
        for row in cursor.fetchall():
            empleados.append({
                'EmpleadoID': row[0],
                'Nombre': row[1],
                'Apellido': row[2],
                'Cargo': row[3],
                'Telefono': row[4],
                'Email': row[5],
                'FechaContratacion': str(row[6]) if row[6] else None
            })
        return jsonify(empleados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Obtener empleado por ID ---
@app.route('/empleado/<int:empleado_id>', methods=['GET'])
@token_required
def obtener_empleado(empleado_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_empleado_por_id (?)", empleado_id)
        row = cursor.fetchone()
        if row:
            empleado = {
                'EmpleadoID': row[0],
                'Nombre': row[1],
                'Apellido': row[2],
                'Cargo': row[3],
                'Telefono': row[4],
                'Email': row[5],
                'FechaContratacion': str(row[6]) if row[6] else None
            }
            return jsonify(empleado)
        else:
            return jsonify({'mensaje': 'Empleado no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Modificar empleado ---
@app.route('/empleado/<int:empleado_id>', methods=['PUT'])
@token_required
def modificar_empleado(empleado_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL modificar_empleado (?, ?, ?, ?, ?, ?, ?)",
            (
                empleado_id,
                data['nombre'],
                data['apellido'],
                data.get('cargo'),
                data.get('telefono'),
                data.get('email'),
                data.get('fecha_contratacion')
            )
        )
        conn.commit()
        return jsonify({'mensaje': 'Empleado modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Eliminar empleado ---
@app.route('/empleado/<int:empleado_id>', methods=['DELETE'])
@token_required
def eliminar_empleado(empleado_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL eliminar_empleado (?)", empleado_id)
        conn.commit()
        return jsonify({'mensaje': 'Empleado eliminado exitosamente'})
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
