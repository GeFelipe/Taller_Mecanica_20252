# Archivo: Servicios_Pago.py

import pyodbc
import flask
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Seguridad.auth import token_required

# --- Ajustar path para acceder a config.py ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import CONNECTION_STRING

app = flask.Flask(__name__)

# ------------------------
# Crear un nuevo pago
# ------------------------
@app.route('/pago/crear', methods=['POST'])
@token_required
def crear_pago():
    try:
        data = flask.request.get_json()
        factura_id = data["factura_id"]
        monto = data["monto"]
        metodo = data["metodo"]

        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("CALL registrar_pago(?, ?, ?)", (factura_id, monto, metodo))
        conn.commit()
        cursor.close()
        conn.close()

        return flask.jsonify({"respuesta": "OK", "mensaje": "Pago registrado correctamente"}), 201
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 400


# ------------------------
# Obtener pagos por factura
# ------------------------
@app.route('/pago/factura/<int:factura_id>', methods=['GET'])
@token_required
def obtener_pagos_por_factura(factura_id):
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("CALL obtener_pagos_por_factura(?)", (factura_id,))

        pagos = []
        for row in cursor.fetchall():
            pagos.append({
                'PagoID': row[0],
                'FacturaID': row[1],
                'FechaEmision': str(row[2]),
                'Monto': float(row[3]),
                'FechaPago': str(row[4]),
                'MetodoPago': row[5]
            })

        cursor.close()
        conn.close()

        return flask.jsonify({"respuesta": "OK", "data": pagos}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 400


# ------------------------
# Actualizar un pago
# ------------------------
@app.route('/pago/actualizar', methods=['PUT'])
@token_required
def actualizar_pago():
    try:
        data = flask.request.get_json()
        pago_id = data["pago_id"]
        nuevo_monto = data["nuevo_monto"]
        nuevo_metodo = data["nuevo_metodo"]

        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("CALL actualizar_pago(?, ?, ?)", (pago_id, nuevo_monto, nuevo_metodo))
        conn.commit()
        cursor.close()
        conn.close()

        return flask.jsonify({"respuesta": "OK", "mensaje": "Pago actualizado correctamente"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 400


# ------------------------
# Eliminar un pago
# ------------------------
@app.route('/pago/eliminar/<int:pago_id>', methods=['DELETE'])
@token_required
def eliminar_pago(pago_id):
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("CALL eliminar_pago(?)", (pago_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return flask.jsonify({"respuesta": "OK", "mensaje": "Pago eliminado correctamente"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 400


# ------------------------
# Iniciar servidor
# ------------------------
if __name__ == '__main__':
    app.run(host='localhost', port=4040, debug=True)
