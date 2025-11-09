# Archivo: servicios_empleado.py

import flask
import json
import pyodbc

import sys
import os
# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connector import (
    crear_empleado,
    obtener_empleado_por_id,
    modificar_empleado,
    eliminar_empleado,
    obtener_todos_empleados
)

app = flask.Flask(__name__)

@app.route('/empleados', methods=["GET"])
def listar_empleados():
    """
    Obtiene todos los empleados.
    Endpoint: GET /empleados
    """
    respuesta = {}
    try:
        columnas, filas = obtener_todos_empleados()
        empleados = []
        if filas:
            for fila in filas:
                empleados.append(dict(zip(columnas, fila)))
        respuesta["Empleados"] = empleados
        respuesta["Respuesta"] = "OK"
        return flask.jsonify(respuesta)
    except Exception as ex:
        respuesta["Error"] = str(ex)
        respuesta["Respuesta"] = "Error"
        return flask.jsonify(respuesta), 500


@app.route('/empleados/<int:empleado_id>', methods=["GET"])
def obtener_empleado(empleado_id):
    """
    Obtiene un empleado por ID.
    Endpoint: GET /empleados/<id>
    """
    respuesta = {}
    try:
        columnas, filas = obtener_empleado_por_id(empleado_id)
        if filas:
            empleado = dict(zip(columnas, filas[0]))
            respuesta["Empleado"] = empleado
            respuesta["Respuesta"] = "OK"
        else:
            respuesta["Mensaje"] = "Empleado no encontrado"
            respuesta["Respuesta"] = "NoData"
        return flask.jsonify(respuesta)
    except Exception as ex:
        respuesta["Error"] = str(ex)
        respuesta["Respuesta"] = "Error"
        return flask.jsonify(respuesta), 500


@app.route('/empleados', methods=["POST"])
def crear_nuevo_empleado():
    """
    Crea un nuevo empleado.
    Endpoint: POST /empleados
    Body JSON:
    {
        "Nombre": "...",
        "Apellido": "...",
        "Cargo": "...",
        "Telefono": "...",
        "Email": "...",
        "FechaContratacion": "YYYY-MM-DD"
    }
    """
    respuesta = {}
    try:
        data = flask.request.get_json()
        crear_empleado(
            data["Nombre"],
            data["Apellido"],
            data.get("Cargo", None),
            data.get("Telefono", None),
            data.get("Email", None),
            data.get("FechaContratacion", None)
        )
        respuesta["Mensaje"] = "Empleado creado correctamente"
        respuesta["Respuesta"] = "OK"
        return flask.jsonify(respuesta), 201
    except Exception as ex:
        respuesta["Error"] = str(ex)
        respuesta["Respuesta"] = "Error"
        return flask.jsonify(respuesta), 500


@app.route('/empleados/<int:empleado_id>', methods=["PUT"])
def actualizar_empleado(empleado_id):
    """
    Actualiza un empleado existente.
    Endpoint: PUT /empleados/<id>
    Body JSON igual que el POST.
    """
    respuesta = {}
    try:
        data = flask.request.get_json()
        modificar_empleado(
            empleado_id,
            data["Nombre"],
            data["Apellido"],
            data.get("Cargo", None),
            data.get("Telefono", None),
            data.get("Email", None),
            data.get("FechaContratacion", None)
        )
        respuesta["Mensaje"] = "Empleado actualizado correctamente"
        respuesta["Respuesta"] = "OK"
        return flask.jsonify(respuesta)
    except Exception as ex:
        respuesta["Error"] = str(ex)
        respuesta["Respuesta"] = "Error"
        return flask.jsonify(respuesta), 500


@app.route('/empleados/<int:empleado_id>', methods=["DELETE"])
def borrar_empleado(empleado_id):
    """
    Elimina un empleado.
    Endpoint: DELETE /empleados/<id>
    """
    respuesta = {}
    try:
        eliminar_empleado(empleado_id)
        respuesta["Mensaje"] = "Empleado eliminado correctamente"
        respuesta["Respuesta"] = "OK"
        return flask.jsonify(respuesta)
    except Exception as ex:
        respuesta["Error"] = str(ex)
        respuesta["Respuesta"] = "Error"
        return flask.jsonify(respuesta), 500

app.run(host="localhost", port=4040, debug=True)

# if __name__ == "__main__":
#     print("🚀 Servidor Flask ejecutándose en http://localhost:4040 ...")
#     app.run(host="localhost", port=4040, debug=True)
