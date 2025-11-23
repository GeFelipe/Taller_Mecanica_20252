# Archivo: servicios_generador_token.py
import sys
import os

# Agregar la carpeta raíz al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from Seguridad.jwt_manager import JWTManager



app = Flask(__name__)
jwt_manager = JWTManager()

@app.route('/token/generar', methods=['POST'])
def generar_token():
    """
    Genera un token JWT con los campos que el usuario envíe.
    Cifra automáticamente los campos definidos en AES_FIELDS.
    Es útil para probar cualquier endpoint del sistema.
    """
    try:
        payload = request.json

        if not payload:
            return jsonify({"error": "Debes enviar un JSON con los datos del token"}), 400
        
        token = jwt_manager.create_token(payload)

        return jsonify({
            "mensaje": "Token generado correctamente",
            "token": token,
            "payload_recibido": payload
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# EJECUCIÓN LOCAL
if __name__ == '__main__':
    app.run(debug=True, port=4040)
