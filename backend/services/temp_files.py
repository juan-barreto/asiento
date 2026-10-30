import os
import tempfile
from contextlib import contextmanager



@contextmanager
def temporal_file(contenido: bytes):
    archivo = tempfile.NamedTemporaryFile(suffix= ".pdf", delete= False)
    ruta = archivo.name

    try:
        archivo.write(contenido)
        archivo.close()
        yield ruta
        
    finally:
        os.unlink(ruta)





