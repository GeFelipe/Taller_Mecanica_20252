# Archivo: servicios_Historial.py

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

# ===============================
#     ENDPOINTS HISTORIAL
# ===============================

# --- Obtener historial completo por ID de vehículo ---
@app.route('/historial/<int:vehiculo_id>', methods=['GET'])
def obtener_historial_por_vehiculo(vehiculo_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_historial_vehiculo_por_id (?)", vehiculo_id)

        historial = []
        for row in cursor.fetchall():
            historial.append({
                'VehiculoID': row[0],
                'Placa': row[1],
                'Marca': row[2],
                'Modelo': row[3],
                'Anio': row[4],
                'Color': row[5],
                'ClienteID': row[6],
                'NombreCliente': row[7],
                'TelefonoCliente': row[8],
                'EmailCliente': row[9],
                'DireccionCliente': row[10],
                'OrdenTrabajoID': row[11],
                'FechaInicio': str(row[12]) if row[12] else None,
                'FechaFin': str(row[13]) if row[13] else None,
                'EstadoOrden': row[14],
                'EmpleadoID': row[15],
                'EmpleadoAsignado': row[16],
                'HistorialID': row[17],
                'Observaciones': row[18],
                'FechaHistorial': str(row[19]) if row[19] else None,
                'CitaID': row[20],
                'FechaCita': str(row[21]) if row[21] else None,
                'MotivoCita': row[22],
                'EstadoCita': row[23]
            })

        return jsonify(historial)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# --- Obtener todos los historiales ---
@app.route('/historiales', methods=['GET'])
def obtener_todos_historiales():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("CALL obtener_historiales_todos_vehiculos()")

        historiales = []
        for row in cursor.fetchall():
            historiales.append({
                'VehiculoID': row[0],
                'Placa': row[1],
                'Marca': row[2],
                'Modelo': row[3],
                'Anio': row[4],
                'Color': row[5],
                'ClienteID': row[6],
                'NombreCliente': row[7],
                'OrdenTrabajoID': row[8],
                'FechaInicio': str(row[9]) if row[9] else None,
                'FechaFin': str(row[10]) if row[10] else None,
                'EstadoOrden': row[11],
                'EmpleadoID': row[12],
                'EmpleadoAsignado': row[13],
                'Observaciones': row[14],
                'FechaRegistro': str(row[15]) if row[15] else None,
                'FechaCita': str(row[16]) if row[16] else None,
                'MotivoCita': row[17]
            })

        return jsonify(historiales)

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
