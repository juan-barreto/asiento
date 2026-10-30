import os
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from backend.services.temp_files import temporal_file
from backend.services.exporters.excel import exportar_excel
from app.services.pipeline import procesar_extracto


app = FastAPI(title="ASIENTO API")

async def _process_uploaded_statement(file: UploadFile):
    contenido = await file.read()

    if not contenido.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="El archivo no parece ser un PDF válido"
        )

    try:
        with temporal_file(contenido) as ruta:
            resultado = procesar_extracto(ruta)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    return resultado

@app.post("/statements")
async def process_statement(file: UploadFile = File(...)):
    resultado = await _process_uploaded_statement(file)
    return resultado


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