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

# --- Crear vehículo ---
@app.route('/vehiculo', methods=['POST'])
@token_required
def crear_vehiculo():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL crear_vehiculo (?, ?, ?, ?, ?, ?, ?)",
            (data['cliente_id'], data['placa'], data['marca'], data['modelo'], data['anio'], data['vin'], data['color'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Vehículo creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Obtener vehículo por ID ---
@app.route('/vehiculo/<int:vehiculo_id>', methods=['GET'])
@token_required
def obtener_vehiculo(vehiculo_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_vehiculo_por_id (?)", vehiculo_id)
        row = cursor.fetchone()
        if row:
            vehiculo = {
                'VehiculoID': row[0],
                'ClienteID': row[1],
                'Placa': row[2],
                'Marca': row[3],
                'Modelo': row[4],
                'Anio': row[5],
                'VIN': row[6],
                'Color': row[7]
            }
            return jsonify(vehiculo)
        else:
            return jsonify({'mensaje': 'Vehículo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Modificar vehículo ---
@app.route('/vehiculo/<int:vehiculo_id>', methods=['PUT'])
@token_required
def modificar_vehiculo(vehiculo_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL modificar_vehiculo (?, ?, ?, ?, ?, ?, ?, ?)",
            (vehiculo_id, data['cliente_id'], data['placa'], data['marca'], data['modelo'], data['anio'], data['vin'], data['color'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Vehículo modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Eliminar vehículo ---
@app.route('/vehiculo/<int:vehiculo_id>', methods=['DELETE'])
@token_required
def eliminar_vehiculo(vehiculo_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL eliminar_vehiculo (?)", vehiculo_id)
        conn.commit()
        return jsonify({'mensaje': 'Vehículo eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=4040)
