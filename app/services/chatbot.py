import os
import re
import json
from groq import Groq
from dotenv import load_dotenv
from pdf_processor import extraccion_texto_por_pagina
from pre_processor import extraer_bloques_movimientos
import time

# Config

load_dotenv()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

# Normalizacion texto PDF

"""def normalize_text(text):
    "
    Esta funcion convierte el texto vertical en un texto mas lineal.

    "
    # Elimina múltiples saltos de linea generados
    
    text = re.sub(r"\n+", "\n", text) 
    
    # Une lineas cortadas (saltos de linea seguidos en el texto)
    text = re.sub(r"\n(?=\S)", " ", text)
    return text.strip()"""

# Limpieza json con IA

def clean_json_response(contenido):
    """
    Esta funcion extrae JSON de la respuesta 

    """
    match = re.search(r"\[.*\]", contenido, re.DOTALL)
    if match:
        return match.group(0).strip()
    
    contenido = contenido.strip()
    if contenido.startswith("[") and not contenido.endswith("]"):
        contenido += "]"
    return contenido


# Le da formato a la IA para un unico formato

def parse_block_with_ai(block_text, callback=None):

    def log(mensaje):
        if callback:
            callback(mensaje)
        else:
            print(mensaje)

    prompt = f"""
Convertí este movimiento bancario a JSON válido.

REGLAS IMPORTANTES:
- responder SOLO JSON
- NO expliques nada
- NO hagas cálculos matemáticos
- saldo debe ser un número literal
- NO usar expresiones como 10-5
- debito y credito nunca juntos
- si un valor no existe usar 0.0
- usar punto decimal
- JSON compatible con json.loads()

FORMATO:
[
  {{
    "fecha": "",
    "descripcion": "",
    "detalle": "",
    "debito": 0.0,
    "credito": 0.0,
    "saldo": 0.0
  }}
]

MOVIMIENTO:
{block_text}
"""

    try:

        res = client.chat.completions.create(

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sos un extractor de movimientos bancarios. "
                        "Respondé únicamente JSON válido."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            model="llama-3.1-8b-instant",

            temperature=0
        )

        content = res.choices[0].message.content

        content = clean_json_response(content)

        movimientos = json.loads(content)

        return movimientos

    except Exception as e:

        log("\n❌ Error procesando bloque")

        log(f"Bloque:\n{block_text}")

        log(f"\nRespuesta IA:\n{content if 'content' in locals() else 'Sin respuesta'}")

        log(f"\nError:\n{e}")

        return []
    
    # Proceso completo
        """
        Esta funcion procesa todas las bloques del PDF y devuelve los movimientos crudos que no estan validados.

        """
def parse_all_blocks(blocks, callback=None):

    def log(mensaje):
        if callback:
            callback(mensaje)
        else:
            print(mensaje)

    all_results = []

    for n, block in enumerate(blocks, start=1):

        log(f"\n📄 Procesando bloque {n}/{len(blocks)}")

        movimientos = parse_block_with_ai(
            block,
            callback
        )

        all_results.extend(movimientos)

        log(f"✅ Movimiento extraído: {len(movimientos)}")

        time.sleep(1)

    return all_results

    
    

if __name__ == "__main__":
    # Prueba
    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    texto = extraccion_texto_por_pagina(pdf_path)
  

    for t in texto:
        limpio = extraer_bloques_movimientos(t["text"])

        resultado = parse_all_blocks(limpio)
        
    print(json.dumps(resultado, indent=2, ensure_ascii=False))  

    

