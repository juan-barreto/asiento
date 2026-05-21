import re
from pdf_processor import extraccion_texto_por_pagina

def es_fecha(linea):
    """
    Detecta si una línea es una fecha tipo:
    02/01/26
    """

    patron_fecha = r"^\d{2}/\d{2}/\d{2}$"

    return re.match(patron_fecha, linea.strip())

def limpiar_lineas(texto):
    """
    Esta función limpia los espacios y borra las lineas vacias.

    """
    lineas = texto.splitlines()

    lineas_limpias = []

    for linea in lineas:
        
        linea = linea.strip()

        if linea:
            lineas_limpias.append(linea)

    return lineas_limpias

def extraer_bloques_movimientos(texto):
    """
    Esta funcion convierte el texto crudo del pdf en bloques estructurados, mejor para la IA

    """

    lineas = limpiar_lineas(texto)

    movimientos= []

    movimiento_actual = None

    for linea in lineas:
        #primero identifico si encuentro una fecha ya que mi texto crudo tiene una secuencia detectable
        if es_fecha(linea):

            #guardo el último movimiento
            if movimiento_actual:
                movimientos.append(movimiento_actual)

            #creamos un nuevo movimiento
            movimiento_actual = {
                "fecha": linea,
                "bloque": []
            }
        else:

            #si todavia no empezo el movimiento, reiniciamos el bucle
            if not movimiento_actual:
                continue#agrego linea al bloque actual, osea agregara dentro de bloque hasta dar con otra fecha
            movimiento_actual["bloque"].append(linea)

        
        #guardo el ultimo movimiento
    if movimiento_actual:
            movimientos.append(movimiento_actual)

    return movimientos


if __name__ == "__main__":

    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    texto = extraccion_texto_por_pagina(pdf_path)
   
    for t in texto:
        limpio = extraer_bloques_movimientos(t["text"])
        print(limpio)