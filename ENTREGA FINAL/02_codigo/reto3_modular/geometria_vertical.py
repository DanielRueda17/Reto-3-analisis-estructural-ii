"""Estado de la geometria vertical del reto.

El PDF no entrega un valor numerico de H. El PDF pide disenar H.
Por eso este modulo no calcula una H definitiva ni la toma de la imagen.
Solo deja registrado que H es una variable pendiente de diseno.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from config import DATA_DIR


@dataclass(frozen=True)
class EstadoGeometriaVertical:
    """Estado actual de H y de la geometria vertical."""

    h_estado: str
    h_valor_m: float | None
    profundidad_apoyo_interior_m: float | None
    criterio_correcto: str
    criterio_no_permitido: str
    siguiente_paso: str


def estado_geometria_vertical() -> EstadoGeometriaVertical:
    """Devuelve el estado vigente de la variable H."""

    return EstadoGeometriaVertical(
        h_estado="pendiente_de_diseno",
        h_valor_m=None,
        profundidad_apoyo_interior_m=None,
        criterio_correcto=(
            "Disenar H por iteracion estructural: proponer alturas candidatas, "
            "modelar la cercha, aplicar el mayor numero simultaneo de camiones "
            "y verificar deflexiones L/800 y S/800."
        ),
        criterio_no_permitido=(
            "No definir H por simetria, proporcion grafica, estetica o lectura "
            "aproximada de la figura."
        ),
        siguiente_paso=(
            "Aprobar el procedimiento de diseno de H antes de generar "
            "coordenadas finales o calculos."
        ),
    )


def guardar_estado_geometria_vertical(estado: EstadoGeometriaVertical) -> None:
    """Guarda el estado de H para que no se confunda con un resultado."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    ruta_json = DATA_DIR / "estado_h_pendiente.json"
    ruta_json.write_text(json.dumps(asdict(estado), indent=2), encoding="utf-8")

    texto = [
        "# Estado de la altura H",
        "",
        "`H` no esta definida todavia.",
        "",
        "## Razon",
        "",
        "El PDF indica que se debe disenar la altura `H` para cumplir el limite",
        "de deflexion. Por tanto, `H` no debe tomarse por simetria, proporcion",
        "grafica ni lectura aproximada de la figura.",
        "",
        "## Estado vigente",
        "",
        f"- Estado: `{estado.h_estado}`.",
        "- Valor adoptado: ninguno.",
        "",
        "## Criterio correcto",
        "",
        estado.criterio_correcto,
        "",
        "## Proximo paso",
        "",
        estado.siguiente_paso,
    ]
    ruta_md = DATA_DIR / "estado_h_pendiente.md"
    ruta_md.write_text("\n".join(texto) + "\n", encoding="utf-8")
