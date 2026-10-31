import os
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from backend.services.temp_files import temporal_file
from backend.services.exporters.excel import exportar_excel
from backend.services.exporters.csv import exportar_csv
from backend.services.exporters.txt import exportar_txt
from backend.models.statements import StatementResponse, TransactionResponse, StatsResponse
from app.services.pipeline import procesar_extracto


app = FastAPI(title="ASIENTO API")

def to_transaction_response(movimiento):
    return TransactionResponse(
            id= movimiento.id,
            date= movimiento.fecha,
            description= movimiento.descripcion,
            detail= movimiento.detalle,
            debit= movimiento.debito,
            credit= movimiento.credito,
            balance= movimiento.saldo,
            confidence= movimiento.confidence
            )
def to_statement_response(resultado):
    return StatementResponse(
        bank=resultado.banco,
        transactions=[to_transaction_response(movimiento) for movimiento in resultado.movimientos],
        validated_transactions=[to_transaction_response(movimiento) for movimiento in resultado.seguros],
        pending_review=[to_transaction_response(movimiento) for movimiento in resultado.revisar],
        stats= StatsResponse(
            total_movements= resultado.stats.total_movimientos,
            total_validated_movements= resultado.stats.total_seguros,
            total_pending_movements= resultado.stats.total_revisar
        )
    )

async def _process_uploaded_statement(file: UploadFile):
    contenido = await file.read()

    if not contenido.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="El archivo no parece ser un PDF válido"
        )

    try:
        with temporal_file(contenido) as ruta:
            resultado_pipeline= procesar_extracto(ruta)
            

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    return resultado_pipeline

@app.post("/statements")
async def process_statement(file: UploadFile = File(...)):
    resultado = await _process_uploaded_statement(file)
    return to_statement_response(resultado)


@app.post("/statements/export/excel")
async def export_statement_excel(file: UploadFile = File(...)):
    resultado = await _process_uploaded_statement(file)

    temporal = NamedTemporaryFile(
        suffix=".xlsx",
        delete=False
    )

    ruta_excel = temporal.name
    temporal.close()

    try:
        exportar_excel(resultado, ruta_excel)

    except Exception:
        os.unlink(ruta_excel)
        raise

    return FileResponse(
        path=ruta_excel,
        filename="asiento_movimientos.xlsx",
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        background=BackgroundTask(os.unlink, ruta_excel),
    )


@app.post("/statements/export/csv")
async def export_statement_csv(file: UploadFile = File(...)):
    resultado = await _process_uploaded_statement(file)

    temporal = NamedTemporaryFile(
        suffix=".csv",
        delete=False,
    )
    ruta_csv = temporal.name
    temporal.close()

    try:
        exportar_csv(resultado, ruta_csv)
    except Exception:
        os.unlink(ruta_csv)
        raise

    return FileResponse(
        path=ruta_csv,
        filename="asiento_movimientos.csv",
        media_type="text/csv",
        background=BackgroundTask(os.unlink, ruta_csv),
    )

@app.post("/statements/export/txt")
async def export_statement_txt(file: UploadFile = File(...)):
    resultado = await _process_uploaded_statement(file)

    temporal = NamedTemporaryFile(
        suffix=".txt",
        delete=False,
    )
    ruta_txt = temporal.name
    temporal.close()

    try:
        exportar_txt(resultado, ruta_txt)
    except Exception:
        os.unlink(ruta_txt)
        raise

    return FileResponse(
        path=ruta_txt,
        filename="asiento_movimientos.txt",
        media_type="text/plain",
        background=BackgroundTask(os.unlink, ruta_txt),
    )