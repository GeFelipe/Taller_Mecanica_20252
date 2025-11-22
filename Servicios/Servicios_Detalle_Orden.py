# Archivo: servicios_detalle_orden.py

from flask import Flask, request, jsonify
import pyodbc
import sys
import os

# --- Ajuste de ruta para acceder a config.py ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import CONNECTION_STRING

app = Flask(__name__)

# ----------------------------------------------
#   FUNCIÓN PARA CREAR LA CONEXIÓN
# ----------------------------------------------
def get_connection():
    return pyodbc.connect(CONNECTION_STRING)


# ==============================================
#        ENDPOINTS: DETALLES DE UNA ORDEN
# ==============================================


# ---------------------------------------------------
# AGREGAR MANO DE OBRA A UNA ORDEN
# ---------------------------------------------------
@app.route('/orden/<int:orden_id>/mano_obra', methods=['POST'])
def agregar_mano_obra(orden_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL agregar_detalle_trabajo (?, ?, ?, ?)",
            (
                orden_id,
                data['descripcion'],
                data['horas'],
                data['costo']
            )
        )

        conn.commit()
        return jsonify({'mensaje': 'Detalle de mano de obra agregado correctamente'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



# ---------------------------------------------------
# AGREGAR REPUESTO A UNA ORDEN
# ---------------------------------------------------
@app.route('/orden/<int:orden_id>/repuesto', methods=['POST'])
def agregar_repuesto(orden_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL agregar_repuesto_a_orden (?, ?, ?)",
            (
                orden_id,
                data['repuesto_id'],
                data['cantidad']
            )
        )

        conn.commit()
        return jsonify({'mensaje': 'Repuesto agregado correctamente a la orden'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



# ---------------------------------------------------
# AGREGAR SERVICIO A UNA ORDEN
# ---------------------------------------------------
@app.route('/orden/<int:orden_id>/servicio', methods=['POST'])
def agregar_servicio(orden_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL agregar_servicio_a_orden (?, ?, ?)",
            (
                orden_id,
                data['servicio_id'],
                data['cantidad']
            )
        )

        conn.commit()
        return jsonify({'mensaje': 'Servicio agregado correctamente a la orden'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/orden/<int:orden_id>/mano_obra', methods=['GET'])
def listar_mano_obra(orden_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL obtener_mano_obra_por_orden (?)", (orden_id,))
        rows = cursor.fetchall()

        resultados = []
        for r in rows:
            resultados.append({
                "detalle_id": r[0],
                "descripcion": r[1],
                "horas": r[2],
                "costo": r[3]
            })

        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/orden/<int:orden_id>/repuesto', methods=['GET'])
def listar_repuestos(orden_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL obtener_repuestos_por_orden (?)", (orden_id,))
        rows = cursor.fetchall()

        resultados = []
        for r in rows:
            resultados.append({
                "detalle_id": r[0],
                "repuesto_id": r[1],
                "nombre": r[2],
                "cantidad": r[3],
                "costo_unitario": r[4]
            })

        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/orden/<int:orden_id>/servicio', methods=['GET'])
def listar_servicios(orden_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL obtener_servicios_por_orden (?)", (orden_id,))
        rows = cursor.fetchall()

        resultados = []
        for r in rows:
            resultados.append({
                "detalle_id": r[0],
                "servicio_id": r[1],
                "nombre": r[2],
                "cantidad": r[3],
                "precio_unitario": r[4]
            })

        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/orden/detalle/mano_obra/<int:detalle_id>', methods=['PUT'])
def actualizar_mano_obra(detalle_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL actualizar_detalle_trabajo (?, ?, ?, ?)",
            (
                detalle_id,
                data['descripcion'],
                data['horas'],
                data['costo']
            )
        )

        conn.commit()
        return jsonify({'mensaje': 'Mano de obra actualizada correctamente'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/orden/detalle/<int:detalle_id>', methods=['DELETE'])
def eliminar_detalle(detalle_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL eliminar_detalle_orden (?)", (detalle_id,))

        conn.commit()
        return jsonify({'mensaje': 'Detalle eliminado correctamente'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/orden/detalle/repuesto/<int:detalle_id>', methods=['PUT'])
def actualizar_repuesto(detalle_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL actualizar_repuesto_orden (?, ?)",
            (
                detalle_id,
                data['cantidad']
            )
        )

        conn.commit()
        return jsonify({'mensaje': 'Repuesto actualizado correctamente'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/orden/detalle/servicio/<int:detalle_id>', methods=['PUT'])
def actualizar_servicio(detalle_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "CALL actualizar_servicio_orden (?, ?)",
            (
                detalle_id,
                data['cantidad']
            )
        )

        conn.commit()
        return jsonify({'mensaje': 'Servicio actualizado correctamente'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ==============================================
# EJECUCIÓN LOCAL
# ==============================================
if __name__ == '__main__':
    app.run(debug=True, port=4040)
