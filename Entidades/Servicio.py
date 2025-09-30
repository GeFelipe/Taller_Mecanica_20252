from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Servicio:
    ServicioID: int | None
    Nombre: str
    Descripcion: str | None = None
    PrecioBase: Decimal | None = None
