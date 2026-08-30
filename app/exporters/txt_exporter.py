def conversion_txt(resultado, ruta, config, callback=None):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\t".join([col.title for col in config.columns]) + "\n")
        for mov in resultado.movimientos:
            row = [str(getattr(mov, col.source, "")) for col in config.columns]
            f.write("\t".join(row) + "\n")
    if callback:
        callback(f"Archivo TXT exportado: {ruta}")
