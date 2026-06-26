from app.services.pdf_processor import extraccion_texto_por_pagina

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

class Provincia(BaseBank):
      
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
