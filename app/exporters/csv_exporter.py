import csv

def conversion_csv(resultado, ruta, config, callback=None):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([col.title for col in config.columns])
        for mov in resultado.movimientos:
            row = [getattr(mov, col.source, "") for col in config.columns]
            writer.writerow(row)
    if callback:
        callback(f"Archivo CSV exportado: {ruta}")
