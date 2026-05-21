"""Geometria base del puente segun la figura del reto.

En esta fase solo convertimos la figura en coordenadas.
No se calculan fuerzas, reacciones ni deflexiones.
"""

from __future__ import annotations

import math

from config import ALTURA_H_EXTREMO_M, PROFUNDIDAD_APOYO_INTERIOR_M
from modelos import Node, Selection


def posiciones_apoyos(luz_lateral_m: float, luz_principal_m: float) -> list[float]:
    """Ubicacion de apoyos para el puente S-L-S."""

    return [
        0.0,
        luz_lateral_m,
        luz_lateral_m + luz_principal_m,
        2 * luz_lateral_m + luz_principal_m,
    ]


def coordenadas_x_tablero(luz_lateral_m: int, luz_principal_m: int) -> list[float]:
    """Coordenadas x de los nodos del tablero."""

    # Luces laterales: paneles de 4 m.
    luz_lateral_izquierda = [x for x in range(0, luz_lateral_m + 1, 4)]

    # Luz principal: paneles de 6 m.
    luz_central = [
        luz_lateral_m + x
        for x in range(0, luz_principal_m + 1, 6)
    ]

    # Luz lateral derecha: paneles de 4 m.
    luz_lateral_derecha = [
        luz_lateral_m + luz_principal_m + x
        for x in range(0, luz_lateral_m + 1, 4)
    ]

    return sorted(
        set(
            float(x)
            for x in luz_lateral_izquierda + luz_central + luz_lateral_derecha
        )
    )


def suavizado_coseno(t: float) -> float:
    """Curva suave entre 0 y 1."""

    return 0.5 - 0.5 * math.cos(math.pi * t)


def coordenada_y_cordon_inferior(
    x_m: float,
    seleccion: Selection,
    altura_h_extremo_m: float | None = ALTURA_H_EXTREMO_M,
    profundidad_apoyo_interior_m: float | None = PROFUNDIDAD_APOYO_INTERIOR_M,
) -> float:
    """Coordenada y del cordon inferior de acuerdo con la silueta del reto.

    Convencion:
    - tablero recto en y = 0;
    - apoyos extremos en y = -H;
    - apoyos interiores mas bajos, como muestra la figura;
    - arco principal sube hacia el centro de la luz L.
    """

    if altura_h_extremo_m is None or profundidad_apoyo_interior_m is None:
        raise ValueError(
            "H esta pendiente de diseno. No se pueden generar coordenadas finales."
        )

    apoyo_izquierdo_m, pila_izquierda_m, pila_derecha_m, apoyo_derecho_m = (
        posiciones_apoyos(
            seleccion.luz_lateral_m,
            seleccion.luz_principal_m,
        )
    )

    y_extremo_m = -altura_h_extremo_m
    y_interior_m = -profundidad_apoyo_interior_m

    if apoyo_izquierdo_m <= x_m <= pila_izquierda_m:
        # Lateral izquierda: baja desde el apoyo extremo hasta la pila interior.
        t = (x_m - apoyo_izquierdo_m) / (pila_izquierda_m - apoyo_izquierdo_m)
        return y_extremo_m + (y_interior_m - y_extremo_m) * suavizado_coseno(t)

    if pila_izquierda_m <= x_m <= pila_derecha_m:
        # Luz principal: arco que sube hacia el centro y vuelve a bajar.
        t = (x_m - pila_izquierda_m) / (pila_derecha_m - pila_izquierda_m)
        subida = math.sin(math.pi * t)
        return y_interior_m + (y_extremo_m - y_interior_m) * subida

    if pila_derecha_m <= x_m <= apoyo_derecho_m:
        # Lateral derecha: sube desde la pila interior hasta el apoyo extremo.
        t = (x_m - pila_derecha_m) / (apoyo_derecho_m - pila_derecha_m)
        return y_interior_m + (y_extremo_m - y_interior_m) * suavizado_coseno(t)

    raise ValueError(f"x = {x_m} m esta fuera del puente")


def construir_nodos_puente(
    seleccion: Selection,
    altura_h_extremo_m: float | None = ALTURA_H_EXTREMO_M,
    profundidad_apoyo_interior_m: float | None = PROFUNDIDAD_APOYO_INTERIOR_M,
) -> list[Node]:
    """Crea nodos del tablero recto y del cordon inferior del reto."""

    nodos: list[Node] = []
    coordenadas_x = coordenadas_x_tablero(
        seleccion.luz_lateral_m,
        seleccion.luz_principal_m,
    )
    apoyos = posiciones_apoyos(
        seleccion.luz_lateral_m,
        seleccion.luz_principal_m,
    )

    # Grupo 1: tablero superior recto.
    for x_m in coordenadas_x:
        nodos.append(
            Node(
                id=len(nodos),
                x_m=x_m,
                y_m=0.0,
                tipo="tablero",
                es_nodo_tablero=True,
            )
        )

    # Grupo 2: cordon inferior con la forma exterior del enunciado.
    for x_m in coordenadas_x:
        y_m = coordenada_y_cordon_inferior(
            x_m=x_m,
            seleccion=seleccion,
            altura_h_extremo_m=altura_h_extremo_m,
            profundidad_apoyo_interior_m=profundidad_apoyo_interior_m,
        )
        nodos.append(
            Node(
                id=len(nodos),
                x_m=x_m,
                y_m=y_m,
                tipo="cordon_inferior",
                es_nodo_apoyo=any(
                    math.isclose(x_m, apoyo_x_m)
                    for apoyo_x_m in apoyos
                ),
            )
        )

    return nodos


# Alias para compatibilidad con nombres anteriores.
build_bridge_nodes = construir_nodos_puente
support_positions = posiciones_apoyos
deck_x_coordinates = coordenadas_x_tablero
