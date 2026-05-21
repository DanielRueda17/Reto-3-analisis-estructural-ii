# Reto 3 Modular

Este es el codigo nuevo para reconstruir el reto paso a paso.

## Archivos

- `config.py`: rutas y semilla.
- `modelos.py`: clases simples (`Selection`, `Node`).
- `seleccion.py`: seleccion aleatoria de `L`, `S` y tipologia.
- `catalogo_aisc.py`: lee la tabla rectangular procesada desde el catalogo del docente.
- `geometria_vertical.py`: estado de `H`; por ahora queda pendiente de diseno.
- `geometria.py`: funciones para coordenadas, bloqueadas hasta aprobar `H`.
- `geometria_candidata.py`: genera geometria y radios para una `H` candidata.
- `conectividad_parker.py`: arma las barras de la cercha Parker.
- `paso_03_geometria_candidata.py`: crea casos de revision en `tmp`.
- `paso_04_conectividad_parker.py`: crea conectividades candidatas en `tmp`.
- `exportar.py`: guarda archivos `.json` y `.csv`.
- `main.py`: ejecuta el paso actual.

Los nombres internos estan en espanol para que el proceso sea mas facil de seguir.

## Como correr

Desde la carpeta raiz del reto:

```powershell
python scripts\reto3_modular\main.py
```

## Estado actual

El codigo no genera coordenadas finales porque `H` aun no esta disenada.
Primero debe aprobarse el procedimiento para seleccionar `H` por verificacion
de deflexion `L/800` y `S/800`.

La fuente vigente de secciones es `catalogo_AISC.pdf`, entregado por el docente.
La tabla activa es `01_datos/secciones_aisc_hss_rectangular.csv`.

Para revisar el paso 3 sin aprobar una H final:

```powershell
python scripts\reto3_modular\paso_03_geometria_candidata.py
```

Para revisar el paso 4 sin aprobar una H final:

```powershell
python scripts\reto3_modular\paso_04_conectividad_parker.py
```
