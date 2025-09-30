from dataclasses import dataclass
from datetime import datetime

@dataclass
class Cita:
    CitaID: int | None
    ClienteID: int
    VehiculoID: int
    FechaHora: datetime
    Motivo: str | None = None
    Estado: str = "Pendiente"  # 'Pendiente', 'Atendida', 'Cancelada'
