from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Pago:
    PagoID: int | None
    FacturaID: int
    Monto: Decimal
    FechaPago: datetime | None = None
    MetodoPago: str | None = None  # 'Efectivo', 'Tarjeta', 'Transferencia'
