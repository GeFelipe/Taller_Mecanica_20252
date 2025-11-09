from flask import Flask, request, jsonify
import pyodbc
import sys
import os

# --- Ajustar path para acceder a db_connector.py ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import CONNECTION_STRING

app = Flask(__name__)

# --- Crear conexión a la base de datos ---
def get_connection():
    return pyodbc.connect(CONNECTION_STRING)

# --- Crear repuesto ---
@app.route('/repuesto', methods=['POST'])
def crear_repuesto():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL crear_repuesto (?, ?, ?, ?, ?)",
            (data['proveedor_id'], data['nombre'], data['descripcion'], data['precio_unitario'], data['stock_actual'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Repuesto creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Obtener repuesto por ID ---
@app.route('/repuesto/<int:repuesto_id>', methods=['GET'])
def obtener_repuesto(repuesto_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_repuesto_por_id (?)", repuesto_id)
        row = cursor.fetchone()
        if row:
            repuesto = {
                'RepuestoID': row[0],
                'ProveedorID': row[1],
                'Nombre': row[2],
                'Descripcion': row[3],
                'PrecioUnitario': float(row[4]),
                'StockActual': row[5]
            }
            return jsonify(repuesto)
        else:
            return jsonify({'mensaje': 'Repuesto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Modificar repuesto ---
@app.route('/repuesto/<int:repuesto_id>', methods=['PUT'])
def modificar_repuesto(repuesto_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CALL modificar_repuesto (?, ?, ?, ?, ?, ?)",
            (repuesto_id, data['proveedor_id'], data['nombre'], data['descripcion'], data['precio_unitario'], data['stock_actual'])
        )
        conn.commit()
        return jsonify({'mensaje': 'Repuesto modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- Eliminar repuesto ---
@app.route('/repuesto/<int:repuesto_id>', methods=['DELETE'])
def eliminar_repuesto(repuesto_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL eliminar_repuesto (?)", repuesto_id)
        conn.commit()
        return jsonify({'mensaje': 'Repuesto eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=4040)
