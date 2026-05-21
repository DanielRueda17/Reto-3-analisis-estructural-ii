# Reto 3 - Analisis Estructural II

Repositorio de entrega final y proceso vigente para el reto del puente cercha
metalico de tres luces. El repositorio remoto no contiene el archivo local
completo del proyecto ni versiones preliminares descartadas fuera de
`ENTREGA FINAL/`.

## Leer primero

El documento principal para entender que se va a hacer, como se va a calcular y
como se va a validar es:

- [Plan de solucion completo](ENTREGA%20FINAL/00_criterios/plan_solucion_reto3.md)

Secciones clave dentro del plan:

- [Que se calcula y para que sirve](ENTREGA%20FINAL/00_criterios/plan_solucion_reto3.md#4-explicacion-de-que-se-calcula-y-para-que-sirve)
- [Como se definio la estructura](ENTREGA%20FINAL/00_criterios/plan_solucion_reto3.md#415-como-se-definio-la-estructura)
- [Control del desplazamiento vertical](ENTREGA%20FINAL/00_criterios/plan_solucion_reto3.md#4159-control-del-desplazamiento-vertical)
- [Diseno de H por iteracion](ENTREGA%20FINAL/00_criterios/plan_solucion_reto3.md#fase-9---disenar-h-por-iteracion)

En resumen: `H` se propone como altura candidata; con esa `H` se construyen
radios, nodos, barras y perfiles; luego se aplican cargas y se calcula
`delta_max`. La `H` solo se acepta si la deflexion cumple `L/800` y `S/800`,
ademas de revisar fuerzas axiales, pandeo y secciones.

## Criterios vigentes

- Luz longitudinal: `L = 90 m`.
- Separacion transversal: `S = 28 m`.
- Tipologia interna: `Parker`.
- Semilla de seleccion: `RETO3_ANALISIS_OSCAR_2026`.
- Criterio de deflexion corregido por docente: `L/800` y `S/800`.
- Camion adoptado por el equipo: `CC14 / CCP-14`.
- Secciones de referencia: catalogo AISC suministrado localmente.

## Fuentes base registradas

- `ENTREGA FINAL/00_criterios/decisiones_actualizadas.md`
- `ENTREGA FINAL/00_criterios/camion_diseno_ccp14.md`
- `ENTREGA FINAL/00_criterios/catalogo_AISC_rectangular_fuente.md`
- `ENTREGA FINAL/00_criterios/revision_pdf_y_correcciones.md`

## Regla critica

La altura `H` no se toma de la imagen ni por proporcion grafica. Es una variable de diseno y debe definirse mediante un procedimiento trazable: candidatos de altura, modelo, cargas moviles, verificacion de deflexion y seleccion justificada.

## Estructura versionada

- `ENTREGA FINAL/00_criterios/`: criterios, decisiones y fuentes aceptadas.
- `ENTREGA FINAL/01_seleccion/`: seleccion aleatoria reproducible.
- `ENTREGA FINAL/02_codigo/`: codigo modular vigente.
- `ENTREGA FINAL/03_memoria_y_resultados/`: memoria y resultados vigentes.
