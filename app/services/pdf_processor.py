import fitz  # libreria PyMuPDF


def extraccion_texto_por_pagina(pdf_path):

    """
    Esta funcion extraer el texto del PDF por página y me devuelve lo siguiente:
    
        [
            { "page_number": 0, "text": "..."}
            { "page_number": 1, "text": "..."} 
        ]
    """

    doc = fitz.open(pdf_path)
    datos_pagina = []

    for i, page in enumerate(doc):
        text = page.get_text()
        datos_pagina.append({
            "page_number": i,
            "text": text.strip()
        })
        
    doc.close()
    return datos_pagina


#Prueba
if __name__ == "__main__":
    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    data = extraccion_texto_por_pagina(pdf_path)
    print(data)
    