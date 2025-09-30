from dataclasses import dataclass
from datetime import datetime

@dataclass
class HistorialVehiculo:
    HistorialID: int | None
    VehiculoID: int
    OrdenTrabajoID: int
    Observaciones: str | None = None
    FechaRegistro: datetime | None = None
