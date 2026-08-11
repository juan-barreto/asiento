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
 
                    
  
        
    """     
 
    
    # PASO 4: Separar por confidence
    seguros = [m for m in movimientos_limpios if m.get("confidence", 0) >= 0.7]
    revisar = [m for m in movimientos_limpios if m.get("confidence", 0) < 0.7]
    
    # Mostrar resumen
    log("\n" + "="*50)
    log("RESUMEN FINAL")
    log("="*50)
    log(f"Movimientos confiables (≥70%): {len(seguros)}")
    log(f"Requieren revisión (<70%):   {len(revisar)}")
    log(f"Descartados:                   {len(movimientos_crudos) - len(movimientos_limpios)}")
    log("="*50 + "\n")
    
    return {
        "todos": movimientos_limpios,
        "seguros": seguros,
        "revisar": revisar,
        "stats": {
            "total_crudos": len(movimientos_crudos),
            "total_validos": len(movimientos_limpios),
            "total_seguros": len(seguros),
            "total_revisar": len(revisar),
            "tasa_exito": len(movimientos_limpios) / len(movimientos_crudos) if movimientos_crudos else 0
        }
    }


def guardar_resultados(resultado, output_dir=".",callback=None):
   
    def log(mensaje):
        if callback:
            callback(mensaje)
        else:
            print(mensaje)

    import os
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar todos
    with open(f"{output_dir}/movimientos_todos.json", "w", encoding="utf-8") as f:
        json.dump(resultado["todos"], f, indent=2, ensure_ascii=False)
    
    # Guardar seguros
    with open(f"{output_dir}/movimientos_seguros.json", "w", encoding="utf-8") as f:
        json.dump(resultado["seguros"], f, indent=2, ensure_ascii=False)
    
    # Guardar para revisar
    with open(f"{output_dir}/movimientos_revisar.json", "w", encoding="utf-8") as f:
        json.dump(resultado["revisar"], f, indent=2, ensure_ascii=False)
    
    # Guardar stats
    with open(f"{output_dir}/stats.json", "w", encoding="utf-8") as f:
        json.dump(resultado["stats"], f, indent=2, ensure_ascii=False)
    
    log("Archivos guardados:")
    log(f"  - {output_dir}/movimientos_todos.json")
    log(f"  - {output_dir}/movimientos_seguros.json")
    log(f"  - {output_dir}/movimientos_revisar.json")
    log(f"  - {output_dir}/stats.json")

"""
# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    # Ruta al PDF
    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    
    # Procesar
    resultado = procesar_extracto(pdf_path)
    print()
    
    