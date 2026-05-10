from datetime import datetime
import re
import json

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

        m["confidence"] = calcular_confidence(m)


    # 4. Agregamos a la lista
        resultado.append(m)


    return resultado

def validar_estructura(m):
    """
    Esta funcion verifica que tenga los campos minimos

    """
    campos_requeridos = ["fecha", "descripcion", "saldo"]

    for campo in campos_requeridos:
        if campo not in m or not m[campo]:
            return False
        
    return True


def normalizar_movimiento(m):
    """
    Esta funcion normaliza las fechas, numeros y texto
    
    """

    # Normalizamos fecha:

    m["fecha"] = normalizar_fecha(m.get("fecha", ""))
    m["debito"] = abs(float(m.get("debito", 0)))
    m["credito"] = abs(float(m.get("credito", 0)))
    m["saldo"] = abs(float(m.get("saldo", 0)))

    # Limpiamos el texto:

    m["descripcion"] = m.get("descripcion", "").strip()
    m["detalle"] = m.get("detalle", "").strip()

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

    if not m.get("descripcion"):
        score -= 0.2

    if m["debito"] == 0 and m["credito"] == 0:
        score -= 0.5

    if m["debito"] > 0 and m["credito"] > 0:
        score -= 0.6

    if not m.get("fecha"):
        score -= 0.4

    if m["saldo"] == 0:
        score -= 0.1

    return max(0.0, min(1.0, score))

if __name__ == "__main__":

  prueba = [
  {
    "fecha": "01/12/2025",
    "descripcion": "SALDO ANTERIOR",
    "detalle": "",
    "debito": 0.0,
    "credito": 0.0,
    "saldo": 23937107.5
  },
  {
    "fecha": "03/11/2025",
    "descripcion": "BIP DB.TR.01/11-C.798921",
    "detalle": "D:20142892066 N:GAITAN ROBERTO",
    "debito": 100000.0,
    "credito": 0.0,
    "saldo": 23837107.5
  },
  {
    "fecha": "03/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 600.0,
    "credito": 0.0,
    "saldo": 23836507.5
  },
  {
    "fecha": "03/11/2025",
    "descripcion": "BIP DB.TR.03/11-C.915277",
    "detalle": "D:20120841050 N:EMILIO ROBERTO",
    "debito": 350000.0,
    "credito": 0.0,
    "saldo": 23486507.5
  },
  {
    "fecha": "03/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 2100.0,
    "credito": 0.0,
    "saldo": 23484407.5
  },
  {
    "fecha": "03/11/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 2100.0,
    "saldo": 23486507.5
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "BIP DB.TR.04/11-C.959312",
    "detalle": "D:20359398035 N:ALMARAZ PABLO",
    "debito": 1120305.0,
    "credito": 0.0,
    "saldo": 22366202.5
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 6721.83,
    "credito": 0.0,
    "saldo": 22359480.67
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "BIP DB.TR.04/11-C.959469",
    "detalle": "D:20177573028 N:DIAZ LOBO IGNA",
    "debito": 855042.0,
    "credito": 0.0,
    "saldo": 21504438.67
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 5130.25,
    "credito": 0.0,
    "saldo": 21499308.42
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "BIP DB.TR.04/11-C.959604",
    "detalle": "D:27300865483 N:GIMENEZ ERNEST",
    "debito": 881505.0,
    "credito": 0.0,
    "saldo": 20617803.42
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 5289.03,
    "credito": 0.0,
    "saldo": 20612514.39
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "BIP DB.TR.04/11-C.894683",
    "detalle": "D:20230683477 N:MORALES CRISTI",
    "debito": 896844.0,
    "credito": 0.0,
    "saldo": 19715670.39
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 5381.06,
    "credito": 0.0,
    "saldo": 19710289.33
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "BIP DB.TR.04/11-C.910724",
    "detalle": "D:20142892066 N:GAITAN ROBERTO",
    "debito": 857547.0,
    "credito": 0.0,
    "saldo": 18852742.33
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 5145.28,
    "credito": 0.0,
    "saldo": 18847597.05
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "BIP DB.TR.04/11-C.894957",
    "detalle": "D:20338561734 N:ACEVEDO JONATA",
    "debito": 900295.0,
    "credito": 0.0,
    "saldo": 17947302.05
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 5401.77,
    "credito": 0.0,
    "saldo": 17941900.28
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "BIP DB.TR.04/11-C.962117",
    "detalle": "D:20120841050 N:EMILIO ROBERTO",
    "debito": 6626700.0,
    "credito": 0.0,
    "saldo": 11315200.28
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 39760.2,
    "credito": 0.0,
    "saldo": 11275440.08
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "DB.DEBIN 04/11-S.824833",
    "detalle": "C:23310065889",
    "debito": 656831.0,
    "credito": 0.0,
    "saldo": 10618609.08
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 3940.99,
    "credito": 0.0,
    "saldo": 10614668.09
  },
  {
    "fecha": "04/11/2025",
    "descripcion": "BIP DB.TR.04/11-C.915680",
    "detalle": "D:23129211059 N:PAZ EDUARDO AN",
    "debito": 1319536.0,
    "credito": 0.0,
    "saldo": 9295132.09
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-LEY 25413",
    "debito": 7917.22,
    "credito": 0.0,
    "saldo": 9287214.87
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "BIP DB.TR.04/11-C.921218 D:30718971140 N:ORDEN Y CUSTOD",
    "detalle": "-450000.00",
    "debito": 450000.0,
    "credito": 0.0,
    "saldo": 8837214.87
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-2700.00",
    "debito": 2700.0,
    "credito": 0.0,
    "saldo": 8834514.87
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "39760.20",
    "debito": 0.0,
    "credito": 39760.2,
    "saldo": 8874275.07
  },
  {
    "fecha": "07/11/2025",
    "descripcion": "CR.TRAN. 30559342064 CONS PALACIO DE",
    "detalle": "500000.00",
    "debito": 0.0,
    "credito": 500000.0,
    "saldo": 9374275.07
  },
  {
    "fecha": "07/11/2025",
    "descripcion": "IMPUESTO CREDITO -LEY 25413",
    "detalle": "-3000.00",
    "debito": 0.0,
    "credito": 3000.0,
    "saldo": 9371275.07
  },
  {
    "fecha": "10/11/2025",
    "descripcion": "BIP DB.TR.10/11-C.204399 D:20230683477 N:MORALES CRISTI",
    "detalle": "-300000.00",
    "debito": 300000.0,
    "credito": 0.0,
    "saldo": 9071275.07
  },
  {
    "fecha": "10/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-1800.00",
    "debito": 1800.0,
    "credito": 0.0,
    "saldo": 9069475.07
  },
  {
    "fecha": "10/11/2025",
    "descripcion": "BIP DB.TR.10/11-C.254594 D:20120841050 N:EMILIO ROBERTO",
    "detalle": "-450000.00",
    "debito": 450000.0,
    "credito": 0.0,
    "saldo": 8619475.07
  },
  {
    "fecha": "10/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-2700.00",
    "debito": 2700.0,
    "credito": 0.0,
    "saldo": 8616775.07
  },
  {
    "fecha": "10/11/2025",
    "descripcion": "BIP DB.TR.10/11-C.267482 D:20359398035 N:ALMARAZ PABLO",
    "detalle": "-100000.00",
    "debito": 100000.0,
    "credito": 0.0,
    "saldo": 8516775.07
  },
  {
    "fecha": "10/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-600.00",
    "debito": 600.0,
    "credito": 0.0,
    "saldo": 8516175.07
  },
  {
    "fecha": "10/11/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "2700.00",
    "debito": 0.0,
    "credito": 2700.0,
    "saldo": 8518875.07
  },
  {
    "fecha": "11/11/2025",
    "descripcion": "COMPRA TARJETA 11/11/25 13:23 COMPR. 000531513564539",
    "detalle": "-13000.00",
    "debito": 13000.0,
    "credito": 0.0,
    "saldo": 8505875.07
  },
  {
    "fecha": "11/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-78.00",
    "debito": 78.0,
    "credito": 0.0,
    "saldo": 8505797.07
  },
  {
    "fecha": "17/11/2025",
    "descripcion": "CR.TRAN. 30559342064 CONS PALACIO DE",
    "detalle": "4000000.00",
    "debito": 0.0,
    "credito": 4000000.0,
    "saldo": 12505797.07
  },
  {
    "fecha": "17/11/2025",
    "descripcion": "IMPUESTO CREDITO -LEY 25413",
    "detalle": "-24000.00",
    "debito": 0.0,
    "credito": 24000.0,
    "saldo": 12481797.07
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "BIP DB.TR.18/11-C.638205 D:20359398035 N:ALMARAZ PABLO",
    "detalle": "-42250.00",
    "debito": 42250.0,
    "credito": 0.0,
    "saldo": 12439547.07
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-253.50",
    "debito": 253.5,
    "credito": 0.0,
    "saldo": 12439293.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "BIP DB.TR.18/11-C.576555 D:20142892066 N:GAITAN ROBERTO",
    "detalle": "-342900.00",
    "debito": 342900.0,
    "credito": 0.0,
    "saldo": 12096393.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-2057.40",
    "debito": 2057.4,
    "credito": 0.0,
    "saldo": 12094336.17
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "BIP DB.TR.18/11-C.640011 D:27300865483 N:GIMENEZ ERNEST",
    "detalle": "-325100.00",
    "debito": 325100.0,
    "credito": 0.0,
    "saldo": 11769236.17
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "-1950.60",
    "debito": 1950.6,
    "credito": 0.0,
    "saldo": 11767285.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "BIP DB.TR.18/11-C.576855 D:20230683477 N:MORALES CRISTI",
    "detalle": "",
    "debito": 291000.0,
    "credito": 0.0,
    "saldo": 11476285.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 1746.0,
    "credito": 0.0,
    "saldo": 11474539.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "BIP DB.TR.18/11-C.639103 D:20120841050 N:EMILIO ROBERTO",
    "detalle": "",
    "debito": 1900000.0,
    "credito": 0.0,
    "saldo": 9574539.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 11400.0,
    "credito": 0.0,
    "saldo": 9563139.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "DB.DEBIN 18/11-S.341215 C:20120841050",
    "detalle": "",
    "debito": 400000.0,
    "credito": 0.0,
    "saldo": 9163139.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 2400.0,
    "credito": 0.0,
    "saldo": 9160739.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 11400.0,
    "saldo": 9172139.57
  },
  {
    "fecha": "18/11/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 2400.0,
    "saldo": 9174539.57
  },
  {
    "fecha": "19/11/2025",
    "descripcion": "BIP DB.TR.19/11-C.698975 D:20120841050 N:EMILIO ROBERTO",
    "detalle": "",
    "debito": 350000.0,
    "credito": 0.0,
    "saldo": 8824539.57
  },
  {
    "fecha": "19/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 2100.0,
    "credito": 0.0,
    "saldo": 8822439.57
  },
  {
    "fecha": "19/11/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 2100.0,
    "saldo": 8824539.57
  },
  {
    "fecha": "20/11/2025",
    "descripcion": "DB.DEBIN 20/11-S.315415 C:24308340259",
    "detalle": "",
    "debito": 1457034.0,
    "credito": 0.0,
    "saldo": 7367505.57
  },
  {
    "fecha": "20/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 8742.2,
    "credito": 0.0,
    "saldo": 7358763.37
  },
  {
    "fecha": "20/11/2025",
    "descripcion": "CR.TRAN. 30559342064 CONS PALACIO DE",
    "detalle": "",
    "debito": 0.0,
    "credito": 6766933.0,
    "saldo": 14125696.37
  },
  {
    "fecha": "20/11/2025",
    "descripcion": "IMPUESTO CREDITO -LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 40601.6,
    "saldo": 14085094.77
  },
  {
    "fecha": "25/11/2025",
    "descripcion": "PAGO LIQUIDACION VISA",
    "detalle": "",
    "debito": 241366.78,
    "credito": 0.0,
    "saldo": 13843727.99
  },
  {
    "fecha": "25/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 1448.2,
    "credito": 0.0,
    "saldo": 13842279.79
  },
  {
    "fecha": "26/11/2025",
    "descripcion": "CR.TRAN. 30536273804 CONSORCIO DE PROPIETARIOS SAN",
    "detalle": "",
    "debito": 0.0,
    "credito": 4495100.0,
    "saldo": 18337379.79
  },
  {
    "fecha": "26/11/2025",
    "descripcion": "IMPUESTO CREDITO -LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 26970.6,
    "saldo": 18310409.19
  },
  {
    "fecha": "27/11/2025",
    "descripcion": "CRED.TRF.27/11-C.905669 D:33512133679 N:TOTAL SYR SA",
    "detalle": "",
    "debito": 0.0,
    "credito": 9568737.0,
    "saldo": 27879146.19
  },
  {
    "fecha": "27/11/2025",
    "descripcion": "IMPUESTO CREDITO -LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 57412.42,
    "saldo": 27821733.77
  },
  {
    "fecha": "28/11/2025",
    "descripcion": "BIP DB.TR.28/11-C.018268 D:20120841050 N:EMILIO ROBERTO",
    "detalle": "",
    "debito": 500000.0,
    "credito": 0.0,
    "saldo": 27321733.77
  },
  {
    "fecha": "28/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 3000.0,
    "credito": 0.0,
    "saldo": 27318733.77
  },
  {
    "fecha": "28/11/2025",
    "descripcion": "BIP DB.TR.28/11-C.018304",
    "detalle": "ORDEN Y CUSTOD",
    "debito": 30718971140.0,
    "credito": 0.0,
    "saldo": 26968733.77
  },
  {
    "fecha": "28/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 2100.0,
    "credito": 0.0,
    "saldo": 26966633.77
  },
  {
    "fecha": "28/11/2025",
    "descripcion": "DB.DEBIN 28/11-S.593207",
    "detalle": "20120841050",
    "debito": 350000.0,
    "credito": 0.0,
    "saldo": 26616633.77
  },
  {
    "fecha": "28/11/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 2100.0,
    "credito": 0.0,
    "saldo": 26614533.77
  },
  {
    "fecha": "28/11/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 3000.0,
    "saldo": 26617533.77
  },
  {
    "fecha": "28/11/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 2100.0,
    "saldo": 26619633.77
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "COMPRA TARJETA 28/11/25",
    "detalle": "17:47 COMPR. 000533220071540",
    "debito": 40710.0,
    "credito": 0.0,
    "saldo": 26578923.77
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 244.26,
    "credito": 0.0,
    "saldo": 26578679.51
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "COMPRA TARJETA M.E. 28/11/25",
    "detalle": "20:23 COMPR. 000533220348330",
    "debito": 66876.5,
    "credito": 0.0,
    "saldo": 26511803.01
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 401.26,
    "credito": 0.0,
    "saldo": 26511401.75
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO RG 5617",
    "detalle": "",
    "debito": 19740.4,
    "credito": 0.0,
    "saldo": 26491661.35
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 118.44,
    "credito": 0.0,
    "saldo": 26491542.91
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "COMPRA TARJETA 29/11/25",
    "detalle": "11:06 COMPR. 000533314734502",
    "debito": 67279.5,
    "credito": 0.0,
    "saldo": 26424263.41
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 403.68,
    "credito": 0.0,
    "saldo": 26423859.73
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "DEPOSITO CHEQUES C/BANCOS BOLETA NRO: 000000000001",
    "detalle": "3864973.62",
    "debito": 0.0,
    "credito": 30288833.35,
    "saldo": 30288833.35
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO CREDITO -LEY 25413",
    "detalle": "",
    "debito": 0.0,
    "credito": 23189.84,
    "saldo": 30265643.51
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "DB.DEBIN 01/12-S.508930",
    "detalle": "20120841050",
    "debito": 400000.0,
    "credito": 0.0,
    "saldo": 29865643.51
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 2400.0,
    "credito": 0.0,
    "saldo": 29863243.51
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "BIP DB TR 01/12-C.000446429589",
    "detalle": "DES:0014-03-502605407206",
    "debito": 350000.0,
    "credito": 0.0,
    "saldo": 29513243.51
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "COMPRA TARJETA 01/12/25",
    "detalle": "14:28 COMPR. 000533514084501",
    "debito": 25900.0,
    "credito": 0.0,
    "saldo": 29487343.51
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 155.4,
    "credito": 0.0,
    "saldo": 29487188.11
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "COMPRA TARJETA 01/12/25",
    "detalle": "11:46 COMPR. 000533514094085",
    "debito": 59667.0,
    "credito": 0.0,
    "saldo": 29427521.11
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "IMPUESTO DEBITO -LEY 25413",
    "detalle": "",
    "debito": 358.0,
    "credito": 0.0,
    "saldo": 29427163.11
  },
  {
    "fecha": "01/12/2025",
    "descripcion": "REV. IMP.DEBITO.-LEY 25413",
    "detalle": "",
    "debito": 2400.0,
    "credito": 0.0,
    "saldo": 29429563.11
  },
  {
    "fecha": "01/11/2025",
    "descripcion": "ITF-LEY25413(DEB)",
    "detalle": "",
    "debito": 0.0,
    "credito": 69003.33,
    "saldo": 29429563.11
  },
  {
    "fecha": "01/11/2025",
    "descripcion": "ITF-LEY25413(CRE)",
    "detalle": "",
    "debito": 151984.62,
    "credito": 0.0,
    "saldo": 29429563.11
  },
  {
    "fecha": "01/11/2025",
    "descripcion": "Tot. Retención ARBA S/Dec. 380/01 Y MOD.:",
    "detalle": "",
    "debito": 151984.62,
    "credito": 0.0,
    "saldo": 29429563.11
  },
  {
    "fecha": "01/11/2025",
    "descripcion": "DESDE: Tasa de interés para descubiertos en Cuentas Corrientes:",
    "detalle": "",
    "debito": 0.0,
    "credito": 0.0,
    "saldo": 29429563.11
  }
]


  resultado = validar_movimientos(prueba)
  print(json.dumps(resultado, indent=2, ensure_ascii=False))  

