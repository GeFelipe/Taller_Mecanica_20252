#import sys
#import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from Seguridad.auth import token_required
#from flask import Flask, request, jsonify
#import pyodbc

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

# --- Crear conexión a la base de datos ---
def get_connection():
    return pyodbc.connect(CONNECTION_STRING)

# --- Crear una nueva cita ---
@app.route('/cita', methods=['POST'])
@token_required
def crear_cita():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL agregar_nueva_cita (?, ?, ?, ?)",
            (data['cliente_id'], data['vehiculo_id'], data['fecha_cita'], data['descripcion'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Cita creada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Obtener citas por cliente ---
@app.route('/cita/cliente/<int:cliente_id>', methods=['GET'])
@token_required
def obtener_citas_cliente(cliente_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_citas_cliente (?)", cliente_id)
        rows = cursor.fetchall()

        citas = []
        for row in rows:
            citas.append({
                'CitaID': row[0],
                'FechaCita': str(row[1]),
                'Descripcion': row[2],
                'Estado': row[3],
                'Vehiculo': row[4]
            })

        return jsonify(citas), 200 if citas else (jsonify({'mensaje': 'No se encontraron citas'}), 404)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Actualizar estado de una cita ---
@app.route('/cita/<int:cita_id>/estado', methods=['PUT'])
@token_required
def actualizar_estado_cita(cita_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL actualizar_estado_cita (?, ?)", (cita_id, data['estado']))
        conn.commit()
        return jsonify({'mensaje': 'Estado de la cita actualizado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Eliminar cita ---
@app.route('/cita/<int:cita_id>', methods=['DELETE'])
@token_required
def eliminar_cita(cita_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL eliminar_cita (?)", cita_id)
        conn.commit()
        return jsonify({'mensaje': 'Cita eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=4040)
