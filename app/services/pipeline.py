import json
from app.services.pdf_processor import extraccion_texto_por_pagina
from app.services.parsers.galicia_parser import extraer_bloques_galicia
from app.services.parsers.provincia_parser import extraer_bloques_provincia
from app.services.parsers.detector import Galicia, Provincia
from app.services.movimiento import ResultadoPipeline, StatsPipeline
from app.services.validator import validar_movimientos

def procesar_extracto(pdf_path, callback=None):
    """
    Pipeline completo: PDF -> Validación → JSON limpio
    """
    def log(mensaje):
        if callback:
            callback(mensaje)
        else:
            print(mensaje)

    log("\nINICIANDO PROCESAMIENTO\n")
    
    # PASO 1: Extraer texto del PDF
    log("Extrayendo texto del PDF...")
    pages_data = extraccion_texto_por_pagina(pdf_path)
    log(f"   ✓ {len(pages_data)} páginas extraídas\n")

    BANCOS = [
          Galicia,
          Provincia
    ]
    movimientos = []
    banco_detectado = None

    for banco in BANCOS:
        

        if banco.detectar(pages_data):
            banco_detectado = banco
            movimientos = []

            for pagina in pages_data:
                movimientos.extend(
                    banco.parser(pagina["text"])
                )

            break

    if banco_detectado is None:
        raise ValueError("No se detectó un banco compatible.")
    
    resultado = validar_movimientos(movimientos)
    
    log(
            json.dumps(
                [m.model_dump(mode="json") for m in resultado],
                indent=2,
                ensure_ascii=False
                )
                )
    seguros = [m for m in resultado if m.confidence >= 0.7]
    revisar = [m for m in resultado if m.confidence < 0.7]

    resultado_pipeline = ResultadoPipeline(
    banco=banco_detectado.nombre,
    movimientos=resultado,
    seguros=seguros,
    revisar=revisar,
    stats=StatsPipeline(
        total_movimientos=len(resultado),
        total_seguros=len(seguros),
        total_revisar=len(revisar)
    )
)

    return resultado_pipeline
 
                    
  
   
if __name__ == "__main__":
    # Ruta al PDF
    #pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\5010613125_20260601_extractos.pdf"
    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\2026-08-20_00720048002000598381.pdf"
    # Procesar
    resultado = procesar_extracto(pdf_path)
    print()
    
    