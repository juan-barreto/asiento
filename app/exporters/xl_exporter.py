from openpyxl import Workbook
import os


def conversion_excel(resultado, ruta, config, callback=None):

    def log(mensaje):
        if callback:
            callback(mensaje)
        else:
            print(mensaje)

    wb = Workbook()

    ws = wb.active
    ws.title = "Movimientos"

    columnas_activas = [
        column
        for column in config.columns
        if column.enabled
    ]

    ws.append([
        column.title
        for column in columnas_activas
    ])

    for movimiento in resultado.movimientos:

        fila = []

        for column in columnas_activas:

            valor = getattr(
                movimiento,
                column.source,
                ""
            )

            fila.append(valor)

        ws.append(fila)

    for columna in ws.columns:

        length = max(
            len(str(cell.value))
            for cell in columna
        )

        ws.column_dimensions[
            columna[0].column_letter
        ].width = length + 2

    wb.save(ruta)

    log(f"Excel guardado en: {ruta}")

    try:

        os.startfile(ruta)

        log("Excel abierto correctamente.")

    except OSError as e:

        log(
            f"No se pudo abrir automáticamente "
            f"el archivo: {e}"
        )