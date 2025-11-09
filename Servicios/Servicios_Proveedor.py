import pyodbc
import sys
import os
import flask
import json
from db_connector import (
    crear_proveedor,
    obtener_proveedor_por_id,
    modificar_proveedor,
    eliminar_proveedor
)

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = flask.Flask(__name__)

@app.route('/proveedor/crear', methods=["POST"])
def crear():
    try:
        data = flask.request.get_json()
        nombre = data["nombre"]
        telefono = data["telefono"]
        email = data["email"]
        direccion = data["direccion"]
        respuesta = crear_proveedor(nombre, telefono, email, direccion)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/proveedor/obtener/<int:proveedor_id>', methods=["GET"])
def obtener(proveedor_id):
    try:
        respuesta = obtener_proveedor_por_id(proveedor_id)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/proveedor/modificar', methods=["PUT"])
def modificar():
    try:
        data = flask.request.get_json()
        proveedor_id = data["proveedor_id"]
        nombre = data["nombre"]
        telefono = data["telefono"]
        email = data["email"]
        direccion = data["direccion"]
        respuesta = modificar_proveedor(proveedor_id, nombre, telefono, email, direccion)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/proveedor/eliminar/<int:proveedor_id>', methods=["DELETE"])
def eliminar(proveedor_id):
    try:
        respuesta = eliminar_proveedor(proveedor_id)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

app.run(host="localhost", port=4040, debug=True)
