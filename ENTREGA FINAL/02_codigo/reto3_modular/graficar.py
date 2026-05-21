"""Graficas del modelo geometrico base.

La figura debe parecerse al enunciado:
- tablero superior recto;
- apoyos extremos altos;
- apoyos interiores bajos;
- arco principal entre las pilas interiores;
- acotamiento S, L, S y H.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from config import ALTURA_H_EXTREMO_M, FIGURE_DIR, PROFUNDIDAD_APOYO_INTERIOR_M
from geometria import posiciones_apoyos
from modelos import Node, Selection


def separar_nodos_por_tipo(nodos: list[Node]) -> tuple[list[Node], list[Node]]:
    """Separa nodos del tablero y nodos del cordon inferior."""

    nodos_tablero = [nodo for nodo in nodos if nodo.es_nodo_tablero]
    nodos_cordon = [nodo for nodo in nodos if nodo.tipo == "cordon_inferior"]

    return nodos_tablero, nodos_cordon


def dibujar_cota_horizontal(
    eje,
    x_inicio_m: float,
    x_fin_m: float,
    y_m: float,
    texto: str,
) -> None:
    """Dibuja una cota horizontal con flechas."""

    eje.annotate(
        "",
        xy=(x_inicio_m, y_m),
        xytext=(x_fin_m, y_m),
        arrowprops={"arrowstyle": "<->", "linewidth": 1.0, "color": "#202020"},
    )
    eje.text(
        (x_inicio_m + x_fin_m) / 2,
        y_m - 1.3,
        texto,
        ha="center",
        va="top",
        fontsize=9,
    )


def dibujar_cota_vertical(
    eje,
    x_m: float,
    y_inicio_m: float,
    y_fin_m: float,
    texto: str,
) -> None:
    """Dibuja una cota vertical con flechas."""

    eje.annotate(
        "",
        xy=(x_m, y_inicio_m),
        xytext=(x_m, y_fin_m),
        arrowprops={"arrowstyle": "<->", "linewidth": 1.0, "color": "#202020"},
    )
    eje.text(
        x_m + 1.2,
        (y_inicio_m + y_fin_m) / 2,
        texto,
        ha="left",
        va="center",
        fontsize=9,
    )


def dibujar_modelo_acotado(
    seleccion: Selection,
    nodos: list[Node],
    altura_h_extremo_m: float | None = ALTURA_H_EXTREMO_M,
    profundidad_apoyo_interior_m: float | None = PROFUNDIDAD_APOYO_INTERIOR_M,
) -> None:
    """Genera la figura del modelo geometrico acotado."""

    if altura_h_extremo_m is None or profundidad_apoyo_interior_m is None:
        raise ValueError(
            "H esta pendiente de diseno. No se puede dibujar figura definitiva."
        )

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    nodos_tablero, nodos_cordon = separar_nodos_por_tipo(nodos)
    apoyos_x = posiciones_apoyos(
        seleccion.luz_lateral_m,
        seleccion.luz_principal_m,
    )
    nodos_apoyo = [nodo for nodo in nodos if nodo.es_nodo_apoyo]

    figura, eje = plt.subplots(figsize=(15, 5.8))

    # Contorno exterior del puente.
    eje.plot(
        [nodo.x_m for nodo in nodos_tablero],
        [nodo.y_m for nodo in nodos_tablero],
        color="#202020",
        linewidth=2.4,
    )
    eje.plot(
        [nodo.x_m for nodo in nodos_cordon],
        [nodo.y_m for nodo in nodos_cordon],
        color="#202020",
        linewidth=2.4,
    )

    # Nodos del modelo.
    eje.scatter(
        [nodo.x_m for nodo in nodos_tablero],
        [nodo.y_m for nodo in nodos_tablero],
        color="#f3f3f3",
        edgecolor="#202020",
        linewidth=0.7,
        s=24,
        zorder=4,
    )
    eje.scatter(
        [nodo.x_m for nodo in nodos_cordon],
        [nodo.y_m for nodo in nodos_cordon],
        color="#d65f2f",
        edgecolor="#202020",
        linewidth=0.4,
        s=24,
        zorder=4,
    )

    # Apoyos exactamente sobre el cordon inferior.
    eje.scatter(
        [nodo.x_m for nodo in nodos_apoyo],
        [nodo.y_m for nodo in nodos_apoyo],
        marker="^",
        color="#0b6e4f",
        edgecolor="#0b6e4f",
        s=135,
        zorder=5,
    )

    for nodo in nodos_apoyo:
        eje.text(
            nodo.x_m,
            nodo.y_m - 1.8,
            f"{nodo.x_m:.0f} m",
            ha="center",
            va="top",
            fontsize=8,
        )

    # Lineas de referencia vertical en los apoyos.
    for x_m in apoyos_x:
        eje.axvline(x_m, color="#87919b", linewidth=0.8, linestyle="--", alpha=0.65)

    # Acotamiento horizontal S-L-S.
    y_cota_m = -profundidad_apoyo_interior_m - 6.0
    dibujar_cota_horizontal(
        eje,
        0.0,
        seleccion.luz_lateral_m,
        y_cota_m,
        f"S = {seleccion.luz_lateral_m} m",
    )
    dibujar_cota_horizontal(
        eje,
        seleccion.luz_lateral_m,
        seleccion.luz_lateral_m + seleccion.luz_principal_m,
        y_cota_m,
        f"L = {seleccion.luz_principal_m} m",
    )
    dibujar_cota_horizontal(
        eje,
        seleccion.luz_lateral_m + seleccion.luz_principal_m,
        seleccion.longitud_total_m,
        y_cota_m,
        f"S = {seleccion.luz_lateral_m} m",
    )

    # Cota H en apoyo extremo, como aparece en la guia.
    x_cota_h_m = seleccion.longitud_total_m + 3.0
    dibujar_cota_vertical(
        eje,
        x_cota_h_m,
        0.0,
        -altura_h_extremo_m,
        f"H = {altura_h_extremo_m:.1f} m",
    )

    # Textos cortos para reconocer la forma del enunciado.
    eje.text(4.0, 2.2, "Tablero superior recto", fontsize=8, ha="left")
    eje.text(
        seleccion.luz_lateral_m + seleccion.luz_principal_m / 2,
        -altura_h_extremo_m - 3.0,
        "R",
        fontsize=12,
        ha="center",
    )
    eje.text(seleccion.longitud_total_m - 18.0, -24.0, "r", fontsize=12, ha="center")

    eje.set_title("Modelo base acotado segun figura del reto")
    eje.set_xlabel("x (m)")
    eje.set_ylabel("y (m)")
    eje.set_aspect("equal", adjustable="box")
    eje.grid(True, alpha=0.22)
    eje.set_xlim(-4.0, seleccion.longitud_total_m + 9.0)
    eje.set_ylim(y_cota_m - 5.0, 5.0)

    figura.tight_layout()
    figura.savefig(
        FIGURE_DIR / "modelo_base_reto_acotado.png",
        dpi=220,
    )
    plt.close(figura)
