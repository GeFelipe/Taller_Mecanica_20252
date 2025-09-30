from dataclasses import dataclass
from datetime import datetime

@dataclass
class OrdenTrabajo:
    OrdenTrabajoID: int | None
    CitaID: int
    EmpleadoID: int
    FechaInicio: datetime | None = None
    FechaFin: datetime | None = None
    Estado: str = "En Proceso"  # 'En Proceso', 'Finalizada', 'Cancelada'
