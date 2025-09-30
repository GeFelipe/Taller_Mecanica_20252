from dataclasses import dataclass

@dataclass
class Proveedor:
    ProveedorID: int | None
    Nombre: str
    Telefono: str | None = None
    Email: str | None = None
    Direccion: str | None = None
