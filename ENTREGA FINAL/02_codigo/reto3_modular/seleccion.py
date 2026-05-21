"""Seleccion aleatoria reproducible de L, S y tipologia.

Esta es la primera parte del reto:
1. Crear las listas de valores permitidos por el enunciado.
2. Fijar una semilla para que el resultado pueda repetirse.
3. Escoger L, S y tipo de cercha.
"""

import random

from config import SEED
from modelos import Selection


def elegir_geometria_aleatoria(semilla: str = SEED) -> Selection:
    """Selecciona L, S y tipologia con una semilla fija."""

    generador_aleatorio = random.Random(semilla)

    # Valores permitidos por el enunciado para la luz principal L.
    opciones_luz_principal = list(range(80, 121, 2))

    # Valores permitidos por el enunciado para cada luz lateral S.
    opciones_luz_lateral = list(range(20, 31, 2))

    # Tipologias indicadas en el anexo del reto.
    opciones_tipo_cercha = [
        "Pratt",
        "Parker",
        "K-Truss",
        "Howe",
        "Camelback",
        "Warren",
        "Fink",
        "Double Intersection Pratt",
        "Warren con verticales",
        "Bowstring",
        "Baltimore",
        "Double Intersection Warren",
        "Waddell A Truss",
        "Pennsylvania",
        "Lattice",
    ]

    return Selection(
        luz_principal_m=generador_aleatorio.choice(opciones_luz_principal),
        luz_lateral_m=generador_aleatorio.choice(opciones_luz_lateral),
        tipo_cercha=generador_aleatorio.choice(opciones_tipo_cercha),
        semilla=semilla,
    )


# Alias corto para mantener compatibilidad si algun archivo viejo llama este nombre.
choose_random_geometry = elegir_geometria_aleatoria
