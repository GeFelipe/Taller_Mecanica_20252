import pyodbc
import sys
import os
import flask
import json
from db_connector import (
    select_cliente,
    insert_cliente,
    update_contacto,
    eliminar_cliente
)

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = flask.Flask(__name__)

@app.route('/cliente/crear', methods=["POST"])
def crear():
    try:
        data = flask.request.get_json()
        nombre = data["nombre"]
        apellido = data["apellido"]
        telefono = data["telefono"]
        email = data["email"]
        direccion = data["direccion"]
        respuesta = insert_cliente(nombre, apellido, telefono, email, direccion)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/cliente/obtener/<int:cliente_id>', methods=["GET"])
def obtener(cliente_id):
    try:
        respuesta = select_cliente(cliente_id)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/cliente/modificar', methods=["PUT"])
def modificar():
    try:
        data = flask.request.get_json()
        cliente_id = data["cliente_id"]
        telefono = data["telefono"]
        direccion = data["direccion"]
        respuesta = update_contacto(cliente_id, telefono, direccion)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

@app.route('/cliente/eliminar/<int:cliente_id>', methods=["DELETE"])
def eliminar(cliente_id):
    try:
        respuesta = eliminar_cliente(cliente_id)
        return flask.jsonify({"respuesta": "OK", "data": respuesta}), 200
    except Exception as e:
        return flask.jsonify({"respuesta": "Error", "error": str(e)}), 400

app.run(host="localhost", port=4040, debug=True)
