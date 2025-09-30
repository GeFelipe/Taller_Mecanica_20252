from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Factura:
    FacturaID: int | None
    OrdenTrabajoID: int
    FechaEmision: datetime | None = None
    Subtotal: Decimal | None = None
    IVA: Decimal | None = None
    Total: Decimal | None = None
