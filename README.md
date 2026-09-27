# ASIENTO

ASIENTO es una aplicación de escritorio para procesar extractos bancarios en PDF y convertir sus movimientos en información estructurada y revisable.

El proyecto nació a partir de una necesidad concreta: facilitar el trabajo con extractos bancarios que llegan en distintos formatos, evitando tener que procesarlos manualmente uno por uno.

## Qué hace

El flujo principal de ASIENTO es:

1. Seleccionar un extracto bancario en PDF.
2. Extraer la información del documento.
3. Procesar y estructurar los movimientos.
4. Validar los datos obtenidos.
5. Revisar los resultados dentro de la aplicación.
6. Exportar la información procesada.

Los movimientos pueden quedar clasificados como datos seguros o como información que requiere revisión.

Actualmente el proyecto cuenta con soporte funcional para extractos de Banco Galicia y Banco Provincia.

## Tecnologías

* Python
* PySide6
* SQLite
* PyMuPDF
* Pydantic
* Exportación a Excel, CSV y TXT

## Arquitectura

El procesamiento está separado en distintas etapas para evitar mezclar la extracción del PDF con la lógica de procesamiento y la interfaz.

```text
PDF
 |
 v
Extracción
 |
 v
Procesamiento
 |
 v
Validación
 |
 v
Revisión
 |
 v
Exportación
```

La aplicación utiliza SQLite para almacenar el historial localmente.

El procesamiento está pensado con un enfoque local-first: los documentos no necesitan salir del equipo para realizar el procesamiento principal.

## Estado del proyecto

ASIENTO se encuentra en desarrollo.

La versión actual permite procesar extractos de Banco Galicia y Banco Provincia, revisar los movimientos detectados y exportar los resultados.

El siguiente desafío del proyecto es ampliar el soporte a otros bancos y mejorar la detección de estructuras de documentos diferentes.

## Por qué lo hice

ASIENTO es un proyecto de aprendizaje y, al mismo tiempo, una herramienta pensada para resolver un problema real.

Una parte importante del desarrollo consiste en analizar cómo están estructurados visualmente los PDFs antes de intentar interpretar sus datos. Esto permite trabajar con diferentes formatos de extractos sin depender únicamente de reglas específicas para cada banco.

El proyecto también me sirve para profundizar en desarrollo de aplicaciones de escritorio, procesamiento de documentos, validación de datos y diseño de software.

## Autor

Juan Manuel Barreto

Desarrollo de software | Python

Portfolio: https://juan-barreto-portfolio.vercel.app/

## Licencia

Proyecto privado. Todos los derechos reservados. El código se publica con fines demostrativos y de portfolio.
