from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Repuesto:
    RepuestoID: int | None
    ProveedorID: int
    Nombre: str
    Descripcion: str | None = None
    PrecioUnitario: Decimal | None = None
    StockActual: int = 0
