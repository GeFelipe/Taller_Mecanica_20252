from flask import Flask, request, jsonify
import sys, os

# --- 🔧 Ajuste para importar desde el directorio raíz ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_connector import (
    crear_factura,
    obtener_factura_por_id,
    modificar_factura,
    eliminar_factura
)

app = Flask(__name__)

# ---------------------------------------------------------
# ENDPOINT: Crear Factura
# ---------------------------------------------------------
@app.route('/factura', methods=['POST'])
def crear_factura_endpoint():
    data = request.get_json()
    orden_trabajo_id = data.get('OrdenTrabajoID')
    subtotal = data.get('Subtotal')
    iva = data.get('IVA')
    total = data.get('Total')

    columnas, resultado = crear_factura(orden_trabajo_id, subtotal, iva, total)
    return jsonify({'mensaje': 'Factura creada correctamente.'}), 201


# ---------------------------------------------------------
# ENDPOINT: Consultar Factura por ID
# ---------------------------------------------------------
@app.route('/factura/<int:factura_id>', methods=['GET'])
def obtener_factura_endpoint(factura_id):
    columnas, resultados = obtener_factura_por_id(factura_id)
    
    if resultados:
        data = [dict(zip(columnas, fila)) for fila in resultados]
        return jsonify(data)
    else:
        return jsonify({'mensaje': ' Factura no encontrada.'}), 404


# ---------------------------------------------------------
#  ENDPOINT: Modificar Factura
# ---------------------------------------------------------
@app.route('/factura/<int:factura_id>', methods=['PUT'])
def modificar_factura_endpoint(factura_id):
    data = request.get_json()
    subtotal = data.get('Subtotal')
    iva = data.get('IVA')
    total = data.get('Total')

    columnas, resultado = modificar_factura(factura_id, subtotal, iva, total)
    return jsonify({'mensaje': ' Factura actualizada correctamente.'})


# ---------------------------------------------------------
# ENDPOINT: Eliminar Factura
# ---------------------------------------------------------
@app.route('/factura/<int:factura_id>', methods=['DELETE'])
def eliminar_factura_endpoint(factura_id):
    columnas, resultado = eliminar_factura(factura_id)
    return jsonify({'mensaje': '🗑️ Factura eliminada correctamente.'})


# ---------------------------------------------------------
# EJECUTAR SERVIDOR
# ---------------------------------------------------------
if __name__ == '__main__':
    app.run(host='localhost', port=4040, debug=True)
