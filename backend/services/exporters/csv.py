import csv


def exportar_csv(resultado, ruta):
    columnas = [
        "Fecha",
        "Descripción",
        "Detalle",
        "Débito",
        "Crédito",
        "Saldo",
    ]

    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
        writer = csv.writer(archivo)

        writer.writerow(columnas)

        for movimiento in resultado.movimientos:
            fila = [
                movimiento.fecha,
                movimiento.descripcion,
                movimiento.detalle,
                movimiento.debito,
                movimiento.credito,
                movimiento.saldo,
            ]

            writer.writerow(fila)