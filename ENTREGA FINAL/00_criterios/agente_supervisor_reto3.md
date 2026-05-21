# Agente supervisor del Reto 3

## Objetivo del agente

Supervisar que el desarrollo del reto siga el PDF, las correcciones del docente
y las decisiones aprobadas por el equipo. Este archivo funciona como lista de
control antes de modelar, calcular o entregar resultados.

## Fuente revisada

- `TareaReo#3GB.pdf`, 3 paginas.
- Correccion del docente: usar `L/800` y `S/800`; mantener forma exterior del
  puente; cambiar solo la parte interna segun seleccion aleatoria.

## Requisitos del PDF

| Tema | Exigencia | Fuente |
|---|---|---|
| Luces | Seleccionar `L` entre 80 m y 120 m, incremento 2 m | PDF, pag. 1 |
| Luces laterales | Seleccionar `S` entre 20 m y 30 m, incremento 2 m | PDF, pag. 1 |
| Tipologia | Seleccionar aleatoriamente una cercha del anexo | PDF, pag. 1 |
| Secciones | Usar perfiles tubulares cuadrados AISC | PDF, pags. 1-2 |
| H | Disenar la altura `H` para cumplir deflexion | PDF, pag. 1 |
| Camiones | Mayor numero simultaneo de camiones de diseno | PDF, pag. 1 |
| Radios | `R` y `r` son libres, pero deben pertenecer a circunferencia | PDF, pag. 2 |
| Lineas de influencia | Validar al menos una LI con carga movil unitaria | PDF, pag. 2 |
| Carga final | Hallar carga movil uniforme maxima de 5 m | PDF, pag. 1 |
| Informe | Maximo 5 paginas, con tablas y figuras | PDF, pag. 2 |

## Correcciones del docente

- El criterio de deflexion vigente es `L/800` y `S/800`.
- La forma exterior del puente se conserva.
- Solo se cambia la parte interna de la cercha segun la tipologia seleccionada.

## Decisiones aprobadas del equipo

- Seleccion aleatoria vigente:
  - `L = 90 m`.
  - `S = 28 m`.
  - Tipologia interna: `Parker`.
- Camion adoptado: `CC14 / CCP-14`, documentado en
  `01_datos/camion_diseno_ccp14.md`.

## Bloqueos actuales

- `H` esta pendiente de diseno. No se debe fijar por proporcion grafica.
- Falta definir el procedimiento de iteracion para seleccionar `H`.
- Falta definir radios `R` y `r` como arcos de circunferencia.
- Falta construir la conectividad interna Parker sobre la forma exterior.
- Falta definir secciones AISC iniciales y regla de ajuste.

## Regla de parada

Si aparece un valor de `H` en una figura, tabla, coordenada o archivo de entrega,
debe indicar una de estas dos condiciones:

- `H provisional`: solo para esquema, no valido para calculo.
- `H disenada`: obtenida por iteracion estructural y verificada con `L/800` y
  `S/800`.

Si no cumple una de esas dos, el archivo no puede pasar a `ENTREGA FINAL`.

## Proximo paso correcto

No seguir generando coordenadas finales. El proximo paso es proponer y aprobar el
procedimiento para disenar `H`, incluyendo:

1. rango de alturas candidatas,
2. forma de definir `R` y `r`,
3. modelo de camiones,
4. criterio de seleccion de secciones,
5. verificacion de deflexion.
