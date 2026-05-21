# Camion de diseno - referencia CCP-14

## Estado de verificacion

Se busco referencia web para el "camion de diseno CCP-15" indicado en la guia del reto. No se encontro una fuente normativa clara con nombre `CCP-15`. La referencia verificable encontrada corresponde a la Norma Colombiana de Diseno de Puentes `CCP-14` de INVIAS/AIS y al camion de diseno `CC14`.

Para el trabajo se adopta el camion de diseno `CC14` de la norma `CCP-14`, por decision de trabajo del equipo despues de revisar que no se encontro una referencia tecnica clara para `CCP-15`.

## Fuente primaria localizada

- INVÍAS, pagina oficial: Norma Colombiana de Diseno de Puentes CCP14.
- URL: https://www.invias.gov.co/index.php/archivo-y-documentos/documentos-tecnicos/3709-norma-colombiana-de-diseno-de-puentes-ccp14
- La pagina indica descarga de `norma_colombiana_de_diseno_de_puentes_ccp14.zip`.
- En esta sesion la descarga directa desde el portal devolvio error 404, por lo que se uso una fuente tecnica secundaria para capturar la figura.

## Fuente secundaria usada para la captura

- Archivo descargado: `01_datos/anexo_diseno_estructural_puente_unipiloto.pdf`.
- URL de descarga: https://repository.unipiloto.edu.co/bitstream/handle/20.500.12277/10569/Anexo%201%20-%20Dise%C3%B1o%20estructural%20del%20puente.pdf?sequence=2
- Pagina revisada: pagina 13 del PDF.
- La pagina reproduce la `Figura 3.6.1.2.2-1 - Caracteristicas del Camion de Diseno, fuente CCP-14`.

## Datos extraidos para el modelo

- Camion de diseno con tres ejes.
- Eje delantero: `40 kN`.
- Primer eje trasero: `160 kN`.
- Segundo eje trasero: `160 kN`.
- Separacion entre eje delantero y primer eje trasero: `4300 mm` = `4.30 m`.
- Separacion entre los dos ejes de `160 kN`: variable entre `4300 mm` y `9000 mm` = `4.30 m` a `9.00 m`, para producir solicitaciones extremas.
- Separacion transversal de ruedas: `1800 mm` = `1.80 m`.
- Carril de diseno: `3600 mm` = `3.60 m`.
- Distancia transversal indicada en la figura: `600 mm` general y `300 mm` para vuelo sobre el tablero.

## Archivos guardados

- Captura recortada del camion: `05_figuras/referencias/ss_camion_diseno_ccp14_fig_3_6_1_2_2_1.png`.
- Pagina fuente renderizada: `05_figuras/referencias/pagina_fuente_camion_ccp14.png`.
- PDF fuente secundaria: `01_datos/anexo_diseno_estructural_puente_unipiloto.pdf`.

## Notas para calculo posterior

- Para la etapa de deflexion se debe decidir la posicion longitudinal de cada camion y el numero simultaneo de camiones que caben sobre el puente.
- El espaciamiento variable de `4.30 m` a `9.00 m` entre ejes traseros debe revisarse contra el efecto buscado: deflexion maxima, fuerza axial maxima o respuesta por linea de influencia.
- Debe confirmarse si se aplica amplificacion dinamica al camion para este reto. La guia no lo menciona explicitamente, pero la referencia CCP-14 si asocia el camion de diseno con asignacion de carga dinamica.
