# Importa la librería PyJWT para crear y verificar tokens JWT
import jwt

# Manejo de fechas para definir tiempos de expiración en el JWT
import datetime

# Importa nuestra clase personalizada para cifrado AES
from Seguridad.aes_cipher import AESCipher

# Para obtener variables de entorno como la clave secreta del JWT
import os


# Lista de campos internos del payload que deben ser cifrados dentro del token
AES_FIELDS = ["usuario_id", "rol", "cliente_id", "id_sucursal"]


class JWTManager:
    def __init__(self):
        """
        Constructor que inicializa el administrador de JWT.
        Carga la clave secreta desde el entorno, define el algoritmo y
        prepara la instancia de cifrado AES.
        """

        # Clave secreta usada para firmar el JWT
        self.secret = os.environ.get("JWT_SECRET_KEY")

        # Algoritmo de firma del JWT (HS256 = HMAC + SHA256)
        self.algorithm = "HS256"

        # Instancia del cifrador AES para cifrar campos internos
        self.aes = AESCipher()


    def create_token(self, payload):
        """
        Crea un token JWT con:
        - Firmado con HS256
        - Campos internos cifrados con AES
        - Expiración automática
        """

        # Copia del payload para no modificar el original
        payload = payload.copy()

        # Recorre cada campo marcado como sensible
        for field in AES_FIELDS:
            # Si ese campo existe en el payload...
            if field in payload:
                # ...se cifra usando AES y SE REEMPLAZA su valor
                payload[field] = self.aes.encrypt(str(payload[field]))

        # Si el payload no contiene expiración, agregar una de 2 horas por defecto
        payload.setdefault(
            "exp",
            datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        )

        # Crear y firmar el token JWT con el payload final (incluye los campos cifrados)
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)

        # Retornar el token generado como string
        return token


    def verify_token(self, token):
        """
        Verifica la firma del token y decodifica su payload.
        Luego desencripta los campos que fueron protegidos con AES.
        """

        # Decodificar el token JWT y validar la firma con la clave secreta
        decoded = jwt.decode(token, self.secret, algorithms=[self.algorithm])

        # Recorrer los campos que deberían estar cifrados
        for field in AES_FIELDS:
            # Si el campo existe, lo desencripta y lo reemplaza con su valor original
            if field in decoded:
                decoded[field] = self.aes.decrypt(decoded[field])

        # Retornar el payload final totalmente legible
        return decoded
