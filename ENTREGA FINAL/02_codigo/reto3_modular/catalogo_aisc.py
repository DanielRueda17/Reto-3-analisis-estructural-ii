"""Lectura del catalogo AISC entregado por el docente.

La tabla vigente esta en:
01_datos/secciones_aisc_hss_rectangular.csv

Esa tabla se transcribe desde `catalogo_AISC.pdf`.
"""

from __future__ import annotations

import csv

from config import DATA_DIR
from modelos import Section


RUTA_CATALOGO_PROCESADO = DATA_DIR / "secciones_aisc_hss_rectangular.csv"


def leer_catalogo_rectangular() -> dict[str, Section]:
    """Lee las secciones HSS rectangulares procesadas."""

    secciones: dict[str, Section] = {}

    with RUTA_CATALOGO_PROCESADO.open(newline="", encoding="utf-8-sig") as file:
        lector = csv.DictReader(file)

        for fila in lector:
            seccion = Section(
                nombre=fila["shape"],
                alto_in=float(fila["depth_in"]),
                ancho_in=float(fila["width_in"]),
                espesor_in=float(fila["t_in"]),
                peso_lb_ft=float(fila["weight_lb_ft"]),
                area_in2=float(fila["area_in2"]),
                ix_in4=float(fila["Ix_in4"]),
                iy_in4=float(fila["Iy_in4"]),
                rx_in=float(fila["rx_in"]),
                ry_in=float(fila["ry_in"]),
                pagina_catalogo=int(fila["page"]),
            )
            secciones[seccion.nombre] = seccion

    return secciones


def listar_nombres_secciones() -> list[str]:
    """Lista los nombres disponibles en la tabla procesada."""

    return sorted(leer_catalogo_rectangular())
