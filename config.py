# Archivo: config.py

# --- CONFIGURACIÓN DE CONEXIÓN A LA BASE DE DATOS ---
DRIVER_NAME = '{MySQL ODBC 9.4 Unicode Driver}' 
SERVER_NAME = 'localhost'
DATABASE_NAME = 'taller_mecanica'
USER_NAME = 'user_python1'
PASSWORD = '1234'

# Cadena de conexión para pyodbc
CONNECTION_STRING = (
    f'DRIVER={DRIVER_NAME};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    f'UID={USER_NAME};'
    f'PWD={PASSWORD};'
)


