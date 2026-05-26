from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Categoria:
    id: int
    nombre: str
    icono: str
    color: str


@dataclass
class Gasto:
    id: int
    descripcion: str
    monto: float
    categoria_id: int
    fecha: str
    categoria_nombre: Optional[str] = None
    categoria_color: Optional[str] = None

    @property
    def fecha_formateada(self) -> str:
        try:
            dt = datetime.fromisoformat(self.fecha)
            return dt.strftime("%d/%m/%Y")
        except Exception:
            return self.fecha


CATEGORIAS_DEFAULT = [
    Categoria(1, "Comida",        "RESTAURANT",      "#FF5722"),
    Categoria(2, "Transporte",    "DIRECTIONS_BUS",  "#2196F3"),
    Categoria(3, "Entretenimiento","SPORTS_ESPORTS",  "#9C27B0"),
    Categoria(4, "Salud",         "LOCAL_HOSPITAL",  "#4CAF50"),
    Categoria(5, "Educacion",     "SCHOOL",          "#FF9800"),
    Categoria(6, "Otros",         "CATEGORY",        "#607D8B"),
]
