"""Conectividad interna Parker para una geometria candidata.

Este modulo arma las barras de la cercha:
- cuerda superior;
- cuerda inferior;
- montantes;
- diagonales Parker.

Todavia no asigna secciones AISC ni calcula rigidez.
"""

from __future__ import annotations

import math

from geometria import posiciones_apoyos
from modelos import CandidateGeometry, Element, Node, Selection


def longitud_barra(nodo_i: Node, nodo_j: Node) -> float:
    """Longitud de una barra entre dos nodos."""

    return math.hypot(nodo_j.x_m - nodo_i.x_m, nodo_j.y_m - nodo_i.y_m)


def mapear_nodos_por_tipo_y_x(
    nodos: list[Node],
    tipo: str,
) -> dict[float, Node]:
    """Crea un diccionario x -> nodo para un tipo de nodo."""

    return {
        nodo.x_m: nodo
        for nodo in nodos
        if nodo.tipo == tipo
    }


def agregar_elemento(
    elementos: list[Element],
    nodos_por_id: dict[int, Node],
    existentes: set[tuple[int, int, str]],
    nodo_i: Node,
    nodo_j: Node,
    familia: str,
) -> None:
    """Agrega una barra evitando duplicados y barras de longitud cero."""

    if nodo_i.id == nodo_j.id:
        return

    longitud_m = longitud_barra(nodo_i, nodo_j)
    if longitud_m <= 1e-9:
        return

    clave = (min(nodo_i.id, nodo_j.id), max(nodo_i.id, nodo_j.id), familia)
    if clave in existentes:
        return

    existentes.add(clave)
    elementos.append(
        Element(
            id=len(elementos),
            nodo_i=nodo_i.id,
            nodo_j=nodo_j.id,
            familia=familia,
            longitud_m=longitud_m,
        )
    )

    # Lectura defensiva: asegura que los nodos existen en el modelo.
    _ = nodos_por_id[nodo_i.id]
    _ = nodos_por_id[nodo_j.id]


def coordenadas_x_por_tramo(
    coordenadas_x: list[float],
    inicio_m: float,
    fin_m: float,
) -> list[float]:
    """Filtra las coordenadas x que pertenecen a un tramo."""

    return [
        x_m
        for x_m in coordenadas_x
        if inicio_m - 1e-9 <= x_m <= fin_m + 1e-9
    ]


def construir_elementos_parker(
    seleccion: Selection,
    geometria: CandidateGeometry,
) -> list[Element]:
    """Construye la conectividad Parker para una geometria candidata."""

    nodos = geometria.nodos
    nodos_por_id = {nodo.id: nodo for nodo in nodos}
    nodos_tablero = mapear_nodos_por_tipo_y_x(nodos, "tablero")
    nodos_cordon = mapear_nodos_por_tipo_y_x(nodos, "cordon_inferior")
    coordenadas_x = sorted(nodos_tablero)

    elementos: list[Element] = []
    existentes: set[tuple[int, int, str]] = set()

    # Cuerda superior: tablero recto.
    for x_i, x_j in zip(coordenadas_x[:-1], coordenadas_x[1:]):
        agregar_elemento(
            elementos,
            nodos_por_id,
            existentes,
            nodos_tablero[x_i],
            nodos_tablero[x_j],
            "cuerda_superior",
        )

    apoyos = posiciones_apoyos(
        seleccion.luz_lateral_m,
        seleccion.luz_principal_m,
    )

    # Cada luz se arma por separado para que las diagonales cambien en su centro.
    for inicio_m, fin_m in zip(apoyos[:-1], apoyos[1:]):
        xs_tramo = coordenadas_x_por_tramo(coordenadas_x, inicio_m, fin_m)
        centro_tramo_m = (inicio_m + fin_m) / 2

        # Cuerda inferior: sigue el cordon curvo.
        for x_i, x_j in zip(xs_tramo[:-1], xs_tramo[1:]):
            agregar_elemento(
                elementos,
                nodos_por_id,
                existentes,
                nodos_cordon[x_i],
                nodos_cordon[x_j],
                "cuerda_inferior",
            )

        # Montantes: unen tablero y cordon inferior.
        for x_m in xs_tramo:
            agregar_elemento(
                elementos,
                nodos_por_id,
                existentes,
                nodos_tablero[x_m],
                nodos_cordon[x_m],
                "montante",
            )

        # Diagonales Parker: se orientan hacia el centro del tramo.
        for x_i, x_j in zip(xs_tramo[:-1], xs_tramo[1:]):
            centro_panel_m = (x_i + x_j) / 2

            if centro_panel_m <= centro_tramo_m:
                nodo_i = nodos_cordon[x_i]
                nodo_j = nodos_tablero[x_j]
            else:
                nodo_i = nodos_tablero[x_i]
                nodo_j = nodos_cordon[x_j]

            agregar_elemento(
                elementos,
                nodos_por_id,
                existentes,
                nodo_i,
                nodo_j,
                "diagonal_parker",
            )

    return elementos


def resumen_familias(elementos: list[Element]) -> dict[str, int]:
    """Cuenta barras por familia."""

    resumen: dict[str, int] = {}
    for elemento in elementos:
        resumen[elemento.familia] = resumen.get(elemento.familia, 0) + 1
    return resumen
