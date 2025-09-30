from dataclasses import dataclass
from datetime import date

@dataclass
class Cliente:
    ClienteID: int | None
    Nombre: str
    Apellido: str
    Telefono: str | None = None
    Email: str | None = None
    Direccion: str | None = None
    FechaRegistro: date | None = None
