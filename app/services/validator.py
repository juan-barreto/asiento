from datetime import datetime
import re
import json
from movimiento import MovimientoRaw, Movimiento
from pdf_processor import extraccion_texto_por_pagina
from pre_processor import extraer_bloques_movimientos

def validar_movimientos(movimientos):
    """
    Esta funcion valida, normaliza y asigna confidence(porcentaje de exito) a los movimientos
    
    """

    resultado = []

    for m in movimientos:

    # 1. Validacion de estructura basica

        if not validar_estructura(m):
            continue
        
    # 2. Normalizamos los datos

        m = normalizar_movimiento(m)

    # 3. Calcular el confidence

        m.confidence = calcular_confidence(m)


    # 4. Agregamos a la lista
        resultado.append(m)


    return resultado

def validar_estructura(m: Movimiento):
    """
    Esta funcion verifica que tenga los campos minimos

    """
    if not m.fecha:
        return False
    
    if not m.descripcion:
      return False

    if m.saldo is None:
        return False
    
    return True

   


def normalizar_movimiento(m: Movimiento):
    """
    Esta funcion normaliza las fechas, numeros y texto
    
    """

    # Normalizamos fecha:

    m.fecha = normalizar_fecha(m.fecha)

    m.debito = abs(m.debito)
    m.credito = abs(m.credito)
    m.saldo = abs(m.saldo)

    m.descripcion = m.descripcion.strip()
    m.detalle = m.detalle.strip()

    return m

def normalizar_fecha(fecha_str):
    """
    Esta funcion convierte cualquier formato en DD/MM/YYYY
    
    """

    # Establecemos los patrones con regex:

    patrones = [
        (r"(\d{2})/(\d{2})/(\d{4})", "{0}/{1}/{2}"),   # 03/11/2025
        (r"(\d{2})/(\d{2})/(\d{2})", "{0}/{1}/20{2}"), # 30/12/25
        (r"(\d{2})-(\d{2})-(\d{4})", "{0}/{1}/{2}"),   # 03-11-2026
        (r"(\d{2})-(\d{2})-(\d{2})", "{0}/{1}/20{2}"),
        (r"^(\d{2})-(\d{2})$", "{0}/{1}/20{2}"),
        ]
    
    for patron, formato in patrones:
        match = re.match(patron, fecha_str)
        if match:
            grupos = match.groups()
            return formato.format(*grupos)
    return None


def calcular_confidence(m):
    """
    Esta funcion nos da un indice de exito en la validacion de datos
    
    """
    score = 1.0

    if not m.descripcion:
        score -= 0.2

    if m.credito == 0 and m.debito == 0:
        score -= 0.5

    if m.credito > 0 and m.debito > 0:
        score -= 0.6

    if not m.fecha:
        score -= 0.4

    if m.saldo == 0:
        score -= 0.1

    return max(0.0, min(1.0, score))

if __name__ == "__main__":
  pdf_path =        r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"
  texto = extraccion_texto_por_pagina(pdf_path)
   
  movimientos = []

  for t in texto:

    movimientos.extend(
        extraer_bloques_movimientos(
            t["text"]
        )
    )
        
  resultado = validar_movimientos(movimientos)

  print(
        json.dumps(
        [m.model_dump() for m in resultado],
        indent=2,
        ensure_ascii=False
        )
    )

