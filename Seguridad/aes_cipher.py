# Importa el algoritmo AES para cifrado simétrico
from Crypto.Cipher import AES

# Importa funciones para agregar y remover padding (relleno)
from Crypto.Util.Padding import pad, unpad

# Para codificar/decodificar datos en Base64 (formato seguro para enviar por JSON)
import base64

# Para acceder a variables de entorno y generar bytes aleatorios
import os


class AESCipher:
    def __init__(self, key=None):
        """
        Constructor de la clase AESCipher.
        Si no se proporciona una clave, se toma la del entorno AES_SECRET_KEY.
        AES-256 requiere exactamente 32 bytes de longitud.
        """

        # Obtiene la clave recibida o la carga desde variable de entorno, luego la convierte a bytes
        self.key = key or os.environ.get("AES_SECRET_KEY").encode()

        # Tamaño del bloque usado por AES (generalmente 16 bytes)
        self.bs = AES.block_size


    def encrypt(self, raw):
        """
        Cifra un texto plano usando AES-256 en modo CBC.
        """

        # Convierte el texto de entrada a bytes
        raw = raw.encode()

        # Genera un IV (vector de inicialización) aleatorio del tamaño del bloque
        # Este IV garantiza que dos textos iguales generen cifrados distintos
        iv = os.urandom(self.bs)

        # Crea un objeto de cifrado AES con:
        # - La clave
        # - El modo CBC
        # - El IV generado
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Aplica padding al texto y luego lo cifra
        encrypted = cipher.encrypt(pad(raw, self.bs))

        # Retorna el IV + el texto cifrado, codificados en Base64 para poder enviarlo por JSON
        return base64.b64encode(iv + encrypted).decode()


    def decrypt(self, enc):
        """
        Descifra un texto cifrado previamente con encrypt().
        """

        # Decodifica la entrada desde Base64 de vuelta a bytes
        enc = base64.b64decode(enc)

        # Extrae el IV (los primeros 16 bytes)
        iv = enc[:self.bs]

        # Crea un objeto AES para descifrar usando la misma clave y el IV original
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Descifra el resto del mensaje (todo después del IV) y remueve el padding
        decrypted = unpad(cipher.decrypt(enc[self.bs:]), self.bs)

        # Devuelve el texto descifrado como string
        return decrypted.decode()

