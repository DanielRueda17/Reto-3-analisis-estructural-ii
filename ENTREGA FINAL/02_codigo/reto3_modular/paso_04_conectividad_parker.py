"""Paso 4: conectividad Parker para geometria candidata.

Este script NO calcula fuerzas ni define H final.
Solo genera la tabla de barras para revisar la topologia de la cercha.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict

import matplotlib.pyplot as plt

from config import ROOT
from conectividad_parker import construir_elementos_parker, resumen_familias
from geometria_candidata import construir_geometria_para_h
from seleccion import elegir_geometria_aleatoria


SALIDA_TMP = ROOT / "tmp" / "paso_04_conectividad_parker"


def guardar_nodos(carpeta_h, geometria) -> None:
    """Guarda los nodos de la geometria candidata."""

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


def guardar_elementos(carpeta_h, elementos) -> None:
    """Guarda la conectividad de barras Parker."""

    with (carpeta_h / "elementos.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "id",
                "nodo_i",
                "nodo_j",
                "familia",
                "longitud_m",
            ]
        )
        for elemento in elementos:
            writer.writerow(
                [
                    elemento.id,
                    elemento.nodo_i,
                    elemento.nodo_j,
                    elemento.familia,
                    f"{elemento.longitud_m:.3f}",
                ]
            )


def guardar_vista_conectividad(carpeta_h, geometria, elementos) -> None:
    """Dibuja una vista rapida de la conectividad candidata."""

    nodos_por_id = {nodo.id: nodo for nodo in geometria.nodos}
    estilos = {
        "cuerda_superior": {"color": "#202020", "linewidth": 2.0},
        "cuerda_inferior": {"color": "#202020", "linewidth": 2.0},
        "montante": {"color": "#2f6f9f", "linewidth": 1.0},
        "diagonal_parker": {"color": "#b24c2f", "linewidth": 1.0},
    }

    figura, eje = plt.subplots(figsize=(15, 5.0))

    for elemento in elementos:
        nodo_i = nodos_por_id[elemento.nodo_i]
        nodo_j = nodos_por_id[elemento.nodo_j]
        estilo = estilos[elemento.familia]
        eje.plot(
            [nodo_i.x_m, nodo_j.x_m],
            [nodo_i.y_m, nodo_j.y_m],
            **estilo,
        )

    for nodo in geometria.nodos:
        if nodo.es_nodo_apoyo:
            eje.scatter(
                nodo.x_m,
                nodo.y_m,
                marker="^",
                color="#0b6e4f",
                s=110,
                zorder=5,
            )
        else:
            eje.scatter(
                nodo.x_m,
                nodo.y_m,
                color="#f4f4f4" if nodo.es_nodo_tablero else "#d65f2f",
                edgecolor="#202020",
                linewidth=0.5,
                s=18,
                zorder=4,
            )

    eje.set_title(f"Conectividad Parker candidata - H = {geometria.h_m:.1f} m")
    eje.set_xlabel("x (m)")
    eje.set_ylabel("y (m)")
    eje.set_aspect("equal", adjustable="box")
    eje.grid(True, alpha=0.22)
    figura.tight_layout()
    figura.savefig(carpeta_h / "vista_conectividad.png", dpi=180)
    plt.close(figura)


def guardar_conectividad_candidata(h_m: float) -> None:
    """Guarda una conectividad Parker para una H candidata."""

    seleccion = elegir_geometria_aleatoria()
    geometria = construir_geometria_para_h(
        seleccion=seleccion,
        h_m=h_m,
    )
    elementos = construir_elementos_parker(
        seleccion=seleccion,
        geometria=geometria,
    )

    carpeta_h = SALIDA_TMP / f"H_{h_m:.1f}m"
    carpeta_h.mkdir(parents=True, exist_ok=True)

    resumen = {
        "estado": "conectividad_candidata_no_aprobada",
        "L_m": seleccion.luz_principal_m,
        "S_m": seleccion.luz_lateral_m,
        "tipo_cercha": seleccion.tipo_cercha,
        "h_m": geometria.h_m,
        "nodos": len(geometria.nodos),
        "elementos": len(elementos),
        "familias": resumen_familias(elementos),
        "arco_principal_R": asdict(geometria.arco_principal),
        "arco_lateral_r": asdict(geometria.arco_lateral),
        "nota": (
            "Conectividad Parker generada para revision. "
            "No define H final ni secciones."
        ),
    }

    (carpeta_h / "resumen_conectividad.json").write_text(
        json.dumps(resumen, indent=2),
        encoding="utf-8",
    )
    guardar_nodos(carpeta_h, geometria)
    guardar_elementos(carpeta_h, elementos)
    guardar_vista_conectividad(carpeta_h, geometria, elementos)


def main() -> None:
    """Genera conectividad para tres H candidatas."""

    for h_m in [6.0, 8.0, 10.0]:
        guardar_conectividad_candidata(h_m)

    print("Paso 4 generado solo para revision.")
    print(f"Carpeta = {SALIDA_TMP}")
    print("Casos = H 6.0 m, 8.0 m, 10.0 m")
    print("Estado = conectividades candidatas no aprobadas")


if __name__ == "__main__":
    main()
