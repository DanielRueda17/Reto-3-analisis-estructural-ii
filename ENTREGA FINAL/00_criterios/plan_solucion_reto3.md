# Plan de solucion completo - Reto 3 puente cercha

## 0. Proposito del plan

Este documento define que se va a hacer, en que orden, con que variables, que se
calcula, que se verifica y que archivo debe respaldar cada resultado. La idea es
evitar trabajar a ciegas: antes de decir que una geometria, una altura `H` o una
seccion sirve, debe existir un calculo trazable.

La variable mas delicada del reto es la altura `H`. `H` no es la flecha. `H` es
una dimension geometrica de la cercha. La flecha o deflexion vertical maxima se
representa como `delta_max` o `Delta_max`, y es una respuesta del modelo bajo
carga. El diseno de `H` se controla principalmente verificando que la flecha
calculada no supere la flecha admisible.

## 1. Datos vigentes y unidades

| Dato | Valor | Unidad | Estado | Fuente |
|---|---:|---|---|---|
| Luz principal `L` | 90 | m | vigente | seleccion aleatoria |
| Luz lateral `S` | 28 | m | vigente | seleccion aleatoria |
| Longitud total `2S + L` | 146 | m | vigente | calculo directo |
| Tipologia interna | Parker | - | vigente | seleccion aleatoria |
| Camion de trabajo | CC14 / CCP-14 | - | vigente del equipo | `camion_diseno_ccp14.md` |
| Catalogo de secciones | AISC HSS rectangular ASTM A1085/A1085M | - | vigente | catalogo docente |
| Criterio de deflexion principal | `L/800` | m o mm | vigente | correccion docente |
| Criterio de deflexion lateral | `S/800` | m o mm | vigente | correccion docente |

Deflexiones admisibles:

```text
delta_adm,L = L/800 = 90/800 = 0.1125 m = 112.5 mm
delta_adm,S = S/800 = 28/800 = 0.0350 m = 35.0 mm
```

Convencion de unidades para el modelo:

```text
longitudes: m
fuerzas: kN
modulo E: kN/m2
areas: m2
desplazamientos: m y mm en tablas finales
esfuerzos axiales: kN
carga uniforme movil: kN/m
```

## 2. Variables importantes del diseno

| Variable | Que significa | Se elige o se calcula | Como se controla |
|---|---|---|---|
| `L` | luz principal | dato seleccionado | fija |
| `S` | luz lateral | dato seleccionado | fija |
| `H` | altura geometrica de la cercha | se propone por iteracion | se acepta si cumple deflexion y secciones |
| `R` | radio del arco principal | se calcula para cada `H` | debe formar circunferencia |
| `r` | radio de arcos laterales | se calcula para cada `H` | debe formar circunferencia |
| `delta_max` | flecha/deflexion vertical maxima calculada | se calcula | debe ser menor o igual a la admisible |
| `delta_adm` | flecha/deflexion admisible | se calcula con `L/800` y `S/800` | criterio de servicio |
| `A` | area de cada perfil | se toma del catalogo | afecta rigidez y resistencia |
| `I`, `rx`, `ry` | propiedades de seccion | se toman del catalogo | sirven para revision de pandeo y criterio de seccion |
| `N` | fuerza axial en barra | se calcula | se compara contra capacidad |
| `q_max` | carga uniforme movil maxima de 5 m | se calcula al final | limitada por deflexion y/o resistencia |

Relacion fisica clave:

```text
Momento global aproximado ~= fuerza en cordones * H
fuerza en cordones ~= Momento global / H
```

Por eso una `H` pequena aumenta fuerzas internas y normalmente aumenta flecha.
Una `H` mayor suele reducir flecha, pero tambien cambia longitudes, angulos,
peso y riesgo de pandeo. Por eso no se fija por dibujo: se itera.

## 3. Controles de calidad obligatorios

Todo resultado importante debe responder:

```text
fuente
metodo
unidad
archivo de respaldo
estado: provisional, pendiente, vigente o aprobado
```

Reglas:

- Ningun valor de `H` pasa como definitivo sin verificar `delta_max`.
- Ninguna flecha se reporta sin unidad y sin comparacion contra `delta_adm`.
- Ninguna seccion se acepta si no viene del catalogo AISC disponible.
- Ningun resultado numerico se presenta como final si viene de una geometria
  preliminar.
- `08_archivo_preliminar/` queda fuera de entrega final.
- `ENTREGA FINAL/` solo contiene el proceso vigente y archivos aprobados o en
  revision actual.

## 4. Explicacion de que se calcula y para que sirve

Esta seccion es la guia mental del trabajo. Si una variable aparece en el
calculo, debe tener una razon. Si no ayuda a tomar una decision, no debe
meterse como resultado principal.

### 4.1 Luz, cuerda y longitud total

Que se tiene:

```text
L = 90 m
S = 28 m
longitud total = 2S + L = 146 m
```

Para que sirve:

- `L` controla la luz principal y el limite de deflexion `L/800`.
- `S` controla las luces laterales y el limite de deflexion `S/800`.
- La longitud total `146 m` define el recorrido completo del camion y de la
  carga uniforme movil de 5 m.
- La cuerda `c` de cada arco es la distancia horizontal entre los extremos de
  ese arco. Se necesita para calcular el radio geometrico `R` o `r`.

Como se valida:

```text
2S + L = 2(28) + 90 = 146 m
delta_adm,L = 90/800 = 112.5 mm
delta_adm,S = 28/800 = 35.0 mm
```

Decision que permite:

```text
define limites de servicio y dominio de carga movil
```

### 4.2 Altura H

Que es:

```text
H = altura geometrica de la cercha
```

Para que sirve:

- Define la posicion vertical del cordon o arco respecto al tablero.
- Cambia los angulos de diagonales y montantes.
- Cambia las longitudes de barras.
- Cambia la rigidez global del puente.
- Cambia la flecha `delta_max`.
- Cambia las fuerzas axiales en cordones y diagonales.
- Cambia el peso y el riesgo de pandeo.

Por que no se toma de la imagen:

```text
El enunciado pide disenar H. Si el PDF pide disenar, H no es dato fijo.
```

Como se valida:

```text
para cada H -> modelo -> cargas -> delta_max -> comparar con L/800 y S/800
```

Decision que permite:

```text
aceptar o rechazar una altura de cercha
```

### 4.3 Flecha estructural delta_max

Que es:

```text
delta_max = deflexion vertical maxima bajo carga
```

Para que sirve:

- Controla el estado de servicio.
- Indica si el puente se deforma demasiado aunque no se rompa.
- Es el criterio principal para aceptar o rechazar `H`.

Como se calcula:

```text
1. armar matriz K
2. aplicar cargas F
3. resolver K*u = F
4. tomar desplazamientos verticales uy
5. buscar el maximo valor absoluto: delta_max = max(|uy|)
```

Como se valida:

```text
delta_max,L <= 112.5 mm
delta_max,S <= 35.0 mm
```

Decision que permite:

```text
si cumple, la H candidata puede seguir a revision de resistencia
si no cumple, se aumenta H, se cambian secciones o se corrige el modelo
```

### 4.4 Flecha geometrica del arco o sagita f

Que es:

```text
f = sagita geometrica del arco circular
```

No es lo mismo que `delta_max`.

Para que sirve:

- Permite calcular el radio de un arco circular.
- Ayuda a construir la forma exterior exigida por la guia.
- Da coordenadas de nodos sobre una curva coherente, no inventada punto a
  punto.

Formula:

```text
R = c^2/(8f) + f/2
```

Donde:

```text
c = cuerda horizontal del arco
f = sagita geometrica del arco
R = radio del arco
```

Como se valida:

- Los puntos generados deben caer sobre la circunferencia.
- El arco debe conservar la forma exterior de la guia.
- Las coordenadas deben ser consistentes y sin saltos raros.

Decision que permite:

```text
construir geometria exterior valida antes de calcular barras
```

### 4.5 Radios R y r

Que son:

```text
R = radio del arco principal
r = radio de los arcos laterales
```

Para que sirven:

- Definen la curvatura exterior del puente.
- Permiten calcular coordenadas del cordon curvo.
- Afectan longitudes de barras.
- Afectan angulos internos.
- Afectan rigidez y esfuerzos.

Como se calculan:

```text
con la cuerda de cada tramo y la sagita geometrica correspondiente
```

Como se validan:

- Deben producir arcos de circunferencia.
- No deben contradecir la forma exterior del puente.
- Deben quedar documentados con unidades en m.

Decision que permiten:

```text
pasar de dimensiones generales a coordenadas reales de nodos
```

### 4.6 Nodos

Que son:

```text
puntos donde se conectan barras, apoyos y cargas
```

Para que sirven:

- Definen la geometria del modelo.
- Permiten aplicar cargas.
- Permiten obtener desplazamientos.
- Permiten construir barras entre pares de puntos.

Que se guarda:

```text
id_nodo
x [m]
y [m]
tipo: tablero, cordon, apoyo, etc.
estado: provisional o final
```

Como se validan:

- No debe haber nodos duplicados innecesarios.
- No debe haber coordenadas absurdas.
- Los apoyos deben caer donde corresponde.
- La longitud total debe cerrar en `146 m`.

Decision que permiten:

```text
definir la malla estructural y los puntos donde se calculan desplazamientos
```

### 4.7 Barras y conectividad

Que son:

```text
barras = elementos entre dos nodos
conectividad = lista nodo_i -> nodo_j
```

Para que sirven:

- Transforman el dibujo en una cercha.
- Definen por donde viajan las fuerzas.
- Permiten armar la matriz de rigidez.

Que se calcula por barra:

```text
longitud L_barra
angulo
familia
cosenos directores
rigidez axial EA/L_barra
```

Como se valida:

- No debe haber barras de longitud cero.
- No debe haber barras duplicadas.
- La cercha no debe quedar con mecanismos.
- La distribucion debe parecer una Parker: diagonales organizadas hacia zonas
  coherentes, montantes y cordones definidos.

Decision que permite:

```text
saber si la topologia sirve antes de gastar tiempo en cargas y secciones
```

### 4.8 Secciones AISC

Que son:

```text
perfiles reales del catalogo con area, peso e inercias
```

Para que sirven:

- El area `A` entra en la rigidez axial `EA/L`.
- El peso puede entrar como peso propio.
- Los radios de giro `rx`, `ry` sirven para pandeo.
- La capacidad de la seccion sirve para revisar resistencia.

Como se validan:

- Deben venir del catalogo entregado.
- Deben tener unidades claras.
- Debe quedar registrada la fuente/pagina.
- No se deben inventar areas.

Decision que permiten:

```text
convertir la geometria en una estructura con rigidez y capacidad reales
```

### 4.9 Rigidez del modelo

Que es:

```text
la relacion entre cargas y desplazamientos
```

Para una barra de cercha:

```text
k = E*A/L_barra
```

Para que sirve:

- Permite calcular desplazamientos.
- Permite calcular flecha `delta_max`.
- Permite calcular fuerzas axiales.

Como se valida:

- La matriz global no debe ser singular despues de aplicar apoyos.
- Las reacciones deben equilibrar las cargas.
- Si se duplican cargas, desplazamientos y fuerzas deben duplicarse en analisis
  lineal.
- Si se aumenta `A`, la flecha debe bajar, no subir sin razon.
- Si se aumenta `H`, normalmente la flecha debe bajar, salvo cambios de
  geometria o secciones que expliquen lo contrario.

Decision que permite:

```text
confiar en que el modelo responde fisicamente
```

### 4.10 Cargas moviles

Que son:

```text
cargas que no se quedan en un solo punto; se desplazan sobre el puente
```

Para que sirven:

- El camion no siempre produce el maximo efecto en el centro.
- Una barra puede ser critica con el camion en otra posicion.
- La linea de influencia existe precisamente para estudiar efectos moviles.

Como se aplican:

```text
1. definir ejes y cargas del camion
2. ubicar el camion en una posicion x
3. convertir ejes a cargas nodales equivalentes
4. resolver el modelo
5. guardar delta_max, reacciones y fuerzas
6. mover el camion y repetir
```

Como se validan:

- La suma de cargas aplicadas debe coincidir con el peso del camion/convoy.
- La posicion del camion debe estar dentro del puente.
- La respuesta debe variar suavemente al mover la carga.
- La posicion critica debe tener sentido fisico.

Decision que permiten:

```text
encontrar el caso mas desfavorable, no solo un caso bonito
```

### 4.11 Fuerzas axiales N

Que son:

```text
N = fuerza interna en cada barra
```

Para que sirven:

- Indican que barras trabajan a tension.
- Indican que barras trabajan a compresion.
- Permiten revisar resistencia.
- Permiten detectar barras criticas.

Como se validan:

- Signos coherentes: tension y compresion separados.
- Equilibrio global de reacciones.
- Barras de cordon deben tener fuerzas altas en zonas de mayor momento.
- Diagonales deben activarse segun posicion de carga.

Decision que permiten:

```text
aceptar, aumentar o cambiar secciones
```

### 4.12 Pandeo

Que es:

```text
riesgo de inestabilidad en barras comprimidas
```

Para que sirve:

- Una barra puede tener area suficiente pero fallar por ser larga y esbelta.
- La `H` cambia longitudes y por eso puede mejorar flecha pero empeorar alguna
  esbeltez.

Que se revisa:

```text
KL/r
N_compresion
capacidad aproximada de compresion
ratio demanda/capacidad
```

Como se valida:

- Revisar barras comprimidas criticas.
- Revisar que `KL/r` no sea absurdo.
- Si una barra falla por pandeo, aumentar seccion o cambiar familia de seccion.

Decision que permite:

```text
no aceptar una solucion flexible o inestable aunque cumpla flecha
```

### 4.13 Linea de influencia

Que es:

```text
respuesta de una barra, reaccion o desplazamiento cuando una carga unitaria se
mueve por el puente
```

Para que sirve:

- Muestra donde una carga movil produce el maximo efecto.
- Valida la posicion critica del camion.
- Es requisito del enunciado.

Como se calcula:

```text
1. escoger respuesta a estudiar
2. mover carga unitaria de 1 kN
3. resolver el modelo en cada posicion
4. registrar respuesta
5. graficar respuesta contra posicion x
```

Como se valida:

- Debe tener forma continua o razonablemente suave.
- El maximo debe coincidir con posiciones criticas esperables.
- La respuesta con una carga real puede estimarse combinando ordenadas de la LI.

Decision que permite:

```text
justificar por que una posicion de carga es critica
```

### 4.14 Carga uniforme movil maxima de 5 m

Que es:

```text
una carga distribuida q [kN/m] aplicada sobre una longitud movil de 5 m
```

Para que sirve:

- Es uno de los resultados pedidos.
- Mide cuanto aguanta el puente ante una carga repartida corta que se mueve.

Como se calcula:

```text
1. fijar una posicion de la carga de 5 m
2. transformar q en cargas nodales equivalentes
3. resolver el modelo
4. revisar flecha y fuerzas
5. mover la carga
6. aumentar q hasta que algun criterio llegue al limite
```

Como se valida:

- `W = q * 5 m`.
- La suma de cargas nodales debe ser `W`.
- La posicion critica debe quedar reportada.
- Debe decir que gobierna: deflexion, tension, compresion o pandeo.

Decision que permite:

```text
reportar q_max y W_max de forma defendible
```

### 4.15 Como se definio la estructura

Esta es la parte que no se puede dejar a adivinanza. La estructura no aparece
magicamente: se arma pasando de la guia a un modelo de nodos, barras, secciones,
cargas y controles.

#### 4.15.1 Sistema de coordenadas

Primero se fija un sistema simple:

```text
x = distancia horizontal a lo largo del puente [m]
y = altura vertical [m]
tablero superior recto: y = 0
cordon inferior: y negativo, debajo del tablero
```

Para que se hace:

- Para que todos los nodos tengan coordenadas claras.
- Para que las cargas del camion se puedan ubicar por posicion `x`.
- Para que los desplazamientos verticales salgan como `uy`.
- Para que la flecha estructural se mida como movimiento vertical respecto al
  tablero.

Como se valida:

- El puente debe empezar en `x = 0 m`.
- El puente debe terminar en `x = 146 m`.
- El tablero debe quedar horizontal en `y = 0`.
- El cordon inferior debe quedar debajo del tablero, con `y < 0`.

#### 4.15.2 Apoyos

Con `S = 28 m` y `L = 90 m`, los apoyos quedan en:

```text
apoyo extremo izquierdo: x = 0 m
pila interior izquierda: x = 28 m
pila interior derecha: x = 28 + 90 = 118 m
apoyo extremo derecho: x = 146 m
```

Para que se hace:

- Los apoyos son los puntos donde la estructura entrega carga al suelo.
- Sirven para imponer restricciones en el modelo.
- Sin apoyos bien definidos, la matriz de rigidez puede quedar como mecanismo.

Como se valida:

```text
0 + S = 28 m
S + L = 118 m
2S + L = 146 m
```

Decision que permite:

```text
definir donde se restringen desplazamientos y donde se separan las tres luces
```

#### 4.15.3 Panelizacion del tablero

El codigo vigente divide el tablero asi:

```text
luces laterales S = 28 m -> paneles cada 4 m
luz principal L = 90 m -> paneles cada 6 m
```

Para que se hace:

- Para tener puntos donde conectar montantes y diagonales.
- Para tener nodos donde aplicar cargas equivalentes del camion.
- Para que la cercha no sea una sola barra larga, sino un sistema triangulado.
- Para que la linea de influencia y la carga movil puedan moverse por puntos
  discretos.

Que significa:

```text
No es que el puente real solo pueda tener esos puntos.
Es una discretizacion del modelo para calcular.
```

Como se valida:

- Los puntos deben incluir `0`, `28`, `118` y `146`.
- No deben quedar paneles fuera de las luces.
- No debe haber nodos duplicados.
- La discretizacion debe ser suficientemente clara para representar la cercha.

Decision que permite:

```text
definir cuantos nodos y barras tendra el modelo
```

#### 4.15.4 Definicion de H dentro de la geometria

Para cada altura candidata `H`, el modelo no dice "esta es la definitiva". Dice:

```text
esta es una H provisional para probar
```

En el codigo candidato actual se usa:

```text
y_extremo = -H
profundidad_apoyo_interior = 2.5H
y_interior = -2.5H
```

Esto quiere decir:

- En los apoyos extremos el cordon inferior baja hasta `-H`.
- En los apoyos interiores baja mas, siguiendo la forma exterior de la guia.
- Esa relacion `2.5H` es un parametro geometrico provisional; no debe quedar
  como verdad final sin aprobacion.

Para que se hace:

- Para poder generar una silueta exterior compatible con la guia.
- Para que cada `H` produzca una geometria completa.
- Para que se pueda comparar una altura contra otra con el mismo procedimiento.

Como se valida:

- La geometria debe conservar la forma exterior.
- Cada `H` debe quedar marcada como candidata.
- Si la relacion `2.5H` no representa bien la guia, se cambia o se barre como
  otro parametro.

Decision que permite:

```text
pasar de "H es pendiente" a "voy a probar esta H y ver si cumple"
```

#### 4.15.5 Radios R y r

Para construir los arcos no se inventan puntos sueltos. Se calcula un arco de
circunferencia.

Se usa:

```text
R = c^2/(8f) + f/2
```

Donde:

```text
c = cuerda del arco
f = sagita geometrica del arco
```

En el modelo:

- `R` representa el radio del arco de la luz principal.
- `r` representa el radio de los arcos laterales.

Para que se hace:

- Para que la forma exterior sea geometrica, no dibujada a ojo.
- Para que los nodos del cordon inferior caigan sobre una curva controlada.
- Para que las longitudes y angulos de barras salgan de coordenadas reales.

Como afecta el calculo:

- Cambia la posicion de los nodos del cordon inferior.
- Cambia la longitud de montantes y diagonales.
- Cambia la rigidez `EA/L` porque cambia `L_barra`.
- Cambia la flecha estructural `delta_max`.
- Cambia fuerzas axiales.

Como se valida:

- Los extremos del arco deben coincidir con apoyos o puntos definidos.
- El radio debe ser positivo.
- La curva debe pasar por los puntos esperados.
- Las unidades deben quedar en m.

Decision que permite:

```text
definir la forma exterior antes de armar barras
```

#### 4.15.6 Nodos del modelo

Luego se crean dos grupos de nodos:

```text
1. nodos del tablero superior: y = 0
2. nodos del cordon inferior: y segun arco y H candidata
```

Se usan las mismas posiciones `x` para tablero y cordon inferior.

Para que se hace:

- El tablero recibe las cargas del camion.
- El cordon inferior ayuda a cerrar la cercha.
- Los montantes conectan tablero y cordon inferior.
- Las diagonales triangulan el sistema.

Como se valida:

- Cada nodo debe tener `id`, `x`, `y` y tipo.
- No debe haber nodos repetidos con el mismo papel.
- Los nodos de apoyo deben coincidir con `x = 0, 28, 118, 146`.
- La forma debe poder graficarse y entenderse antes de calcular.

Decision que permite:

```text
tener puntos reales donde conectar barras y aplicar cargas
```

#### 4.15.7 Barras de la cercha

Con los nodos listos, se agregan barras por familia:

```text
cuerda_superior: une nodos consecutivos del tablero
cuerda_inferior: une nodos consecutivos del cordon inferior
montantes: unen tablero y cordon inferior en la misma x
diagonales_parker: unen tablero y cordon con inclinacion hacia el centro del tramo
```

Para que se hace cada familia:

- `cuerda_superior`: transmite compresion o tension longitudinal segun la zona y
  ayuda a formar el borde superior de la cercha.
- `cuerda_inferior`: cierra el sistema y trabaja como el otro cordon principal.
- `montantes`: llevan carga vertical del tablero hacia el sistema de cercha.
- `diagonales_parker`: triangulan los paneles para que el modelo no sea un
  mecanismo y para que las cargas viajen por esfuerzos axiales.

Como se hizo la diagonal Parker:

```text
en cada luz se identifica el centro del tramo
si el panel esta antes del centro, la diagonal se orienta hacia el centro
si el panel esta despues del centro, la diagonal cambia de sentido
```

Para que se hace:

- Esa orientacion representa una tipologia Parker interna.
- Evita poner diagonales al azar.
- Hace que la estructura tenga una logica de transferencia de cargas.

Como se valida:

- No debe haber barras de longitud cero.
- No debe haber barras duplicadas.
- Cada barra debe conectar nodos existentes.
- Cada luz debe tener cuerda superior, cuerda inferior, montantes y diagonales.
- La figura de conectividad debe verse como cercha, no como lineas sin sentido.

Decision que permite:

```text
pasar de una geometria dibujada a una estructura calculable
```

#### 4.15.8 Asignacion de perfiles

Despues de tener barras, cada barra necesita una seccion AISC.

La asignacion no es decorativa. Sirve porque:

```text
rigidez axial de barra = E*A/L_barra
```

Si no hay perfil, no hay `A`. Si no hay `A`, no hay rigidez real. Si no hay
rigidez real, no se puede calcular flecha ni fuerzas de forma defendible.

Regla inicial de asignacion:

```text
cordones -> perfiles mas robustos
diagonales -> perfiles intermedios
montantes -> perfiles menores o intermedios
```

Por que:

- Los cordones suelen tomar las fuerzas principales asociadas al momento global.
- Las diagonales toman cortante y cambian mucho con la posicion del camion.
- Los montantes transfieren carga vertical y estabilizan paneles.

Como se valida:

- Cada perfil debe existir en el catalogo.
- Cada barra debe tener una familia y una seccion.
- Si la flecha queda muy alta, se aumenta `H` o se aumentan areas.
- Si una barra falla por fuerza axial o pandeo, se cambia su perfil.
- No se acepta una seccion porque "se ve bien"; se acepta por demanda/capacidad
  y por deflexion.

Decision que permite:

```text
dar rigidez y capacidad real a la cercha
```

#### 4.15.9 Control del desplazamiento vertical

El desplazamiento vertical no se controla mirando el dibujo. Se controla con el
modelo de rigidez.

Procedimiento:

```text
1. construir nodos
2. construir barras
3. asignar perfiles
4. calcular rigidez EA/L de cada barra
5. ensamblar matriz global K
6. aplicar apoyos
7. aplicar cargas del camion
8. resolver desplazamientos u
9. tomar desplazamientos verticales uy
10. hallar delta_max
11. comparar contra L/800 y S/800
```

Para que se hace:

- Para saber si la estructura se baja mas de lo permitido.
- Para decidir si la `H` candidata sirve.
- Para decidir si toca aumentar perfiles.

Como se valida:

```text
delta_max,L <= 112.5 mm
delta_max,S <= 35.0 mm
```

Ademas:

- Si se aumenta el area de perfiles, la deflexion deberia bajar.
- Si se aumenta `H`, la deflexion normalmente deberia bajar.
- Si el resultado contradice esa tendencia, se revisan unidades, apoyos, cargas
  y conectividad.

Decision que permite:

```text
aceptar o rechazar la rigidez global del puente
```

#### 4.15.10 Como se sabe que el modelo no esta mal armado

No basta con que el programa entregue numeros. Hay que revisar:

Geometria:

```text
x inicial = 0 m
x final = 146 m
apoyos en 0, 28, 118, 146 m
tablero en y = 0
cordon inferior debajo del tablero
```

Topologia:

```text
sin barras duplicadas
sin barras de longitud cero
sin nodos desconectados importantes
sin mecanismos
diagonales coherentes con Parker
```

Unidades:

```text
E en kN/m2
A en m2
L_barra en m
F en kN
u en m
delta final en mm
```

Equilibrio:

```text
suma de cargas verticales ~= suma de reacciones verticales
```

Sensibilidad fisica:

```text
si aumento carga -> aumenta delta
si aumento area -> baja delta
si aumento H razonablemente -> baja delta
si quito una barra importante -> el modelo cambia fuerte o falla
```

Comparacion externa:

```text
revisar una corrida simple en Ftool o con calculo manual simplificado
```

Decision que permite:

```text
confiar en el modelo antes de usarlo para entregar H, perfiles, flechas y q_max
```

## 5. Orden completo de solucion

### Fase 1 - Revisar enunciado, correcciones y decisiones

Objetivo: separar datos reales de supuestos.

Acciones:

- Revisar `TareaReo#3GB.pdf`.
- Revisar correccion del docente.
- Confirmar que gobierna `L/800` y `S/800`, no `L/240` ni `S/240`.
- Confirmar que la forma exterior del puente se conserva.
- Confirmar que solo cambia la cercha interna segun tipologia Parker.
- Registrar que `H` es variable de diseno.

Salida esperada:

```text
ENTREGA FINAL/00_criterios/decisiones_actualizadas.md
ENTREGA FINAL/00_criterios/revision_pdf_y_correcciones.md
ENTREGA FINAL/00_criterios/agente_supervisor_reto3.md
```

Estado actual: realizado, pero debe seguirse usando como filtro antes de cada
calculo.

### Fase 2 - Seleccion aleatoria reproducible

Objetivo: obtener `L`, `S` y tipologia sin escoger a mano.

Acciones:

- Usar semilla `RETO3_ANALISIS_OSCAR_2026`.
- Ejecutar seleccion aleatoria.
- Guardar resultado en `json` y `md`.

Resultado vigente:

```text
L = 90 m
S = 28 m
tipologia = Parker
longitud total = 146 m
```

Salida esperada:

```text
ENTREGA FINAL/01_seleccion/seleccion_aleatoria.json
ENTREGA FINAL/01_seleccion/seleccion_aleatoria.md
ENTREGA FINAL/01_seleccion/seleccion_modelo_base_reto.json
```

Estado actual: realizado.

### Fase 3 - Definir variables geometricas antes de calcular

Objetivo: dejar claro que no se va a inventar `H`.

Acciones:

- Definir `H` como variable candidata, no definitiva.
- Definir un rango inicial de alturas razonables.
- Para cada `H`, calcular geometria exterior compatible con la guia.
- Calcular radios `R` y `r` como arcos de circunferencia.

Rango inicial propuesto para estudiar:

```text
H = 6, 7, 8, 9, 10, 11, 12 m
```

Este rango no significa que alguna altura ya sea correcta. Solo sirve para
explorar rigidez, flecha, fuerzas y peso.

Formula de radio para cada arco:

```text
R = c^2/(8f) + f/2
```

donde:

```text
c = cuerda horizontal del arco
f = flecha geometrica del arco, no deflexion estructural
```

Nota importante: aqui la palabra flecha puede crear confusion. En geometria de
arcos, `f` es la sagita del arco. En estructura, `delta_max` es la deflexion
vertical bajo carga. En el informe se debe escribir "sagita geometrica" para el
arco y "deflexion vertical" para el desplazamiento.

Salida esperada:

```text
ENTREGA FINAL/02_codigo/reto3_modular/geometria.py
ENTREGA FINAL/02_codigo/reto3_modular/geometria_candidata.py
ENTREGA FINAL/03_memoria_y_resultados/estado_h_pendiente.md
```

Estado actual: base programada, `H` sigue pendiente.

### Fase 4 - Construir geometria candidata por cada H

Objetivo: generar nodos del puente para cada altura candidata.

Acciones:

- Crear nodos del cordon superior.
- Crear nodos del cordon inferior.
- Ubicar apoyos.
- Mantener la forma exterior de la guia.
- Guardar coordenadas con unidades en m.
- Marcar cada geometria como `H provisional`.

Para cada candidato se debe registrar:

```text
H [m]
R [m]
r [m]
numero de nodos
coordenadas principales
estado = provisional
```

No se permite:

- llamar final una geometria que solo es candidata,
- tomar `H` de la imagen,
- ajustar `H` por estetica.

Salida esperada:

```text
tablas de nodos candidatas
figuras conceptuales marcadas como preliminares
```

Estado actual: base programada, falta usarla dentro del ciclo estructural.

### Fase 5 - Construir conectividad Parker

Objetivo: pasar de puntos a cercha estructural.

Acciones:

- Conectar cordon superior.
- Conectar cordon inferior.
- Conectar montantes.
- Conectar diagonales Parker.
- Revisar que no haya barras duplicadas.
- Revisar que la tipologia sea consistente con Parker.

Familias de barras:

```text
cuerda_superior
cuerda_inferior
montantes
diagonales_parker
```

Para cada barra se debe guardar:

```text
id
nodo_i
nodo_j
familia
longitud [m]
angulo [deg]
estado
```

Salida esperada:

```text
ENTREGA FINAL/02_codigo/reto3_modular/conectividad_parker.py
tablas de elementos para revision
figura de conectividad
```

Estado actual: base programada.

### Fase 6 - Preparar catalogo AISC y secciones candidatas

Objetivo: que las barras tengan propiedades reales, no areas inventadas.

Acciones:

- Usar el catalogo AISC disponible.
- Trabajar con HSS rectangular ASTM A1085/A1085M por decision del equipo.
- Crear tabla reducida de secciones.
- Registrar pagina o fuente de cada seccion.
- Asignar secciones iniciales por familia.

Propiedades necesarias:

```text
nombre de seccion
A [m2 o mm2]
peso [kg/m o kN/m]
Ix, Iy
rx, ry
espesor
pagina/fuente
```

Asignacion inicial propuesta:

```text
cordones: secciones mayores
diagonales: secciones intermedias
montantes: secciones menores o intermedias
```

Esto no es definitivo. Se ajusta si fallan deflexion, resistencia o pandeo.

Salida esperada:

```text
ENTREGA FINAL/03_memoria_y_resultados/secciones_aisc_hss_rectangular.csv
ENTREGA FINAL/02_codigo/reto3_modular/catalogo_aisc.py
```

Estado actual: tabla inicial creada; falta definir regla formal de seleccion.

### Fase 7 - Armar modelo estructural 2D

Objetivo: convertir la cercha en un modelo calculable.

Hipotesis de modelo:

```text
cercha plana 2D
barras axiales
nodos articulados
rigidez axial EA/L
desplazamientos ux, uy por nodo
```

Acciones:

- Crear grados de libertad por nodo.
- Calcular longitud y cosenos directores de cada barra.
- Armar rigidez local axial.
- Transformar a coordenadas globales.
- Ensamblar matriz global `K`.
- Aplicar apoyos.
- Aplicar cargas nodales equivalentes.
- Resolver desplazamientos.
- Calcular reacciones.
- Calcular fuerzas axiales.

Ecuacion base:

```text
K * u = F
```

Salida por corrida:

```text
desplazamientos nodales ux, uy [m]
deflexiones verticales uy [mm]
reacciones [kN]
fuerzas axiales N [kN]
estado de estabilidad del modelo
```

Control minimo:

- La matriz debe ser estable despues de aplicar apoyos.
- Las reacciones deben equilibrar las cargas.
- No debe haber mecanismo.
- Los desplazamientos deben tener signo y unidad.

Estado actual: pendiente de implementar completamente.

### Fase 8 - Definir cargas

Objetivo: aplicar cargas de forma trazable.

Tipos de carga:

```text
peso propio de secciones, si se aprueba incluirlo
camion CC14 / CCP-14
convoy con mayor numero simultaneo de camiones
carga unitaria movil para lineas de influencia
carga uniforme movil de 5 m
```

Acciones:

- Documentar cargas del camion.
- Convertir posiciones de ruedas/ejes a coordenadas sobre tablero.
- Pasar cargas puntuales a nodos del tablero.
- Barrer posiciones del camion a lo largo de 146 m.
- Identificar posicion critica por deflexion y por fuerza axial.

Pendiente clave:

```text
confirmar si se incluye peso propio
confirmar separacion y numero simultaneo de camiones
confirmar criterio final para q_max
```

Salida esperada:

```text
tabla de cargas por posicion
tabla de posicion critica
figura de camion critico
```

Estado actual: camion documentado; falta motor de carga movil.

### Fase 9 - Disenar H por iteracion

Objetivo: encontrar una altura `H` que cumpla deflexion y sea defendible.

Esta fase es central. No se puede omitir.

Para cada `H` candidata:

```text
1. construir geometria
2. calcular R y r
3. construir conectividad Parker
4. asignar secciones candidatas
5. armar modelo 2D
6. aplicar cargas moviles de camion
7. hallar delta_max,L y delta_max,S
8. comparar contra L/800 y S/800
9. calcular fuerzas axiales N
10. revisar secciones y pandeo basico
11. calcular peso aproximado
12. guardar resultado de la corrida
```

Variables de salida por candidato:

```text
H [m]
R [m]
r [m]
secciones usadas
peso estimado [kN o kg]
delta_max,L [mm]
delta_adm,L = 112.5 mm
ratio_L = delta_max,L / delta_adm,L
delta_max,S [mm]
delta_adm,S = 35.0 mm
ratio_S = delta_max,S / delta_adm,S
N_max_tension [kN]
N_max_compresion [kN]
barra critica
posicion critica del camion
cumple_deflexion = si/no
cumple_resistencia = si/no
estado
```

Criterio de aceptacion:

```text
delta_max,L <= 112.5 mm
delta_max,S <= 35.0 mm
secciones disponibles en catalogo
fuerzas axiales dentro de capacidad preliminar
sin barras evidentemente inestables por pandeo
geometria coherente con la guia
```

Seleccion de `H`:

```text
Se elige la menor H que cumpla deflexion y resistencia con margen razonable,
sin producir barras demasiado largas/esbeltas ni un peso absurdo.
```

Si ninguna `H` cumple:

```text
1. aumentar H dentro de un rango razonable
2. aumentar secciones de cordones
3. aumentar secciones de diagonales/montantes criticos
4. revisar modelo de cargas
5. reportar bloqueo si el criterio no es alcanzable
```

Tabla obligatoria en la memoria:

| H [m] | delta_max,L [mm] | L/800 [mm] | ratio L | delta_max,S [mm] | S/800 [mm] | ratio S | secciones | cumple |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 6 | pendiente | 112.5 | pendiente | pendiente | 35.0 | pendiente | pendiente | pendiente |
| 7 | pendiente | 112.5 | pendiente | pendiente | 35.0 | pendiente | pendiente | pendiente |
| 8 | pendiente | 112.5 | pendiente | pendiente | 35.0 | pendiente | pendiente | pendiente |
| 9 | pendiente | 112.5 | pendiente | pendiente | 35.0 | pendiente | pendiente | pendiente |
| 10 | pendiente | 112.5 | pendiente | pendiente | 35.0 | pendiente | pendiente | pendiente |
| 11 | pendiente | 112.5 | pendiente | pendiente | 35.0 | pendiente | pendiente | pendiente |
| 12 | pendiente | 112.5 | pendiente | pendiente | 35.0 | pendiente | pendiente | pendiente |

Estado actual: pendiente. Esta fase debe aprobarse antes de correr iteraciones
numericas completas.

### Fase 10 - Verificar resistencia axial y pandeo preliminar

Objetivo: no aceptar una cercha solo porque cumple flecha.

Acciones:

- Tomar fuerzas axiales maximas por barra.
- Separar tension y compresion.
- Revisar capacidad axial de secciones.
- Revisar esbeltez de barras comprimidas.
- Identificar barras criticas.

Variables:

```text
N_t [kN]
N_c [kN]
A [m2]
L_barra [m]
rx, ry
KL/r
capacidad preliminar
ratio demanda/capacidad
```

Importante:

```text
La deflexion controla servicio.
La resistencia controla seguridad.
Ambas deben revisarse.
```

Estado actual: pendiente de programacion y criterios.

### Fase 11 - Lineas de influencia

Objetivo: cumplir el requisito del PDF y validar el comportamiento movil.

Acciones:

- Seleccionar una respuesta critica: fuerza en barra critica, reaccion o
  deflexion.
- Mover una carga unitaria de `1 kN` sobre el tablero.
- Registrar respuesta por posicion.
- Graficar linea de influencia.
- Validar que la forma tenga sentido fisico.

Salida esperada:

```text
posicion x [m]
respuesta por carga unitaria
grafica de LI
barra o respuesta analizada
validacion con carga movil
```

Estado actual: pendiente en modelo final.

### Fase 12 - Carga uniforme movil maxima de 5 m

Objetivo: hallar la carga uniforme movil maxima pedida por el reto.

Acciones:

- Definir una carga distribuida movil de longitud `5 m`.
- Convertirla a cargas nodales equivalentes.
- Barrerla sobre la longitud del puente.
- Para cada posicion, revisar deflexion y fuerzas.
- Incrementar `q` hasta llegar al limite que gobierne.

Variables:

```text
q [kN/m]
longitud cargada = 5 m
W = q * 5 m
delta_max [mm]
N_max [kN]
posicion critica x [m]
modo que gobierna: deflexion o resistencia
```

Salida esperada:

```text
q_max [kN/m]
W_max [kN]
posicion critica
criterio que controla
tabla o grafica de barrido
```

Estado actual: pendiente, depende de tener `H` y secciones finales.

### Fase 13 - Verificacion independiente

Objetivo: no confiar ciegamente en el script principal.

Acciones:

- Revisar equilibrio de reacciones.
- Comparar una corrida simple con calculo manual o Ftool.
- Revisar signos de fuerzas axiales.
- Revisar que la deformada tenga sentido.
- Revisar que la posicion critica del camion sea razonable.
- Revisar que el resultado no dependa de un error de unidades.

Chequeos minimos:

```text
suma de cargas verticales ~= suma de reacciones verticales
unidades de E, A, L coherentes
delta en m convertido a mm correctamente
sin apoyos redundantes o mecanismo
sin barras de longitud cero
```

Estado actual: pendiente.

### Fase 14 - Documentacion final

Objetivo: preparar una entrega compacta, defendible y sin humo.

El informe final debe incluir:

- datos del problema,
- decisiones vigentes,
- geometria final,
- valor final de `H`,
- radios `R` y `r`,
- secciones AISC usadas,
- tabla de iteracion de `H`,
- verificacion de deflexion,
- fuerzas criticas,
- carga uniforme movil maxima de 5 m,
- linea de influencia validada,
- limitaciones y supuestos aprobados.

Formato recomendado:

```text
maximo 5 paginas
tablas compactas
figuras con estado: definitiva o conceptual
unidades en todos los resultados
```

Estado actual: pendiente de resultados finales.

## 6. Flujo de trabajo resumido

```text
leer fuentes
seleccionar L, S y Parker
definir rango de H
para cada H:
    generar geometria
    calcular R y r
    construir conectividad
    asignar secciones
    armar rigidez
    aplicar camiones
    calcular delta_max
    comparar con L/800 y S/800
    revisar fuerzas y pandeo
elegir H final
calcular linea de influencia
calcular q_max de carga uniforme movil de 5 m
verificar independiente
documentar entrega final
```

## 7. Archivos vigentes del proceso

```text
ENTREGA FINAL/00_criterios/
ENTREGA FINAL/01_seleccion/
ENTREGA FINAL/02_codigo/reto3_modular/
ENTREGA FINAL/03_memoria_y_resultados/
```

Archivos locales que no son entrega final:

```text
00_enunciado/
01_datos/
05_figuras/
06_documentos/
07_verificacion_ftool/
08_archivo_preliminar/
tmp/
scripts/
```

Esos archivos pueden servir como respaldo local, pero no deben mezclarse con la
entrega final sin revision.

## 8. Pendientes que requieren aprobacion o confirmacion

1. Aprobar el rango inicial de `H = 6 m` a `12 m`, o modificarlo.
2. Confirmar si se incluye peso propio en las verificaciones.
3. Confirmar criterio exacto para mayor numero simultaneo de camiones.
4. Confirmar que el camion `CC14 / CCP-14` es aceptado definitivamente.
5. Confirmar uso de HSS rectangular AISC como reemplazo practico del tubular
   cuadrado mencionado en el enunciado.
6. Confirmar si `q_max` de 5 m debe limitarse por deflexion, resistencia o ambas.
7. Confirmar si el modelo 2D axial de cercha es suficiente para el alcance.

## 9. Estado actual real

El proyecto tiene una base de seleccion, geometria candidata, conectividad
Parker, catalogo inicial y documentacion de criterios. Todavia no existe:

```text
H final
delta_max final
secciones finales verificadas
q_max final
linea de influencia final
verificacion independiente final
```

Por tanto, cualquier `H` vista hasta ahora debe tratarse como provisional. La
proxima fase correcta es aprobar el procedimiento de iteracion de `H` y ejecutar
las corridas estructurales completas controlando explicitamente la flecha
`delta_max`.
