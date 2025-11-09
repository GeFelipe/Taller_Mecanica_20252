import pyodbc
import sys
import os
import flask
import json
from db_connector import (
    crear_vehiculo,
    modificar_vehiculo,
    obtener_vehiculo_por_id,
    eliminar_vehiculo
)

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = flask.Flask(__name__)

@app.route('/vehiculo/crear', methods=["POST"])
def crear():
    try:
        data = flask.request.get_json()
        cliente_id = data["cliente_id"]
        placa = data["placa"]
        marca = data["marca"]
        modelo = data["modelo"]
        anio = data["anio"]
        vin = data["vin"]
        color = data["color"]
        respuesta = crear_vehiculo(cliente_id, placa, marca, modelo, anio, vin, color)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/vehiculo/obtener/<int:vehiculo_id>', methods=["GET"])
def obtener(vehiculo_id):
    try:
        respuesta = obtener_vehiculo_por_id(vehiculo_id)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/vehiculo/modificar', methods=["PUT"])
def modificar():
    try:
        data = flask.request.get_json()
        vehiculo_id = data["vehiculo_id"]
        cliente_id = data["cliente_id"]
        placa = data["placa"]
        marca = data["marca"]
        modelo = data["modelo"]
        anio = data["anio"]
        vin = data["vin"]
        color = data["color"]
        respuesta = modificar_vehiculo(vehiculo_id, cliente_id, placa, marca, modelo, anio, vin, color)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/vehiculo/eliminar/<int:vehiculo_id>', methods=["DELETE"])
def eliminar(vehiculo_id):
    try:
        respuesta = eliminar_vehiculo(vehiculo_id)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

app.run(host="localhost", port=4040, debug=True)
