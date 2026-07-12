from PySide6.QtCore import QObject, Signal
from app.services.pipeline import procesar_extracto


class ExtractWorker(QObject):

    #Defincion de señales

    log = Signal(str)

    finished = Signal(object)

    error = Signal(str)

    def __init__(self,ruta):
        super().__init__()
        self.ruta = ruta

    def run(self):
        try:
            self.resultado = procesar_extracto(
                                self.ruta,
                                callback=self.log.emit
                                        )
            self.finished.emit(self.resultado)

        except Exception as e:
            self.error.emit(str(e))

