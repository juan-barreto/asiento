from openpyxl import Workbook
import os


def conversion_excel(resultado, callback=None):

    def log(mensaje):
        if callback:
            callback(mensaje)
        else:
            print(mensaje)

    wb = Workbook()

    ws = wb.active
    ws.title = "Movimientos"

    # Encabezados
    ws.append([
        "Fecha",
        "Descripción",
        "Detalle",
        "Crédito",
        "Débito",
        "Saldo",
        "Confidence"
    ])

    # Movimientos
    for movimiento in resultado.movimientos:
        ws.append([
            movimiento.fecha,
            movimiento.descripcion,
            movimiento.detalle,
            movimiento.credito,
            movimiento.debito,
            movimiento.saldo,
            movimiento.confidence
        ])

    # Ajuste automático
    for columna in ws.columns:
        length = max(len(str(cell.value)) for cell in columna)
        ws.column_dimensions[columna[0].column_letter].width = length + 2

    ruta = "extracto_pyside.xlsx"

    wb.save(ruta)

    log(f"Excel guardado en: {ruta}")

    try:
        os.startfile(ruta)
        log("Excel abierto correctamente.")
    except OSError as e:
        log(f"No se pudo abrir automáticamente el archivo: {e}")