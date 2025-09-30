from dataclasses import dataclass
from datetime import datetime

@dataclass
class InventarioMovimiento:
    MovimientoID: int | None
    RepuestoID: int
    TipoMovimiento: str   # 'Entrada' o 'Salida'
    Cantidad: int
    FechaMovimiento: datetime | None = None
