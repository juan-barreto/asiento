from fastapi import FastAPI, Query, File, UploadFile, HTTPException
from backend.services.temp_files import temporal_file
from app.services.pipeline import procesar_extracto

app = FastAPI(title="ASIENTO API")

@app.get("/")
def inicio():
    return {"mensaje": "ASIENTO API funcionando"}


@app.get("/extractos/{extracto_id}")
def obtener_extracto(extracto_id: int):
    return {
        "extracto_id": extracto_id,
        "mensaje": "Solicitud recibida correctamente"
    }

@app.get("/extractos")
def lista_extractos(limite: int = Query(default=10, ge=1, le=100)):
    return {"limite": limite}

@app.post("/extractos")
async def recibir_archivo(archivo: UploadFile = File(...)):

    contenido = await archivo.read()

    if not contenido.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="El archivo no parece ser un PDF válido"
        )
    with temporal_file(contenido) as ruta:
        resultado = procesar_extracto(ruta)
        
    return resultado

"""{
        "nombre": archivo.filename,
        "tipo": archivo.content_type,
        "tamaño" : len(contenido)
    }"""