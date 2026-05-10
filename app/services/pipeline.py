import json
from app.services.pdf_processor import extraccion_texto_por_pagina
from app.services.chatbot import parse_all_pages
from app.services.validator import validar_movimientos

def procesar_extracto(pdf_path):
    """
    Pipeline completo: PDF → IA → Validación → JSON limpio
    """
    print("\nINICIANDO PROCESAMIENTO\n")
    
    # PASO 1: Extraer texto del PDF
    print("Extrayendo texto del PDF...")
    pages_data = extraccion_texto_por_pagina(pdf_path)
    print(f"   ✓ {len(pages_data)} páginas extraídas\n")
    
    # PASO 2: Procesar con IA
    print("🤖 Enviando a IA...")
    movimientos_crudos = parse_all_pages(pages_data)
    print(f"\n   ✓ Total movimientos crudos: {len(movimientos_crudos)}\n")
    
    # PASO 3: Validar y limpiar
    print("✅ Validando movimientos...")
    movimientos_limpios = validar_movimientos(movimientos_crudos)
    print(f"   ✓ Movimientos válidos: {len(movimientos_limpios)}\n")
    
    # PASO 4: Separar por confidence
    seguros = [m for m in movimientos_limpios if m.get("confidence", 0) >= 0.7]
    revisar = [m for m in movimientos_limpios if m.get("confidence", 0) < 0.7]
    
    # Mostrar resumen
    print("\n" + "="*50)
    print("RESUMEN FINAL")
    print("="*50)
    print(f"Movimientos confiables (≥70%): {len(seguros)}")
    print(f"Requieren revisión (<70%):   {len(revisar)}")
    print(f"Descartados:                   {len(movimientos_crudos) - len(movimientos_limpios)}")
    print("="*50 + "\n")
    
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


def guardar_resultados(resultado, output_dir="."):
    """
    Guarda los resultados en archivos JSON.
    """
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
    
    print("Archivos guardados:")
    print(f"  - {output_dir}/movimientos_todos.json")
    print(f"  - {output_dir}/movimientos_seguros.json")
    print(f"  - {output_dir}/movimientos_revisar.json")
    print(f"  - {output_dir}/stats.json")


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    # Ruta al PDF
    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    
    # Procesar
    resultado = procesar_extracto(pdf_path)
    
    # Guardar
    guardar_resultados(resultado, output_dir="resultados")
    
    # Mostrar ejemplos
    if resultado["seguros"]:
        print("\nEJEMPLO SEGURO:")
        print(json.dumps(resultado["seguros"][0], indent=2, ensure_ascii=False))
    
    if resultado["revisar"]:
        print("\nEJEMPLO REVISAR:")
        print(json.dumps(resultado["revisar"][0], indent=2, ensure_ascii=False))
    
    # Mostrar stats
    print("\nESTADÍSTICAS:")
    print(f"  Tasa de éxito: {resultado['stats']['tasa_exito']:.1%}")