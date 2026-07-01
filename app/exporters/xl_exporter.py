from openpyxl import Workbook
from app.services.pipeline import procesar_extracto


wb = Workbook()
ws = wb.active

# Encabezados
ws.append(["Fecha", "Descripcion","Detalle", "Crédito", "Debito", "Saldo", "Porcentaje de exito(1.00 = 100%)"])



if __name__ == "__main__":
    # Ruta al PDF
    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"
    
    # Procesar
    resultado = procesar_extracto(pdf_path)
    
    for movimiento in resultado.movimientos:
        ws.append([
            movimiento.fecha,
            movimiento.descripcion,
            movimiento.detalle,
            movimiento.credito,
            movimiento.debito,
            movimiento.saldo,
            movimiento.confidence

        ])
    
    # Ajuste automatico por ancho

    for columna in ws.columns:
        length = max(len(str(cell.value)) for cell in columna)
        ws.column_dimensions[columna[0].column_letter].width = length + 2


    wb.save("extracto_prueba4.xlsx")
