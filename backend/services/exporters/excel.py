from openpyxl import Workbook


def exportar_excel(resultado, ruta):
    wb = Workbook()
    ws = wb.active
    ws.title = "Movimientos"

    columnas = [
        "Fecha",
        "Descripción",
        "Detalle",
        "Débito",
        "Crédito",
        "Saldo",
    ]

    ws.append(columnas)

    for movimiento in resultado.movimientos:
        fila = [
            movimiento.fecha,
            movimiento.descripcion,
            movimiento.detalle,
            movimiento.debito,
            movimiento.credito,
            movimiento.saldo,
        ]

        ws.append(fila)

    for columna in ws.columns:
        ancho = max(len(str(celda.value or ""))
                    
            for celda in columna
        )
        ws.column_dimensions[
            columna[0].column_letter
        ].width = ancho + 2

    wb.save(ruta)

if __name__ == "__main__":

    from app.services.pipeline import procesar_extracto

    pdf = r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_02_27.pdf"
    resultado = procesar_extracto(pdf)
    rutar = r"C:\Users\Juan\Desktop\ASIENTO\app\services\pruebaparapi.xlsx"
    exportar_excel(resultado, rutar)