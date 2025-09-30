from dataclasses import dataclass
from decimal import Decimal

@dataclass
class OrdenTrabajoServicio:
    OrdenTrabajoServicioID: int | None
    OrdenTrabajoID: int
    ServicioID: int
    Cantidad: int
    PrecioUnitario: Decimal
