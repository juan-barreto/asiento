import os
import re
import json
from groq import Groq
from dotenv import load_dotenv
from app.services.pdf_processor import extraccion_texto_por_pagina
from app.services.validator import validar_movimientos
import time

# Config

load_dotenv()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

# Normalizacion texto PDF

def normalize_text(text):
    """
    Esta funcion convierte el texto vertical en un texto mas lineal.

    """
    # Elimina múltiples saltos de linea generados
    
    text = re.sub(r"\n+", "\n", text) 
    
    # Une lineas cortadas (saltos de linea seguidos en el texto)
    text = re.sub(r"\n(?=\S)", " ", text)
    return text.strip()

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

def parse_page_with_ai(page_text):
    """
    Esta funcion manda una pagina a la IA y te devuelve movimientos en formato unico

    """
    prompt = f"""
Extraé movimientos bancarios y devolvé SOLO JSON válido.

REGLAS:
- fecha => DD/MM/YYYY
- debito => positivo si resta dinero
- credito => positivo si suma dinero
- nunca debito y credito juntos
- números con punto decimal
- ignorar encabezados y textos legales

FORMATO:
[
  {{
    "fecha": "DD/MM/YYYY",
    "descripcion": "",
    "detalle": "",
    "debito": 0.00,
    "credito": 0.00,
    "saldo": 0.00
  }}
]

Texto:
{page_text}
]

EJEMPLOS DE CONVERSIÓN:

Input: "02/01/26 TRF INMED PROVEED  -78.000,00  20.597.811,14"
Output: {{"fecha": "02/01/2026", "descripcion": "TRF INMED PROVEED", "debito": 78000.0, "credito": 0.0, "saldo": 20597811.14}}

Input: "07/11/2025 CR.TRAN. CONS PALACIO DE  500000.00  07-11  9374275.07"
Output: {{"fecha": "07/11/2025", "descripcion": "CR.TRAN. CONS PALACIO DE", "debito": 0.0, "credito": 500000.0, "saldo": 9374275.07}}

Input: "30/12/25 ACREDITAMIENTO CANJE GALICIA  1.845.300,00  20.686.882,94"
Output: {{"fecha": "30/12/2025", "descripcion": "ACREDITAMIENTO CANJE GALICIA", "debito": 0.0, "credito": 1845300.0, "saldo": 20686882.94}}

Texto del PDF:
{page_text}
"""
    
    try:
        res = client.chat.completions.create(
            messages =[
                {"role": "system", "content": "Sos un extractor de datos bancarios. Respondés SOLO con JSON valido, sin texto extra."},
                {"role": "user", "content": prompt}
            ],
            model = "llama-3.1-8b-instant",
            temperature = 0.1  #palabra clave para determinar la exactitud de la IA
        )

        content = res.choices[0].message.content
        content = clean_json_response(content)
        movimientos = json.loads(content)
        return movimientos
    
    except Exception as e:
        print(f"\n❌ Error JSON en respuesta de IA:")
        print(f"Contenido: {content if 'content' in locals() else 'Sin respuesta'}")
        print(f"Error: {e}")
        return []
    
    except Exception as e:
        print(f"\n❌ Error general en IA. {e}")
        return []
    
    # Proceso completo

def parse_all_pages(pages_data):
        """
        Esta funcion procesa todas las paginas del PDF y devuelve los movimientos crudos que no estan validados.

        """
        all_results = []

        for page in pages_data:
            print(f"📄 Procesando página {page['page_number']}...")

            # 1. Normalizar texto
            clean_text = normalize_text(page["text"])

            # 2. Mandar a IA 
            movimientos = parse_page_with_ai(clean_text)

            time.sleep(2)

            # 3. Acumular (sin validar todavia)
            all_results.extend(movimientos)


            print(f"   Extraídos {len(movimientos)} movimiento   ")

        return all_results
    
    # Prueba

if __name__ == "__main__":
    texto_prueba = [{'page_number': 0, 'text': '20120841050\n001\nSr. EMILIO ROBERTO SARA\nCantidad de Titulares:\n055835/6\nDNI\nExtracto de Cuenta Informativo\nPARANA 623, PISO1   A\nEmitido el\nMENSUAL\n55-CUENTA CORRIENTE INDIVIDUOS\nCUENTA CORRIENTE EN PESOS\nFrecuencia\n5026 - AVELLANEDA\nCIUDAD AUTONOMA BUENOS AIRES\n01/12/2025\nCBU:\n0140024301502605583560\n055835/6\nFecha\nConcepto\nFecha Valor\nSaldo\nImporte\n31/10/2025\nSALDO ANTERIOR\n23937107.50\n03/11/2025\nBIP DB.TR.01/11-C.798921 D:20142892066 N:GAITAN ROBERTO\n-100000.00\n03-11\n23837107.50\n03/11/2025\nIMPUESTO DEBITO -LEY 25413\n-600.00\n03-11\n23836507.50\n03/11/2025\nBIP DB.TR.03/11-C.915277 D:20120841050 N:EMILIO ROBERTO\n-350000.00\n03-11\n23486507.50\n03/11/2025\nIMPUESTO DEBITO -LEY 25413\n-2100.00\n03-11\n23484407.50\n03/11/2025\nREV. IMP.DEBITO.-LEY 25413\n2100.00\n03-11\n23486507.50\n04/11/2025\nBIP DB.TR.04/11-C.959312 D:20359398035 N:ALMARAZ PABLO\n-1120305.00\n04-11\n22366202.50\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-6721.83\n04-11\n22359480.67\n04/11/2025\nBIP DB.TR.04/11-C.959469 D:20177573028 N:DIAZ LOBO IGNA\n-855042.00\n04-11\n21504438.67\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-5130.25\n04-11\n21499308.42\n04/11/2025\nBIP DB.TR.04/11-C.959604 D:27300865483 N:GIMENEZ ERNEST\n-881505.00\n04-11\n20617803.42\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-5289.03\n04-11\n20612514.39\n04/11/2025\nBIP DB.TR.04/11-C.894683 D:20230683477 N:MORALES CRISTI\n-896844.00\n04-11\n19715670.39\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-5381.06\n04-11\n19710289.33\n04/11/2025\nBIP DB.TR.04/11-C.910724 D:20142892066 N:GAITAN ROBERTO\n-857547.00\n04-11\n18852742.33\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-5145.28\n04-11\n18847597.05\n04/11/2025\nBIP DB.TR.04/11-C.894957 D:20338561734 N:ACEVEDO JONATA\n-900295.00\n04-11\n17947302.05\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-5401.77\n04-11\n17941900.28\n04/11/2025\nBIP DB.TR.04/11-C.962117 D:20120841050 N:EMILIO ROBERTO\n-6626700.00\n04-11\n11315200.28\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-39760.20\n04-11\n11275440.08\n04/11/2025\nDB.DEBIN 04/11-S.824833 C:23310065889\n-656831.00\n04-11\n10618609.08\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-3940.99\n04-11\n10614668.09\n04/11/2025\nBIP DB.TR.04/11-C.915680 D:23129211059 N:PAZ EDUARDO\nAN\n-1319536.00\n04-11\n9295132.09'}, {'page_number': 1, 'text': '20120841050\n001\nSr. EMILIO ROBERTO SARA\nCantidad de Titulares:\n055835/6\nDNI\nExtracto de Cuenta Informativo\nPARANA 623, PISO1   A\nEmitido el\nMENSUAL\n55-CUENTA CORRIENTE INDIVIDUOS\nCUENTA CORRIENTE EN PESOS\nFrecuencia\n5026 - AVELLANEDA\nCIUDAD AUTONOMA BUENOS AIRES\n01/12/2025\nCBU:\n0140024301502605583560\n055835/6\nFecha\nConcepto\nFecha Valor\nSaldo\nImporte\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-7917.22\n04-11\n9287214.87\n04/11/2025\nBIP DB.TR.04/11-C.921218 D:30718971140 N:ORDEN Y\nCUSTOD\n-450000.00\n04-11\n8837214.87\n04/11/2025\nIMPUESTO DEBITO -LEY 25413\n-2700.00\n04-11\n8834514.87\n04/11/2025\nREV. IMP.DEBITO.-LEY 25413\n39760.20\n04-11\n8874275.07\n07/11/2025\nCR.TRAN. 30559342064 CONS PALACIO DE\n500000.00\n07-11\n9374275.07\n07/11/2025\nIMPUESTO CREDITO -LEY 25413    0001\n-3000.00\n07-11\n9371275.07\n10/11/2025\nBIP DB.TR.10/11-C.204399 D:20230683477 N:MORALES CRISTI\n-300000.00\n10-11\n9071275.07\n10/11/2025\nIMPUESTO DEBITO -LEY 25413\n-1800.00\n10-11\n9069475.07\n10/11/2025\nBIP DB.TR.10/11-C.254594 D:20120841050 N:EMILIO ROBERTO\n-450000.00\n10-11\n8619475.07\n10/11/2025\nIMPUESTO DEBITO -LEY 25413\n-2700.00\n10-11\n8616775.07\n10/11/2025\nBIP DB.TR.10/11-C.267482 D:20359398035 N:ALMARAZ PABLO\n-100000.00\n10-11\n8516775.07\n10/11/2025\nIMPUESTO DEBITO -LEY 25413\n-600.00\n10-11\n8516175.07\n10/11/2025\nREV. IMP.DEBITO.-LEY 25413\n2700.00\n10-11\n8518875.07\n11/11/2025\nCOMPRA TARJETA 11/11/25 13:23 COMPR. 000531513564539\n-13000.00\n11-11\n8505875.07\n11/11/2025\nIMPUESTO DEBITO -LEY 25413\n-78.00\n11-11\n8505797.07\n17/11/2025\nCR.TRAN. 30559342064 CONS PALACIO DE\n4000000.00\n17-11\n12505797.07\n17/11/2025\nIMPUESTO CREDITO -LEY 25413    0001\n-24000.00\n17-11\n12481797.07\n18/11/2025\nBIP DB.TR.18/11-C.638205 D:20359398035 N:ALMARAZ PABLO\n-42250.00\n18-11\n12439547.07\n18/11/2025\nIMPUESTO DEBITO -LEY 25413\n-253.50\n18-11\n12439293.57\n18/11/2025\nBIP DB.TR.18/11-C.576555 D:20142892066 N:GAITAN ROBERTO\n-342900.00\n18-11\n12096393.57\n18/11/2025\nIMPUESTO DEBITO -LEY 25413\n-2057.40\n18-11\n12094336.17\n18/11/2025\nBIP DB.TR.18/11-C.640011 D:27300865483 N:GIMENEZ ERNEST\n-325100.00\n18-11\n11769236.17\n18/11/2025\nIMPUESTO DEBITO -LEY 25413\n-1950.60\n18-11\n11767285.57'}, {'page_number': 2, 'text': '20120841050\n001\nSr. EMILIO ROBERTO SARA\nCantidad de Titulares:\n055835/6\nDNI\nExtracto de Cuenta Informativo\nPARANA 623, PISO1   A\nEmitido el\nMENSUAL\n55-CUENTA CORRIENTE INDIVIDUOS\nCUENTA CORRIENTE EN PESOS\nFrecuencia\n5026 - AVELLANEDA\nCIUDAD AUTONOMA BUENOS AIRES\n01/12/2025\nCBU:\n0140024301502605583560\n055835/6\nFecha\nConcepto\nFecha Valor\nSaldo\nImporte\n18/11/2025\nBIP DB.TR.18/11-C.576855 D:20230683477 N:MORALES CRISTI\n-291000.00\n18-11\n11476285.57\n18/11/2025\nIMPUESTO DEBITO -LEY 25413\n-1746.00\n18-11\n11474539.57\n18/11/2025\nBIP DB.TR.18/11-C.639103 D:20120841050 N:EMILIO ROBERTO\n-1900000.00\n18-11\n9574539.57\n18/11/2025\nIMPUESTO DEBITO -LEY 25413\n-11400.00\n18-11\n9563139.57\n18/11/2025\nDB.DEBIN 18/11-S.341215 C:20120841050\n-400000.00\n18-11\n9163139.57\n18/11/2025\nIMPUESTO DEBITO -LEY 25413\n-2400.00\n18-11\n9160739.57\n18/11/2025\nREV. IMP.DEBITO.-LEY 25413\n11400.00\n18-11\n9172139.57\n18/11/2025\nREV. IMP.DEBITO.-LEY 25413\n2400.00\n18-11\n9174539.57\n19/11/2025\nBIP DB.TR.19/11-C.698975 D:20120841050 N:EMILIO ROBERTO\n-350000.00\n19-11\n8824539.57\n19/11/2025\nIMPUESTO DEBITO -LEY 25413\n-2100.00\n19-11\n8822439.57\n19/11/2025\nREV. IMP.DEBITO.-LEY 25413\n2100.00\n19-11\n8824539.57\n20/11/2025\nDB.DEBIN 20/11-S.315415 C:24308340259\n-1457034.00\n20-11\n7367505.57\n20/11/2025\nIMPUESTO DEBITO -LEY 25413\n-8742.20\n20-11\n7358763.37\n20/11/2025\nCR.TRAN. 30559342064 CONS PALACIO DE\n6766933.00\n20-11\n14125696.37\n20/11/2025\nIMPUESTO CREDITO -LEY 25413    0001\n-40601.60\n20-11\n14085094.77\n25/11/2025\nPAGO LIQUIDACION VISA\n-241366.78\n25-11\n13843727.99\n25/11/2025\nIMPUESTO DEBITO -LEY 25413\n-1448.20\n25-11\n13842279.79\n26/11/2025\nCR.TRAN. 30536273804 CONSORCIO DE PROPIETARIOS SAN\n4495100.00\n26-11\n18337379.79\n26/11/2025\nIMPUESTO CREDITO -LEY 25413    0023\n-26970.60\n26-11\n18310409.19\n27/11/2025\nCRED.TRF.27/11-C.905669 D:33512133679 N:TOTAL SYR SA\n9568737.00\n27-11\n27879146.19\n27/11/2025\nIMPUESTO CREDITO -LEY 25413\n-57412.42\n27-11\n27821733.77\n28/11/2025\nBIP DB.TR.28/11-C.018268 D:20120841050 N:EMILIO ROBERTO\n-500000.00\n28-11\n27321733.77\n28/11/2025\nIMPUESTO DEBITO -LEY 25413\n-3000.00\n28-11\n27318733.77'}, {'page_number': 3, 'text': '20120841050\n001\nSr. EMILIO ROBERTO SARA\nCantidad de Titulares:\n055835/6\nDNI\nExtracto de Cuenta Informativo\nPARANA 623, PISO1   A\nEmitido el\nMENSUAL\n55-CUENTA CORRIENTE INDIVIDUOS\nCUENTA CORRIENTE EN PESOS\nFrecuencia\n5026 - AVELLANEDA\nCIUDAD AUTONOMA BUENOS AIRES\n01/12/2025\nCBU:\n0140024301502605583560\n055835/6\nFecha\nConcepto\nFecha Valor\nSaldo\nImporte\n28/11/2025\nBIP DB.TR.28/11-C.018304 D:30718971140 N:ORDEN Y\nCUSTOD\n-350000.00\n28-11\n26968733.77\n28/11/2025\nIMPUESTO DEBITO -LEY 25413\n-2100.00\n28-11\n26966633.77\n28/11/2025\nDB.DEBIN 28/11-S.593207 C:20120841050\n-350000.00\n28-11\n26616633.77\n28/11/2025\nIMPUESTO DEBITO -LEY 25413\n-2100.00\n28-11\n26614533.77\n28/11/2025\nREV. IMP.DEBITO.-LEY 25413\n3000.00\n28-11\n26617533.77\n28/11/2025\nREV. IMP.DEBITO.-LEY 25413\n2100.00\n28-11\n26619633.77\n01/12/2025\nCOMPRA TARJETA 28/11/25 17:47 COMPR. 000533220071540\n-40710.00\n01-12\n26578923.77\n01/12/2025\nIMPUESTO DEBITO -LEY 25413\n-244.26\n01-12\n26578679.51\n01/12/2025\nCOMPRA TARJETA M.E. 28/11/25 20:23 COMPR.\n000533220348330\n-66876.50\n01-12\n26511803.01\n01/12/2025\nIMPUESTO DEBITO -LEY 25413\n-401.26\n01-12\n26511401.75\n01/12/2025\nIMPUESTO RG 5617\n-19740.40\n01-12\n26491661.35\n01/12/2025\nIMPUESTO DEBITO -LEY 25413\n-118.44\n01-12\n26491542.91\n01/12/2025\nCOMPRA TARJETA 29/11/25 11:06 COMPR. 000533314734502\n-67279.50\n01-12\n26424263.41\n01/12/2025\nIMPUESTO DEBITO -LEY 25413\n-403.68\n01-12\n26423859.73\n01/12/2025\nDEPOSITO CHEQUES C/BANCOS BOLETA NRO: 000000000001\n3864973.62\n28-11\n30288833.35\n01/12/2025\nIMPUESTO CREDITO -LEY 25413\n-23189.84\n28-11\n30265643.51\n01/12/2025\nDB.DEBIN 01/12-S.508930 C:20120841050\n-400000.00\n01-12\n29865643.51\n01/12/2025\nIMPUESTO DEBITO -LEY 25413\n-2400.00\n01-12\n29863243.51\n01/12/2025\nBIP DB TR 01/12-C.000446429589 DES:0014-03-502605407206\n-350000.00\n01-12\n29513243.51\n01/12/2025\nCOMPRA TARJETA 01/12/25 14:28 COMPR. 000533514084501\n-25900.00\n01-12\n29487343.51\n01/12/2025\nIMPUESTO DEBITO -LEY 25413\n-155.40\n01-12\n29487188.11\n01/12/2025\nCOMPRA TARJETA 01/12/25 11:46 COMPR. 000533514094085\n-59667.00\n01-12\n29427521.11\n01/12/2025\nIMPUESTO DEBITO -LEY 25413\n-358.00\n01-12\n29427163.11'}, {'page_number': 4, 'text': '20120841050\n001\nSr. EMILIO ROBERTO SARA\nCantidad de Titulares:\n055835/6\nDNI\nExtracto de Cuenta Informativo\nPARANA 623, PISO1   A\nEmitido el\nMENSUAL\n55-CUENTA CORRIENTE INDIVIDUOS\nCUENTA CORRIENTE EN PESOS\nFrecuencia\n5026 - AVELLANEDA\nCIUDAD AUTONOMA BUENOS AIRES\n01/12/2025\nCBU:\n0140024301502605583560\n055835/6\nFecha\nConcepto\nFecha Valor\nSaldo\nImporte\n01/12/2025\nREV. IMP.DEBITO.-LEY 25413\n2400.00\n01-12\n29429563.11\nTodas las comisiones y cargos percibidos por el Banco se encuentran publicados en www.bancoprovincia.com.ar; ‘Comisiones, Tasas y Cargos’\nImporte\nLos números con signo negativo en el campo "IMPORTE" corresponden a operaciones de débito, mientras que los que no llevan signo corresponden a\noperaciones de crédito.\n01/11/2025\nITF-LEY25413(DEB):\n$0.00\nITF-LEY25413(CRE):\n$-69003.33\nTot. Retención ARBA\nS/Dec. 380/01 Y MOD.:\n$-151984.62\n$0.00\nDESDE:\nTasa de interés para descubiertos en Cuentas Corrientes:\nA  partir  del  mes  de  Febrero  de  2014,  la  variabilidad  de  la  de  interés  se  rige  por  la  tasa  badlar  bancos  privados  promedio  últimos  5  días  hábiles,\ndisponibles  al  cierre  de  cada  mes.\nUsted puede solicitar la “Caja de ahorros” en pesos con las prestaciones previstas en el punto 1.8. de las normas sobre “Depósitos de ahorro, cuenta\nsueldo y especiales”, las cuales serán gratuitas. Usted puede consultar el “Régimen de Transparencia” elaborado por el Banco Central sobre la base de la\ninformación proporcionada por los sujetos obligados a fin de comparar los costos y características de los productos y servicios financieros ingresando a\nhttp://www.bcra.gob.ar/BCRAyVos/Regimen_de_transparencia.asp.\nLe  informamos  que  a  partir  del  día  01.09.2016,  el  Banco  dejará  de  percibir  el  cargo  correspondiente  al  seguro  de  vida  sobre  saldo  deudor,  según\nComunicación  "A"  5928  del  B.C.R.A.\nFecha Valor\nFecha en la cual se hizo efectivo el movimiento (independientemente de la fecha en que se contabilice la misma por el sistema) y es tomada a efectos de\ncálculo de intereses.\nCondiciones de Garantía\nLos depósitos en pesos y en moneda extranjera cuentan con la garantía de hasta $ 6.000.000. En las operaciones a nombre de dos o más personas, la\ngarantía se prorrateará entre sus titulares. En ningún caso, el total de la garantía por persona y por depósito podrá exceder de $ 6.000.000, cualquiera\nsea el número de cuentas y/o depósitos. Ley 24.485, Decreto Nº 540/95 y modificatorios y Com. "A" 6973 y sus modificatorias y complementarias.\nSe encuentran excluidos los captados a tasas superiores a la de referencia conforme a los límites establecidos por el Banco Central, los adquiridos por\nendoso y los efectuados por personas vinculadas a la entidad financiera.\nLa\n totalidad\n de\n los\n depósitos\n efectuados\n en\n esta\n Institución,\n se\n encuentran\n garantizados\n por\n la\n Provincia\n de\n Buenos\n Aires.\nPor disposición del Juzgado en lo Civil y Comercial n° 16 de La Plata se informa a efectos de ejercer el derecho contemplado en el art. 54 de la Ley 24.240\n(Opt  Out  o  exclusión),  la  existencia  de  los  autos  “CENTRO  DE  ORIENTACIÓN  DEFENSA  Y  EDUCACIÓN  DEL  CONSUMIDOR  –  CODECC/BANCO  DE  LA\nPROVINCIA DE BUENOS AIRES S/NULIDAD DE CONTRATO” Expte. LP-33992-2017, en trámite por ante el Jdo. en lo C. y C. n°16 de La Plata, en los que se\ndemanda  la  nulidad  de  la  modificación  del  medio  de  envío  del  resumen  de  cuenta  y  tarjetas  (de  formato  papel  a  electrónico),  así  como  de  todo  lo\ncobrado por “Cargo por envío postal”, el cese de dicho cobro, la restitución de lo percibido con intereses, el envío de los resúmenes en papel a todo\naquel que no hubiera solicitado el cambio de modalidad, multa civil y administrativa. No es necesario presentarse al Juzgado, ni realizar ningún trámite.\nEl resultado del proceso solo puede beneficiarlo (según art. 54 de la ley de defensa del consumidor), que significa que una eventual sentencia en contra\nno puede provocarle ningún perjuicio.'}]
    
  



    resultado = parse_all_pages(texto_prueba)
        
    print(json.dumps(resultado, indent=2, ensure_ascii=False))  

    

