"""Punto de entrada del codigo modular del Reto 3.

Este archivo debe leerse como el indice del proceso.
Cada linea importante llama una parte del trabajo.
"""

from exportar import save_selection
from geometria_vertical import estado_geometria_vertical, guardar_estado_geometria_vertical
from seleccion import elegir_geometria_aleatoria


def main() -> None:
    # Paso 1: hacer la seleccion aleatoria del enunciado.
    seleccion = elegir_geometria_aleatoria()

    # Paso 2: dejar claro que H aun no esta disenada.
    estado_h = estado_geometria_vertical()

    # Paso 3: guardar solo lo que esta aprobado.
    save_selection(seleccion)
    guardar_estado_geometria_vertical(estado_h)

    print("Seleccion aleatoria")
    print(f"  L = {seleccion.luz_principal_m} m")
    print(f"  S = {seleccion.luz_lateral_m} m")
    print(f"  Tipologia = {seleccion.tipo_cercha}")
    print()
    print("Altura H")
    print("  Estado = pendiente de diseno")
    print("  Archivo = 01_datos/estado_h_pendiente.md")
    print()
    print("Modelo geometrico")
    print("  No se generan coordenadas finales hasta disenar H.")


if __name__ == "__main__":
    main()
