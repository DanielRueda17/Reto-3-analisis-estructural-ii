"""Exportacion de resultados intermedios.

Estas funciones no calculan: solo guardan archivos para revisar.
"""

import csv
import json

from config import DATA_DIR, MODEL_DIR
from modelos import Node, Selection


def save_selection(selection: Selection) -> None:
    """Guarda la seleccion aleatoria."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "semilla": selection.semilla,
        "L_m": selection.luz_principal_m,
        "S_m": selection.luz_lateral_m,
        "longitud_total_m": selection.longitud_total_m,
        "tipo_cercha": selection.tipo_cercha,
    }

    path = DATA_DIR / "seleccion_modelo_base_reto.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_nodes(nodes: list[Node]) -> None:
    """Guarda nodos en CSV para revision."""

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    path = MODEL_DIR / "coordenadas_modelo_base_reto.csv"

    with path.open("w", newline="", encoding="utf-8") as file:
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

        for node in nodes:
            writer.writerow(
                [
                    node.id,
                    f"{node.x_m:.3f}",
                    f"{node.y_m:.3f}",
                    node.tipo,
                    node.es_nodo_tablero,
                    node.es_nodo_apoyo,
                ]
            )
