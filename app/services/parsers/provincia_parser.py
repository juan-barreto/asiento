import re
from app.services.pdf_processor import extraccion_texto_por_pagina
from app.services.movimiento import MovimientoRaw, Movimiento

def es_fecha(linea):
    """
    Detecta si una línea es una fecha tipo:
    02/01/26
    """

    patron_fecha = r"^\d{2}/\d{2}/\d{4}$"

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

def parsear_movimiento(raw: MovimientoRaw):

    """ 
    print("\n----------------")
    print(raw.fecha)
    print(raw.bloque)
    print("----------------")
    """

    descripcion = raw.bloque[0] if raw.bloque else ""

    if descripcion.upper() == "SALDO ANTERIOR":
        return Movimiento(
        fecha=raw.fecha,
        descripcion=descripcion,
        detalle="",
        debito=0.0,
        credito=0.0,
        saldo=convertir_numero(raw.bloque[-1])
    )

    detalle = " | ".join(raw.bloque[1:-3]) 
    if len(raw.bloque) >= 3:
        importe = raw.bloque[-3]
    else:
        importe = ""
    """ print("Fecha:", raw.fecha)
    print("IMPORTE:", importe)
    print("DEBITO:", es_debito(importe))
    print("CREDITO:", es_credito(importe))"""
    
    if not (es_debito(importe) or es_credito(importe)):
        return None
    debito = convertir_numero(importe) if es_debito(importe) else 0.00
    credito = convertir_numero(importe) if es_credito(importe) else 0.00
    saldo = convertir_numero(raw.bloque[-1])
    return Movimiento(
        fecha=raw.fecha,
        descripcion= descripcion,
        detalle= detalle,
        debito= debito,
        credito= credito,
        saldo=saldo
    )
def convertir_numero(texto):
    try:
        if not texto:

            return 0.00

        texto = texto.strip()

        return float(texto)
    
    except ValueError:
        return 0.00

def es_debito(texto):
        patron = r"^-[\d\.]+\.\d{2}$"
        return re.match(patron, texto) is not None
    

def es_credito(texto):
        patron = r"^[\d\.]+\.\d{2}$"
        return re.match(patron, texto) is not None
    


def extraer_bloques_provincia(texto):
    """
    Esta funcion convierte el texto crudo del pdf en bloques estructurados, mejor para mejor lectura

    """
    fin_tabla = texto.find("Todas las comisiones y cargos")

    if fin_tabla != -1:
        texto = texto[:fin_tabla]

    lineas = limpiar_lineas(texto)

    movimientos = []

    movimiento_actual = None

    for linea in lineas:
        
        if linea == "Total":
            break

        if es_fecha(linea):

            if movimiento_actual:
                movimiento_parseado = parsear_movimiento(movimiento_actual)
                if movimiento_parseado:
                    movimientos.append(movimiento_parseado)

            movimiento_actual = MovimientoRaw(
                fecha=linea,
                bloque=[]
            )

        else:

            if not movimiento_actual:
                continue

            movimiento_actual.bloque.append(linea)

    if movimiento_actual:
        movimiento_actual_parseado = parsear_movimiento(movimiento_actual)
        movimientos.append(movimiento_actual_parseado)

    return movimientos


if __name__ == "__main__":

    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\5026558356_20251201_extractos.pdf"
    texto = extraccion_texto_por_pagina(pdf_path)
   
    for t in texto:
        limpio = extraer_bloques_movimientos(t["text"])
        print(limpio)