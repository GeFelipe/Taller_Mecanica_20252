from dataclasses import dataclass

@dataclass
class Vehiculo:
    VehiculoID: int | None
    ClienteID: int
    Placa: str
    Marca: str | None = None
    Modelo: str | None = None
    Anio: int | None = None
    VIN: str | None = None
    Color: str | None = None
