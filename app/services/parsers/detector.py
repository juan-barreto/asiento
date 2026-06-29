from app.services.pdf_processor import extraccion_texto_por_pagina
from app.services.parsers.galicia_parser import extraer_bloques_galicia
from app.services.parsers.provincia_parser import extraer_bloques_provincia

class BaseBank:

        nombre = ""
        keywords = []

        @classmethod
        def detectar(cls,paginas):

            texto = "\n".join(
                pagina["text"] for pagina in paginas
                ).upper()


            for palabra in cls.keywords:
                  
                  if palabra.upper() in texto:
                        return True
            return False
        
class Galicia(BaseBank):
      nombre = "Galicia"

      keywords = ["RESUMEN DE CUENTA CORRIENTE EN PESOS","MOVIMIENTOS"]   

      parser = extraer_bloques_galicia

class Provincia(BaseBank):
       
      parser = extraer_bloques_provincia

      nombre = "Provincia"

      keywords = ["FECHA VALOR"]
     

if __name__ == "__main__":
      
    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    textos = extraccion_texto_por_pagina(pdf_path)
    
    BANCOS = [
          Galicia,
          Provincia
    ]

    for banco in BANCOS:
          
          if banco.detectar(textos):
                print(banco.nombre)
                break
