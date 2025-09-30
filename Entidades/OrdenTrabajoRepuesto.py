from dataclasses import dataclass
from decimal import Decimal

@dataclass
class OrdenTrabajoRepuesto:
    OrdenTrabajoRepuestoID: int | None
    OrdenTrabajoID: int
    RepuestoID: int
    Cantidad: int
    PrecioUnitario: Decimal
