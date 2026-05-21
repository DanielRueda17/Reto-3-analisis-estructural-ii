"""Paso 3: revisar geometria para alturas H candidatas.

Este script NO decide la H final.
Solo genera tablas de prueba para revisar que la geometria se construye bien
cuando se entrega una H candidata.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from config import ROOT
from geometria_candidata import construir_geometria_para_h
from seleccion import elegir_geometria_aleatoria


SALIDA_TMP = ROOT / "tmp" / "paso_03_geometria_candidata"


def guardar_geometria_candidata(h_m: float) -> None:
    """Guarda una geometria candidata para revision."""

    seleccion = elegir_geometria_aleatoria()
    geometria = construir_geometria_para_h(
        seleccion=seleccion,
        h_m=h_m,
    )

    carpeta_h = SALIDA_TMP / f"H_{h_m:.1f}m"
    carpeta_h.mkdir(parents=True, exist_ok=True)

    resumen = {
        "estado": "candidata_no_aprobada",
        "L_m": seleccion.luz_principal_m,
        "S_m": seleccion.luz_lateral_m,
        "tipo_cercha": seleccion.tipo_cercha,
        "h_m": geometria.h_m,
        "profundidad_apoyo_interior_m": (
            geometria.profundidad_apoyo_interior_m
        ),
        "arco_principal_R": asdict(geometria.arco_principal),
        "arco_lateral_r": asdict(geometria.arco_lateral),
        "nota": (
            "Esta geometria sirve para revisar coordenadas y radios. "
            "No define la H final del puente."
        ),
    }

    (carpeta_h / "resumen_geometria.json").write_text(
        json.dumps(resumen, indent=2),
        encoding="utf-8",
    )

    with (carpeta_h / "nodos.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "id",
                "x_m",
                "y_m",
                "tipo",
                "es_nodo_tablero",
                "es_nodo_apoyo",
            ]
        )
        for nodo in geometria.nodos:
            writer.writerow(
                [
                    nodo.id,
                    f"{nodo.x_m:.3f}",
                    f"{nodo.y_m:.3f}",
                    nodo.tipo,
                    nodo.es_nodo_tablero,
                    nodo.es_nodo_apoyo,
                ]
            )


def main() -> None:
    """Genera tres casos pequenos para revisar el paso 3."""

    for h_m in [6.0, 8.0, 10.0]:
        guardar_geometria_candidata(h_m)

    print("Paso 3 generado solo para revision.")
    print(f"Carpeta = {SALIDA_TMP}")
    print("Casos = H 6.0 m, 8.0 m, 10.0 m")
    print("Estado = candidatas no aprobadas")


if __name__ == "__main__":
    main()
