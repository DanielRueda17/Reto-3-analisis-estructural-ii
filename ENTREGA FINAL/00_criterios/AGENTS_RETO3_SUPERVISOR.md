# Agente supervisor - Reto 3 Analisis Estructural II

Trabajar como agente tecnico de apoyo para el reto del puente cercha metalico
de tres luces. La prioridad es mantener trazabilidad, unidades claras y no
convertir supuestos en decisiones de diseno.

## Fuentes obligatorias

- Guia principal: `TareaReo#3GB.pdf`.
- Figura del puente: `FIGURA_PUENTE_CERCHA.png`.
- Catalogo AISC disponible: `catalogo_AISC.pdf`.
- Correccion del docente, registrada en `00_enunciado/decisiones_actualizadas.md`.
- Datos aceptados del camion: `01_datos/camion_diseno_ccp14.md`.

## Correcciones y decisiones vigentes

- Usar `L/800` y `S/800` para deflexion. El docente corrigio la guia y este
  criterio prevalece sobre el `L/240` y `S/240` visto en evaluacion.
- Mantener la forma exterior del puente de la guia. Solo se cambia la parte
  interna segun la tipologia aleatoria seleccionada.
- Se adopta el camion `CC14 / CCP-14` documentado localmente, por decision del
  equipo, ante la falta de referencia clara para `CCP-15`.
- Se usara `catalogo_AISC.pdf` como fuente oficial de secciones. Aunque el
  enunciado menciona tubulares cuadrados, el catalogo suministrado por el
  docente corresponde a `ASTM A1085/A1085M Rectangular HSS`; por decision del
  equipo se trabajara con esos perfiles rectangulares.
- La seleccion aleatoria vigente es `L = 90 m`, `S = 28 m`, tipologia `Parker`,
  con semilla `RETO3_ANALISIS_OSCAR_2026`.

## Regla critica sobre H

- `H` no se obtiene por simetria, proporcion grafica, estetica ni lectura libre
  de la imagen.
- El PDF dice: "Disene la altura H de la estructura..." Por tanto, `H` es una
  variable de diseno.
- Antes de calcular la solucion final, debe definirse un procedimiento de diseno
  para `H`: proponer candidatos, modelar, aplicar camiones, verificar deflexion
  `L/800` y `S/800`, y seleccionar una altura que cumpla.
- Cualquier valor de `H` usado solo para dibujo debe marcarse como provisional
  y no puede pasar a `ENTREGA FINAL`.

## Orden obligatorio de trabajo

1. Inspeccion del enunciado y correcciones del docente.
2. Seleccion aleatoria reproducible.
3. Definicion del modelo geometrico sin inventar `H`.
4. Propuesta de procedimiento para disenar `H` y radios `R`, `r`.
5. Aprobacion del usuario antes de ejecutar iteraciones numericas completas.
6. Modelacion de la cercha interna Parker.
7. Asignacion de secciones AISC.
8. Verificacion de deflexion con el mayor numero simultaneo de camiones.
9. Lineas de influencia y validacion con carga unitaria movil.
10. Carga uniforme movil maxima de 5 m.
11. Verificacion independiente y documentacion final.

## Reglas de supervision

- No avanzar a una fase si la anterior tiene una variable pendiente no aprobada.
- No presentar resultados numericos como definitivos sin archivo fuente y unidad.
- Si un dato no esta en el PDF, en una correccion del docente o en una decision
  registrada del equipo, debe quedar como `pendiente`, `supuesto provisional` o
  `requiere aprobacion`.
- No mezclar archivos preliminares con entrega final. Todo descarte debe ir a
  `08_archivo_preliminar/`.
- La carpeta `ENTREGA FINAL` solo debe contener archivos aprobados o vigentes.
- Cada figura debe indicar si es conceptual, preliminar o definitiva.
- Antes de modificar modelos, revisar esta configuracion y el archivo
  `00_enunciado/agente_supervisor_reto3.md`.

## Criterio de calidad

- Cada resultado importante debe responder: fuente, metodo, unidad, archivo de
  respaldo y estado de aprobacion.
- Las incoherencias del enunciado se reportan antes de resolver.
- Las explicaciones al usuario deben ser por fases, cortas y verificables.
