from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DetalleTrabajo:
    DetalleTrabajoID: int | None
    OrdenTrabajoID: int
    Descripcion: str | None = None
    ManoDeObraHoras: Decimal | None = None
    CostoManoDeObra: Decimal | None = None
