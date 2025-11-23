# Archivo: servicios_orden_trabajo.py

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

# ===========================
#     CONEXIÓN A BD
# ===========================
def get_connection():
    return pyodbc.connect(CONNECTION_STRING)


# ===========================
#   CREAR ORDEN DE TRABAJO
# ===========================
@app.route('/orden', methods=['POST'])
@token_required
def crear_orden():
    """
    Crea una nueva orden de trabajo y registra historial.
    Procedimiento: crear_orden_trabajo(cita_id, empleado_id, observaciones)
    """
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL crear_orden_trabajo (?, ?, ?)",
            (
                data['cita_id'],
                data['empleado_id'],
                data.get('observaciones')
            )
        )
        conn.commit()

        return jsonify({'mensaje': 'Orden de trabajo creada correctamente'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ===========================
#   OBTENER ORDEN COMPLETA
# ===========================
@app.route('/orden/<int:orden_id>', methods=['GET'])
@token_required
def obtener_orden(orden_id):
    """
    Retorna la orden completa con detalle, repuestos y servicios.
    Procedimiento: obtener_orden_completa(orden_id)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL obtener_orden_completa (?)", orden_id)

        # --- Primer resultset: Información general ---
        orden_row = cursor.fetchone()

        if not orden_row:
            return jsonify({'mensaje': 'Orden no encontrada'}), 404

        orden = {
            'OrdenTrabajoID': orden_row[0],
            'FechaInicio': str(orden_row[1]),
            'FechaFin': str(orden_row[2]) if orden_row[2] else None,
            'Estado': orden_row[3],
            'Cliente': orden_row[4],
            'Vehiculo': orden_row[5],
            'Empleado': orden_row[6]
        }

        # --- Mover al segundo resultset (detalle trabajo) ---
        cursor.nextset()
        detalles = []
        for row in cursor.fetchall():
            detalles.append({
                'DetalleID': row[0],
                'OrdenTrabajoID': row[1],
                'Descripcion': row[2],
                'Costo': float(row[3]) if row[3] else None
            })

        # --- Tercer resultset (repuestos) ---
        cursor.nextset()
        repuestos = []
        for row in cursor.fetchall():
            repuestos.append({
                'Repuesto': row[0],
                'Cantidad': row[1],
                'PrecioUnitario': float(row[2])
            })

        # --- Cuarto resultset (servicios) ---
        cursor.nextset()
        servicios = []
        for row in cursor.fetchall():
            servicios.append({
                'Servicio': row[0],
                'Cantidad': row[1],
                'PrecioUnitario': float(row[2])
            })

        return jsonify({
            'orden': orden,
            'detalle_trabajo': detalles,
            'repuestos': repuestos,
            'servicios': servicios
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ===========================
#   FINALIZAR ORDEN
# ===========================
@app.route('/orden/<int:orden_id>/finalizar', methods=['PUT'])
@token_required
def finalizar_orden(orden_id):
    """
    Marca una orden como finalizada y la registra en historial.
    Procedimiento: finalizar_orden_trabajo(orden_id, observaciones)
    """
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL finalizar_orden_trabajo (?, ?)",
            (
                orden_id,
                data.get('observaciones')
            )
        )
        conn.commit()

        return jsonify({'mensaje': 'Orden finalizada correctamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ===========================
#     EJECUCIÓN LOCAL
# ===========================
if __name__ == '__main__':
    app.run(debug=True, port=4040)
