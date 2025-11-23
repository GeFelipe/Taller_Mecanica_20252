# Importa wraps para mantener los metadatos de la función decorada
from functools import wraps

# Importa los objetos request y jsonify de Flask
# request -> acceder a headers, query params, body...
# jsonify -> devolver respuestas JSON
from flask import request, jsonify

# Importa nuestro manejador de JWT personalizado
from Seguridad.jwt_manager import JWTManager

# Crea una instancia del administrador de JWT
# Esto permitirá verificar tokens y desencriptar campos
jwt_manager = JWTManager()


# ===========================================================
# DECORADOR: token_required
# Se usa para proteger endpoints exigiendo un JWT válido
# ===========================================================
def token_required(f):

    # @wraps mantiene intacto el nombre y documentación
    # de la función original (por buenas prácticas)
    @wraps(f)
    def decorated(*args, **kwargs):

        # Inicializamos la variable token
        token = None

        # -------------------------------------------------------
        # EXTRAER TOKEN DEL HEADER Authorization
        # Ejemplo esperado:
        # Authorization: Bearer eyJhbGciOiJIUzI1...
        # -------------------------------------------------------
        if "Authorization" in request.headers:
            # Remueve "Bearer " para obtener solo el token limpio
            token = request.headers["Authorization"].replace("Bearer ", "")

        # Si no llega token, se retorna error inmediatamente
        if not token:
            return jsonify({"error": "Token faltante"}), 401

        # -------------------------------------------------------
        # VERIFICAR TOKEN
        # -------------------------------------------------------
        try:
            # Verifica firma, expiración y campos cifrados
            data = jwt_manager.verify_token(token)

            # Guarda los datos del usuario en request.user
            # Esto permite usar request.user dentro de cualquier endpoint
            request.user = data  # ← ya desencriptado

        except Exception as e:
            # Si falla cualquier cosa en la verificación
            return jsonify({"error": "Token inválido: " + str(e)}), 401

        # Ejecuta la función real si todo está bien
        return f(*args, **kwargs)

    # Retorna la función decorada final
    return decorated
