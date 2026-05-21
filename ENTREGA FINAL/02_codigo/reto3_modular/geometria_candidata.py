"""Geometria para una altura candidata H.

Este modulo corresponde al paso 3:
para una H candidata se calculan coordenadas y radios R, r.

Importante:
- H entra como dato candidato, no como resultado definitivo.
- R y r se calculan con geometria de circunferencia.
- Aqui todavia no se calculan fuerzas ni deflexiones.
"""

from __future__ import annotations

import math

from geometria import coordenadas_x_tablero, posiciones_apoyos
from modelos import ArcGeometry, CandidateGeometry, Node, Selection


def calcular_radio_arco(cuerda_m: float, flecha_m: float) -> float:
    """Calcula el radio de un arco circular.

    Formula:
        R = c^2 / (8f) + f / 2

    donde:
    - c = cuerda del arco, en m;
    - f = flecha del arco, en m.
    """

    if cuerda_m <= 0:
        raise ValueError("La cuerda del arco debe ser positiva.")
    if flecha_m <= 0:
        raise ValueError("La flecha del arco debe ser positiva.")

    return cuerda_m**2 / (8 * flecha_m) + flecha_m / 2


def crear_arco_circular(cuerda_m: float, flecha_m: float) -> ArcGeometry:
    """Crea los datos basicos de un arco circular."""

    return ArcGeometry(
        cuerda_m=cuerda_m,
        flecha_m=flecha_m,
        radio_m=calcular_radio_arco(cuerda_m, flecha_m),
    )


def coordenada_y_arco_entre_apoyos(
    x_m: float,
    x_inicio_m: float,
    x_fin_m: float,
    y_apoyo_m: float,
    flecha_m: float,
) -> float:
    """Devuelve la coordenada y de un arco circular entre dos apoyos.

    La flecha se mide verticalmente desde el apoyo hacia arriba.
    Como el tablero esta en y = 0, las coordenadas del cordon inferior
    quedan negativas.
    """

    cuerda_m = x_fin_m - x_inicio_m
    radio_m = calcular_radio_arco(cuerda_m, flecha_m)
    centro_x_m = (x_inicio_m + x_fin_m) / 2
    distancia_centro_m = x_m - centro_x_m
    y_circulo_m = math.sqrt(max(radio_m**2 - distancia_centro_m**2, 0.0))

    # Ajuste para que el arco pase por y_apoyo_m en los extremos.
    return y_apoyo_m + y_circulo_m - (radio_m - flecha_m)


def coordenada_y_arco_entre_dos_puntos(
    x_m: float,
    punto_inicio: tuple[float, float],
    punto_fin: tuple[float, float],
    flecha_m: float,
) -> float:
    """Coordenada y de un arco circular entre dos puntos.

    La flecha se mide perpendicular a la cuerda. Se usa la normal con componente
    vertical negativa para que el arco quede por debajo de la cuerda.
    """

    x_inicio_m, y_inicio_m = punto_inicio
    x_fin_m, y_fin_m = punto_fin
    dx_m = x_fin_m - x_inicio_m
    dy_m = y_fin_m - y_inicio_m
    cuerda_m = math.hypot(dx_m, dy_m)

    if cuerda_m <= 0:
        raise ValueError("Los puntos del arco no pueden coincidir.")

    t_x = dx_m / cuerda_m
    t_y = dy_m / cuerda_m
    normal_x = t_y
    normal_y = -t_x

    if normal_y > 0:
        normal_x *= -1
        normal_y *= -1

    radio_m = calcular_radio_arco(cuerda_m, flecha_m)
    distancia_centro_cuerda_m = radio_m - flecha_m
    punto_medio_x_m = (x_inicio_m + x_fin_m) / 2
    punto_medio_y_m = (y_inicio_m + y_fin_m) / 2

    # Si el arco baja respecto a la cuerda, el centro queda al lado opuesto.
    centro_x_m = punto_medio_x_m - distancia_centro_cuerda_m * normal_x
    centro_y_m = punto_medio_y_m - distancia_centro_cuerda_m * normal_y

    raiz_m = math.sqrt(max(radio_m**2 - (x_m - centro_x_m) ** 2, 0.0))
    y_1_m = centro_y_m + raiz_m
    y_2_m = centro_y_m - raiz_m

    # Se toma la rama inferior porque el cordon inferior va debajo del tablero.
    return min(y_1_m, y_2_m)


def construir_geometria_para_h(
    seleccion: Selection,
    h_m: float,
    relacion_profundidad_interior: float = 2.5,
    relacion_flecha_lateral: float = 0.15,
) -> CandidateGeometry:
    """Construye una geometria candidata para una altura H.

    `relacion_profundidad_interior` controla cuanto mas bajos quedan los apoyos
    interiores respecto a H. No es resultado final: es un parametro geometrico
    que se puede barrer junto con H si hace falta.
    """

    if h_m <= 0:
        raise ValueError("H debe ser positiva.")
    if relacion_profundidad_interior <= 1:
        raise ValueError("La profundidad interior debe ser mayor que H.")
    if relacion_flecha_lateral <= 0:
        raise ValueError("La flecha lateral debe ser positiva.")

    apoyos = posiciones_apoyos(
        seleccion.luz_lateral_m,
        seleccion.luz_principal_m,
    )
    x_0, x_s, x_s_l, x_total = apoyos
    profundidad_apoyo_interior_m = h_m * relacion_profundidad_interior

    y_extremo_m = -h_m
    y_interior_m = -profundidad_apoyo_interior_m

    # Arco principal R: de pila interior izquierda a pila interior derecha.
    # Su flecha sube desde los apoyos interiores hasta una profundidad H.
    flecha_principal_m = profundidad_apoyo_interior_m - h_m
    arco_principal = crear_arco_circular(
        cuerda_m=seleccion.luz_principal_m,
        flecha_m=flecha_principal_m,
    )

    # Arcos laterales r: se calculan sobre la cuerda real entre apoyo extremo
    # y apoyo interior. La flecha lateral es libre y revisable.
    cuerda_lateral_m = math.hypot(
        seleccion.luz_lateral_m,
        profundidad_apoyo_interior_m - h_m,
    )
    flecha_lateral_m = relacion_flecha_lateral * seleccion.luz_lateral_m
    arco_lateral = crear_arco_circular(
        cuerda_m=cuerda_lateral_m,
        flecha_m=flecha_lateral_m,
    )

    nodos: list[Node] = []
    coordenadas_x = coordenadas_x_tablero(
        seleccion.luz_lateral_m,
        seleccion.luz_principal_m,
    )

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

    for x_m in coordenadas_x:
        if x_0 <= x_m <= x_s:
            y_m = coordenada_y_arco_entre_dos_puntos(
                x_m=x_m,
                punto_inicio=(x_0, y_extremo_m),
                punto_fin=(x_s, y_interior_m),
                flecha_m=flecha_lateral_m,
            )
        elif x_s <= x_m <= x_s_l:
            y_m = coordenada_y_arco_entre_apoyos(
                x_m=x_m,
                x_inicio_m=x_s,
                x_fin_m=x_s_l,
                y_apoyo_m=y_interior_m,
                flecha_m=flecha_principal_m,
            )
        else:
            y_m = coordenada_y_arco_entre_dos_puntos(
                x_m=x_m,
                punto_inicio=(x_s_l, y_interior_m),
                punto_fin=(x_total, y_extremo_m),
                flecha_m=flecha_lateral_m,
            )

        nodos.append(
            Node(
                id=len(nodos),
                x_m=x_m,
                y_m=y_m,
                tipo="cordon_inferior",
                es_nodo_apoyo=any(math.isclose(x_m, apoyo) for apoyo in apoyos),
            )
        )

    return CandidateGeometry(
        h_m=h_m,
        profundidad_apoyo_interior_m=profundidad_apoyo_interior_m,
        arco_principal=arco_principal,
        arco_lateral=arco_lateral,
        nodos=nodos,
    )
