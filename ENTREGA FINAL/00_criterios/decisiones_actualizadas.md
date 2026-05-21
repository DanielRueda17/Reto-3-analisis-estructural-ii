# Decisiones actualizadas del reto

## Respuesta del docente

El docente confirmo que debe usarse el criterio de deflexion:

```text
L/800 y S/800
```

Tambien indico que la guia fue actualizada y que se debe rectificar la propuesta geometrica:

```text
Mantener la forma exterior del puente.
Cambiar solo la parte interna segun la seleccion aleatoria.
```

## Decision de trabajo sobre camion de diseno

Como el enunciado menciona `CCP-15`, pero no se encontro una referencia tecnica clara para ese camion, se adopta para el calculo el camion `CC14` de la norma `CCP-14`, ya documentado en:

```text
01_datos/camion_diseno_ccp14.md
```

Datos que se usaran:

- Eje delantero: `40 kN`.
- Primer eje trasero: `160 kN`.
- Segundo eje trasero: `160 kN`.
- Separacion entre eje delantero y primer eje trasero: `4.30 m`.
- Separacion entre ejes traseros: variable entre `4.30 m` y `9.00 m`.

## Consecuencia para el modelo

Los resultados preliminares con geometria Parker libre quedan como ensayo de metodo. Para el modelo definitivo se debe reconstruir la geometria conservando la forma exterior del puente indicada por la guia y aplicar la tipologia Parker solo en la configuracion interna de la cercha.

## Decision de trabajo sobre catalogo AISC

El catalogo suministrado por el docente en la carpeta del reto es:

```text
catalogo_AISC.pdf
```

Ese archivo corresponde a:

```text
ASTM A1085/A1085M Rectangular HSS
```

Aunque el enunciado menciona perfiles tubulares cuadrados, se adopta el catalogo
entregado por el docente como fuente oficial de secciones. Por tanto, para el
modelo se usaran perfiles HSS rectangulares A1085 tomados de `catalogo_AISC.pdf`.

La tabla reducida previa de HSS cuadrados queda como archivo no vigente y no debe
usarse para el diseno final.
