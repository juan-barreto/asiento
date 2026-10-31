def exportar_txt(resultado, ruta):
    columnas = [
        "Fecha",
        "Descripción",
        "Detalle",
        "Débito",
        "Crédito",
        "Saldo",
    ]

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\t".join(columnas) + "\n")

        for mov in resultado.movimientos:
            fila = [
                str(mov.fecha),
                str(mov.descripcion),
                str(mov.detalle),
                str(mov.debito),
                str(mov.credito),
                str(mov.saldo),
            ]

            archivo.write("\t".join(fila) + "\n")