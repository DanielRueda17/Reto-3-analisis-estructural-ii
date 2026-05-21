# Plan de solucion - Reto 3 puente cercha

## Resumen corto

El reto se va a resolver construyendo un modelo estructural 2D de una cercha
metalica de tres luces. La idea no es asumir directamente una altura `H`, sino
disenarla mediante iteracion: se prueban alturas candidatas, se arma la
geometria del puente, se asignan secciones AISC, se aplican los camiones de
diseno y se verifica que la deflexion cumpla `L/800` y `S/800`. Cuando el puente
cumpla esa condicion, se usa el modelo definido para hallar la carga movil
uniforme maxima de 5 m y validar al menos una linea de influencia.

El proyecto se esta armando por modulos de codigo para que cada fase se pueda
revisar y defender. Primero se separan los datos del enunciado y las decisiones
del docente; despues se programa la seleccion aleatoria; luego se genera la
geometria para una `H` candidata; despues se arma la conectividad Parker; luego
se asignan secciones del catalogo AISC; y finalmente se construye el modelo de
rigidez, las cargas moviles, la verificacion de deflexion y la carga maxima.

## Analisis inicial realizado

Se reviso el PDF del reto y la respuesta del docente. Del enunciado se
identifico que se debe seleccionar aleatoriamente la luz principal `L`, las luces
laterales `S` y la tipologia de cercha. Tambien se identifico que la altura `H`
no es un dato fijo: el enunciado pide disenarla para que la deflexion vertical
maxima cumpla el criterio indicado. Por correccion del docente, el criterio que
gobierna es `L/800` para la luz principal y `S/800` para las luces laterales.

Tambien se reviso la correccion geometrica del docente: se debe mantener la
forma exterior del puente y solo cambiar la parte interna segun la tipologia
aleatoria. Por eso, la solucion no debe partir de una cercha Parker libre, sino
de una geometria exterior consistente con la guia, con una configuracion interna
Parker. Ademas, se reviso el catalogo entregado por el docente y se encontro que
corresponde a `ASTM A1085/A1085M Rectangular HSS`; por decision de trabajo se
usara ese catalogo oficial, aunque el enunciado mencione tubulares cuadrados.

## Decisiones vigentes

- Seleccion aleatoria vigente:
  - `L = 90 m`.
  - `S = 28 m`.
  - Tipologia interna: `Parker`.
- Longitud total del puente:
  - `2S + L = 2(28) + 90 = 146 m`.
- Criterio de deflexion:
  - Luz principal: `L/800 = 90/800 = 0.1125 m = 112.5 mm`.
  - Luces laterales: `S/800 = 28/800 = 0.0350 m = 35.0 mm`.
- `H` queda como variable de diseno, no como valor tomado de la figura.
- Se adopta el camion `CC14 / CCP-14` como modelo de trabajo, pendiente de
  confirmacion final con el ingeniero.
- Se usara `catalogo_AISC.pdf` como fuente oficial de secciones.
- La tabla reducida anterior de HSS cuadrados queda archivada como no vigente.

## Estructura general del codigo

El codigo se esta organizando en la carpeta:

```text
scripts/reto3_modular/
```

La intencion es que cada archivo haga una sola parte del proceso:

- `config.py`: guarda rutas generales y la semilla de seleccion.
- `modelos.py`: define las estructuras de datos principales.
- `seleccion.py`: realiza la seleccion aleatoria de `L`, `S` y tipologia.
- `geometria_vertical.py`: deja registrado que `H` esta pendiente de diseno.
- `geometria_candidata.py`: genera geometria para una `H` candidata.
- `conectividad_parker.py`: arma las barras internas tipo Parker.
- `catalogo_aisc.py`: lee la tabla de secciones tomada del catalogo del docente.
- `paso_03_geometria_candidata.py`: genera casos de revision de geometria.
- `paso_04_conectividad_parker.py`: genera casos de revision de conectividad.

## Plan de solucion paso a paso

### Paso 1 - Lectura del enunciado y decisiones

Objetivo: separar lo que viene del PDF, lo que corrigio el docente y lo que
queda pendiente. Esta fase evita convertir una suposicion en resultado. Para
eso se documentaron las decisiones en `00_enunciado/decisiones_actualizadas.md`
y se creo un supervisor del proyecto en `AGENTS.md` y
`00_enunciado/agente_supervisor_reto3.md`.

En esta fase se decidio que el criterio correcto de deflexion es `L/800` y
`S/800`, que la forma exterior del puente debe conservarse, que la parte interna
sera Parker y que `H` se debe disenar. Tambien se dejo registrado que el catalogo
vigente sera el PDF entregado por el docente.

### Paso 2 - Seleccion aleatoria reproducible

Objetivo: obtener `L`, `S` y tipologia de forma reproducible. Para esto se usa
el codigo `seleccion.py`, donde se programo la funcion:

```python
elegir_geometria_aleatoria()
```

Esta funcion usa la semilla `RETO3_ANALISIS_OSCAR_2026` y selecciona:

```text
L = 90 m
S = 28 m
tipologia = Parker
```

La intencion de este codigo es que el resultado no dependa de una eleccion a
mano, sino de un proceso repetible que se pueda mostrar en el informe.

### Paso 3 - Geometria para una H candidata

Objetivo: construir la geometria del puente para una altura candidata `H`, sin
decir todavia que esa `H` es definitiva. Esta parte se programa en:

```text
geometria_candidata.py
```

Alli se pretende que la funcion:

```python
construir_geometria_para_h(seleccion, h_m)
```

reciba una altura candidata `H` y genere:

- nodos del tablero superior,
- nodos del cordon inferior,
- posicion de apoyos,
- radio principal `R`,
- radio lateral `r`.

Los radios se calculan como arcos de circunferencia usando la relacion
geometrica:

```text
R = c^2/(8f) + f/2
```

donde `c` es la cuerda del arco y `f` es la flecha. Esta fase es necesaria
porque el PDF dice que `R` y `r` son libres, pero deben pertenecer a una
circunferencia.

El script:

```text
paso_03_geometria_candidata.py
```

genera casos temporales para revisar, por ejemplo `H = 6 m`, `H = 8 m` y
`H = 10 m`. Esos archivos se guardan en `tmp/`, no en entrega final, porque son
geometrias candidatas.

### Paso 4 - Conectividad interna Parker

Objetivo: convertir la geometria en una cercha 2D con barras. Esta fase no
calcula fuerzas todavia; solo define que nodo se conecta con que nodo. Se
programo en:

```text
conectividad_parker.py
```

La funcion principal es:

```python
construir_elementos_parker(seleccion, geometria)
```

Esta funcion toma los nodos generados para una `H` candidata y crea las barras
por familia:

- `cuerda_superior`: barras horizontales del tablero superior.
- `cuerda_inferior`: barras que siguen el cordon inferior.
- `montante`: barras verticales entre tablero y cordon inferior.
- `diagonal_parker`: diagonales orientadas hacia el centro de cada luz.

El script:

```text
paso_04_conectividad_parker.py
```

genera tablas de nodos, tablas de elementos y una vista de revision. Para una
prueba con `H = 8 m`, el modelo candidato produjo:

```text
nodos = 60
elementos = 117
cuerda_superior = 29
cuerda_inferior = 29
montantes = 30
diagonales Parker = 29
```

Esto sirve para revisar la topologia antes de asignar secciones y calcular.

### Paso 5 - Catalogo AISC y secciones candidatas

Objetivo: asignar secciones reales del catalogo a cada familia de barras. Se
reviso que el catalogo entregado por el docente es:

```text
catalogo_AISC.pdf
ASTM A1085/A1085M Rectangular HSS
```

Por eso se creo una tabla inicial:

```text
01_datos/secciones_aisc_hss_rectangular.csv
```

y un lector:

```text
catalogo_aisc.py
```

La funcion que se pretende usar es:

```python
leer_catalogo_rectangular()
```

Esta funcion lee las secciones disponibles con propiedades como:

- area `A`,
- peso nominal,
- inercias `Ix`, `Iy`,
- radios de giro `rx`, `ry`,
- espesor,
- pagina del catalogo.

El siguiente codigo a construir debe asignar secciones candidatas a:

```text
cuerda_superior
cuerda_inferior
montantes
diagonales
```

La idea es enriquecer cada barra con seccion, area, peso y capacidad axial
simple. Con eso el modelo ya queda listo para armar rigidez.

### Paso 6 - Modelo estructural 2D de cercha

Objetivo: armar el modelo matematico de la cercha. Despues de tener nodos,
barras y areas, se construira un codigo que arme la rigidez axial de cada barra:

```text
k = EA/L
```

Para esto se necesitara programar funciones que:

- creen grados de libertad por nodo,
- ensamblen la matriz global de rigidez,
- apliquen restricciones en los apoyos,
- apliquen cargas nodales equivalentes,
- resuelvan desplazamientos,
- calculen reacciones,
- calculen fuerzas axiales en barras.

Este paso convierte el dibujo en un modelo estructural 2D verificable.

### Paso 7 - Cargas de camiones y diseno de H

Objetivo: disenar `H` por deflexion. Para cada altura candidata y conjunto de
secciones, se aplicara el mayor numero simultaneo de camiones sobre el puente.
El codigo debe mover o ubicar los camiones sobre la longitud total de `146 m` y
calcular la deflexion vertical maxima.

La condicion de aceptacion sera:

```text
deflexion en luz principal <= 112.5 mm
deflexion en luces laterales <= 35.0 mm
```

La `H` final sera la menor altura que cumpla esas deflexiones con secciones
razonables del catalogo. Si una altura no cumple, se ajusta `H`, secciones o
ambas.

### Paso 8 - Carga movil uniforme de 5 m

Objetivo: con el puente ya definido, hallar la carga maxima uniforme movil de
5 m. Para esto el codigo debe mover una carga distribuida de longitud `5 m`
desde izquierda a derecha y evaluar la respuesta critica.

La carga maxima se expresara como:

```text
q_max en kN/m
W_max = q_max * 5 m
```

La condicion que gobierne puede ser resistencia axial, deflexion o la condicion
que se acuerde revisar con el ingeniero.

### Paso 9 - Lineas de influencia

Objetivo: obtener lineas de influencia de elementos o respuestas criticas y
validar al menos una con la definicion de carga movil unitaria. El codigo debe
mover una carga unitaria de `1 kN` por el tablero y registrar la respuesta de un
elemento seleccionado.

Esta validacion es importante porque el PDF no solo pide resultados, sino
comprobar al menos una linea de influencia.

### Paso 10 - Verificacion y documentacion final

Objetivo: organizar resultados para sustentacion e informe. La idea es dejar:

- seleccion aleatoria,
- geometria final,
- `H` disenada,
- secciones AISC usadas,
- verificacion de deflexion,
- carga movil maxima,
- linea de influencia validada,
- tablas y figuras principales.

El informe final debe tener maximo 5 paginas, por lo que la documentacion debe
ser compacta y apoyada en tablas y figuras claras.

## Cosas pendientes de confirmar con el ingeniero

1. Confirmar que se acepta usar el catalogo rectangular `catalogo_AISC.pdf`,
   aunque el enunciado mencione tubulares cuadrados.
2. Confirmar que el camion de trabajo `CC14 / CCP-14` es aceptable ante la duda
   del `CCP-15`.
3. Confirmar si se debe incluir peso propio de la cercha o solo las cargas
   indicadas en la guia.
4. Confirmar si el modelo 2D de cercha axial es suficiente para el alcance del
   reto.
5. Confirmar si la carga movil uniforme de 5 m debe controlarse por resistencia,
   deflexion o ambas.
6. Confirmar si se permite seleccionar libremente `R` y `r` mientras sean arcos
   de circunferencia.

## Estado actual del avance

El proyecto ya tiene la estructura base para seleccionar luces, generar
geometrias candidatas, calcular radios circulares y construir la conectividad
Parker. Lo que sigue es terminar la base del catalogo AISC rectangular, asignar
secciones candidatas y construir el modelo de rigidez para empezar a verificar
deflexiones. En este momento el avance es metodologico y de modelacion; todavia
no existe una `H` final ni una carga maxima final.
