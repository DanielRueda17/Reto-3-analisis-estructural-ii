"""Estructuras de datos simples para el reto.

Este archivo solo define "moldes" de datos. No calcula nada.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Selection:
    """Resultado de la seleccion aleatoria."""

    luz_principal_m: int
    luz_lateral_m: int
    tipo_cercha: str
    semilla: str

    @property
    def longitud_total_m(self) -> int:
        """Longitud total del puente: S + L + S."""

        return 2 * self.luz_lateral_m + self.luz_principal_m


@dataclass(frozen=True)
class Node:
    """Punto del modelo estructural."""

    id: int
    x_m: float
    y_m: float
    tipo: str
    es_nodo_tablero: bool = False
    es_nodo_apoyo: bool = False


@dataclass(frozen=True)
class ArcGeometry:
    """Datos geometricos de un arco circular."""

    cuerda_m: float
    flecha_m: float
    radio_m: float


@dataclass(frozen=True)
class CandidateGeometry:
    """Geometria generada para una altura candidata H."""

    h_m: float
    profundidad_apoyo_interior_m: float
    arco_principal: ArcGeometry
    arco_lateral: ArcGeometry
    nodos: list[Node]


@dataclass(frozen=True)
class Element:
    """Barra de la cercha."""

    id: int
    nodo_i: int
    nodo_j: int
    familia: str
    longitud_m: float


@dataclass(frozen=True)
class Section:
    """Propiedades de una seccion HSS del catalogo AISC."""

    nombre: str
    alto_in: float
    ancho_in: float
    espesor_in: float
    peso_lb_ft: float
    area_in2: float
    ix_in4: float
    iy_in4: float
    rx_in: float
    ry_in: float
    pagina_catalogo: int

    @property
    def area_m2(self) -> float:
        """Area en m2."""

        return self.area_in2 * 0.00064516
