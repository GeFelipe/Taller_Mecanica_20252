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

# --- Crear servicio ---
@app.route('/servicio', methods=['POST'])
def crear_servicio():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL crear_servicio (?, ?, ?)",
            (data['nombre'], data['descripcion'], data['precio_base'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Servicio creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Obtener servicio por ID ---
@app.route('/servicio/<int:servicio_id>', methods=['GET'])
def obtener_servicio(servicio_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_servicio_por_id (?)", servicio_id)
        row = cursor.fetchone()
        if row:
            servicio = {
                'ServicioID': row[0],
                'Nombre': row[1],
                'Descripcion': row[2],
                'PrecioBase': float(row[3])
            }
            return jsonify(servicio)
        else:
            return jsonify({'mensaje': 'Servicio no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Modificar servicio ---
@app.route('/servicio/<int:servicio_id>', methods=['PUT'])
def modificar_servicio(servicio_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL modificar_servicio (?, ?, ?, ?)",
            (servicio_id, data['nombre'], data['descripcion'], data['precio_base'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Servicio modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Eliminar servicio ---
@app.route('/servicio/<int:servicio_id>', methods=['DELETE'])
def eliminar_servicio(servicio_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL eliminar_servicio (?)", servicio_id)
        conn.commit()
        return jsonify({'mensaje': 'Servicio eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=4040)
