import sys
from PySide6.QtWidgets import QApplication , QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QFileDialog
from PySide6.QtCore import QThread
from app.services.pipeline import procesar_extracto
from app.workers.extract_worker import ExtractWorker
import json

# QApplication es el nucleo de mi app en Qt, maneja el loop de eventos (clicks, teclado ,etc)

app = QApplication(sys.argv)


# QMainWindow es una ventana con estructura mas completa, tiene: (menu, status bar, etc)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASIENTO")
        self.resize(400,300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.texto = QTextEdit()
        self.texto.setReadOnly(True)
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.cambiar_texto)
        self.button = QPushButton("Clear")
        self.input.setPlaceholderText("Write something...")
        self.mensajes = ""
        self.button_pdf = QPushButton("Seleccionar PDF")
        self.button_process = QPushButton("Procesar")
        self.button_process.setEnabled(False)
        self.label_state = QLabel("State: no selected")

        self.button.clicked.connect(self.limpiar_texto)
        self.button_pdf.clicked.connect(self.seleccionar_pdf)
        self.button.clicked.connect(self.cambiar_texto)
        self.button_process.clicked.connect(self.procesar)
        
        self.definir_Vlayout()
        
    def seleccionar_pdf(self):
        self.ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if self.ruta:
            self.label_state.setText("State: file selected")
            self.button_process.setEnabled(True)
      
            



    def definir_Vlayout(self):
        self.layoutv = QVBoxLayout()
        self.layoutv.addWidget(self.label_state)
        self.layoutv.addWidget(self.texto)
        self.central_widget.setLayout(self.layoutv)
        self.layoutv.addLayout(self.definir_Hlayout())
        
    def obtener_input(self):
        return self.input.text()
    def agregar_mensaje(self,textos):
        self.texto.append(textos)
    def limpiar_texto(self):
        self.texto.clear()
    def cambiar_texto(self):
        texto_input = self.obtener_input().strip()
        if texto_input == "":
            return
        
        self.agregar_mensaje(texto_input)
        self.limpiar_texto()

    def crear_thread(self):
         #creo thread
        self.thread = QThread()
        #creo objeto worker
        self.worker = ExtractWorker(self.ruta)
        #muevo el worker al thread
        self.worker.moveToThread(self.thread)
        #cuando el thread arranca, correr worker.run
        self.thread.started.connect(self.worker.run)
        #logs del worker
        self.worker.log.connect(self.agregar_mensaje)
        #resultado final
        self.worker.finished.connect(self.proceso_finalizado)
        #errores
        self.worker.error.connect(self.mostrar_error)
        #limpio el thread al terminar
        self.worker.finished.connect(self.thread.quit)
        #destruyo los objetos correctamente
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.worker.deleteLater)
        #arranco el thread
        self.thread.start()

    def procesar(self):
        self.label_state.setText(f"State: processing - {self.ruta}")
        self.button_process.setEnabled(False)
        self.crear_thread()
        

    def proceso_finalizado(self, resultado):

        self.resultado = resultado
        
        self.resultado_json = json.dumps(self.resultado, indent=2, ensure_ascii=False)

        self.agregar_mensaje("Finished.")
        self.agregar_mensaje(self.resultado_json)
        self.label_state.setText("State: completed")

    def mostrar_error(self, error):
        self.agregar_mensaje(error)
        self.label_state.setText("State: Error")


    def definir_Hlayout(self):
        self.layouth = QHBoxLayout()
        self.layouth.addWidget(self.input)
        self.layouth.addWidget(self.button)
        self.layouth.addWidget(self.button_pdf)
        self.layouth.addWidget(self.button_process)
        self.layouth.addStretch()
        return self.layouth

   
        


if __name__ == "__main__":

    window = Window()
    window.show()
    # Este es el evento en prueba donde mantiene la app activa esperando los eventos, sino esta esto la ventana se abriria y cerrraria instantaneamente
    sys.exit(app.exec())